import argparse
# Import Yamale and make a schema object:
import yamale
from yamale.schema import Schema
from yamale.yamale_error import YamaleError
import datetime
from .validators import DefaultValidators, RootValidation
import yaml
import os

def yamale_args_wrapper():
    parser = argparse.ArgumentParser(description='Validate yaml files.')
    parser.add_argument('-path', metavar='PATH', default='./', nargs='?',
                        help='folder to validate. Default is current directory.')
    parser.add_argument('-s', '--schema',
                        help='filename of schema. Default is schema.yaml.')
    parser.add_argument('-n', '--cpu-num', default=4, type=int,
                        help='number of CPUs to use. Default is 4.')
    parser.add_argument('-p', '--parser', default='pyyaml',
                        help='YAML library to load files. Choices are "ruamel" or "pyyaml" (default).')
    parser.add_argument('--no-strict', action='store_true',
                        help='Disable strict mode, unexpected elements in the data will be accepted.')
    parser.add_argument('--no-error', action='store_true',
                        help='Ignore error when violation of schema is identified.')
    parser.add_argument('--ok', default='okh',
                        help='This indicates which Open Know specification to use.')
    return parser.parse_args()

def included_ok_schema(oktype):
    module_root = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(module_root, 'schemas', oktype.lower() + '.yaml')

# validation_wrapper : in order to do root level validation, we will move from
# run validation and handle the YamaleError(s) for root and default validation
# then join those together into a common ValidationResults layer
# def validation_wrapper(schema, data, validators, args):
#     original_validation=False
#     # Capturing original logic
#     if original_validation:
#         root_validation = RootValidation(schema=schema, data=data, validators=validators, args=args)
#         root_validation_error = None
#     else:
#         root_validation = RootValidation(schema=schema, data=data, validators=validators, args=args)
#         root_validation_error = None
#         try:
#             pre_results = root_validation.validate() # single goes through here
#             print(pre_results)
#         except (YamaleError) as e:
#             print(type(pre_results))
#             print(pre_results)
#             root_validation_error = e

def composite_error_message(result, root_validation_error=None):
    results = []
    for r in result:
        results.append(str(r))
        if root_validation_error:
            # # print('ERROR? ' + str(type(root_validation_error)))
            # for result in root_validation_error.results:
            #     # print("Error validating data '%s' with '%s'\n\t" % (result.data, result.schema))
            #     for error in result.errors:
            #         print('\t%s' % error)
            # results.extend(root_validation_error.results)
            for result in root_validation_error.results:
                for error in result.errors:
                    error_string = '\t%s' % error
                    results.append(error_string)
    return '\n'.join(results)

def main():
    args = yamale_args_wrapper()
    validators = DefaultValidators.copy()
    schema_to_use = included_ok_schema(args.ok) if args.schema is None else args.schema
    results = []
    string_error_messages = []
    # error_messages = []
    data_filename_arr=[]
    path_to_use = args.path
    strict= not args.no_strict
    raise_error= not args.no_error
    
    try:
        schema = yamale.make_schema(schema_to_use, validators=validators)
        path_to_use = os.path.abspath(path_to_use)
        if os.path.isfile(path_to_use):
            if(path_to_use.endswith('.yaml') or path_to_use.endswith('.yml')):
                data_filename_arr.append(path_to_use)
        else:
            for root, dirs, files in os.walk(path_to_use):
                for f in files:
                    if (f.endswith('.yaml') or f.endswith('.yml')) and f != schema_to_use:
                        d = os.path.join(root, f)
                        data_filename_arr.append(d)

        file_count = 1

        for d in data_filename_arr:
            data = yamale.make_data(d) # currently single files
            # Create a Data object
            root_validation = RootValidation(schema=schema, data=data, validators=validators, args=args)
            root_validation_error = None
            try:
                root_validation.validate() # single goes through here
            except (YamaleError) as e:
                root_validation_error = e

            # root_level_validation(schema, data, validators, args)
            # Validate data against the schema. Throws a ValueError if data is invalid.
            mistake_made = False
            result = None
            try:
                should_raise_error = False if len(data_filename_arr) > 0 else raise_error
                result = yamale.validate(schema, data, strict, should_raise_error)
            except (SyntaxError, NameError, TypeError, ValueError, YamaleError) as f:
                print(f)
                print(result)
                mistake_made = True
            composited_error_message = composite_error_message(result, root_validation_error)
            if len(composited_error_message) > 0:
                string_error_messages.append(composited_error_message)
            results.extend(result)

            if file_count < len(data_filename_arr):
                file_count += 1

    except (SyntaxError, NameError, TypeError, ValueError, YamaleError) as e:
        err_type = str(type(e)).split("\'")[1]+": "
        print('Validation error!\n%s' % err_type+str(e))
        # TODO: should declare custom error types such as validation etc
        raise e
    if string_error_messages:
        raise ValueError('\n----\n'.join(set(string_error_messages)))
    # if error_messages:
    #     raise ValueError('\n----\n'.join(set(error_messages)))

if __name__ == '__main__':
    main()

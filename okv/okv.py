import argparse
# Import Yamale and make a schema object:
import yamale
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

def composite_error_message(result, root_validation_error=None):
    results = []
    for given_result in result:
        results.append(str(given_result))
        if root_validation_error:
            for error_result in root_validation_error.results:
                for error in error_result.errors:
                    error_string = '\t' + str(error)
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
    strict = not args.no_strict
    raise_error= not args.no_error
    
    schema = yamale.make_schema(schema_to_use, validators=validators)
    path_to_use = os.path.abspath(path_to_use)
    if os.path.isfile(path_to_use):
        if (path_to_use.endswith('.yaml') or path_to_use.endswith('.yml')):
            data_filename_arr.append(path_to_use)
    else:
        for root, _dirs, files in os.walk(path_to_use):
            for file in files:
                if (file.endswith('.yaml') or file.endswith('.yml')) and file != schema_to_use:
                    d = os.path.join(root, file)
                    data_filename_arr.append(d)

    file_count = 1

    for d in data_filename_arr:
        data = yamale.make_data(d)
        # Create a Data object
        root_validation = RootValidation(schema=schema, data=data, validators=validators, args=args)
        root_validation_error = None
        try:
            root_validation.validate()
        except (YamaleError) as err:
            root_validation_error = err

        # root_level_validation(schema, data, validators, args)
        # Validate data against the schema. Throws a ValueError if data is invalid.
        result = None
        try:
            should_raise_error = False if len(data_filename_arr) > 0 else raise_error
            result = yamale.validate(schema, data, strict, should_raise_error)
        except (SyntaxError, NameError, TypeError, ValueError, YamaleError) as f:
            print(f)
            print(result)
        error_message = composite_error_message(result, root_validation_error)
        if len(error_message) > 0:
            string_error_messages.append(error_message)
        results.extend(result)

        if file_count < len(data_filename_arr):
            file_count += 1

    if string_error_messages:
        raise ValueError('\n----\n'.join(set(string_error_messages)))

if __name__ == '__main__':
    main()

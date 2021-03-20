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
    parser.add_argument('--ok', default='okh',
                        help='This indicates which Open Know specification to use.')
    return parser.parse_args()

def included_ok_schema(oktype):
    module_root = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(module_root, 'schemas', oktype + '.yaml')

def main():
    args = yamale_args_wrapper()
    validators = DefaultValidators.copy()
    schema_to_use = included_ok_schema(args.ok) if args.schema is None else args.schema
    results = []
    data_filename_arr=[]
    path_to_use = args.path
    
    try:
        schema = yamale.make_schema(schema_to_use, validators=validators)
        if(path_to_use.endswith('.yaml') or path_to_use.endswith('.yml')):
            data_filename_arr.append(path_to_use)
        else:
            for root, dirs, files in os.walk(path_to_use):
                for f in files:
                    if (f.endswith('.yaml') or f.endswith('.yml')) and f != schema_to_use:
                        data_filename_arr.append(args.path+"/"+f)

        file_count = 1

        for d in data_filename_arr:
            # print(d)
            data = yamale.make_data(d) # currently single files
            # Create a Data object
            
            root_validation = RootValidation(schema=schema, data=data, validators=validators, args=args)
            pre_results = root_validation.validate() # single goes through here
            for p in pre_results:
                if '\'None\' is Valid' not in p:
                    print(p)

            # root_level_validation(schema, data, validators, args)
            # Validate data against the schema. Throws a ValueError if data is invalid.
            mistake_made = False
            try:
                result = yamale.validate(schema, data, False, False)
            except (SyntaxError, NameError, TypeError, ValueError, YamaleError) as f:
                print(f)
                print(result)
                mistake_made = True
            
            if mistake_made == False:
                results_list = list(dict.fromkeys(result))
                for r in results_list:
                    print(r)

            if file_count < len(data_filename_arr):
                print("\n • • • \n")
                file_count += 1

    except (SyntaxError, NameError, TypeError, ValueError, YamaleError) as e:
        err_type = str(type(e)).split("\'")[1]+": "
        print('Validation error!\n%s' % err_type+str(e))
        print("Consider revising .yaml format.")

if __name__ == '__main__':
    main()

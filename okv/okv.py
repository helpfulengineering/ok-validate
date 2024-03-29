import argparse
import datetime
import os
import sys

import yamale
import yaml
from yamale.yamale_error import YamaleError

from .validators import DefaultValidators, RootValidation



def yamale_args_wrapper():
    parser = argparse.ArgumentParser(description='Validate yaml files.')
    parser.add_argument(
        '-path',
        metavar='PATH',
        default='./',
        nargs='?',
        help='folder to validate. Default is current directory.',
    )
    parser.add_argument(
        '-s',
        '--schema',
        help='filename of schema. Default is schema.yaml.',
    )
    parser.add_argument(
        '-n', '--cpu-num',
        default=4,
        type=int,
        help='number of CPUs to use. Default is 4.',
    )
    parser.add_argument(
        '-p',
        '--parser',
        default='pyyaml',
        help='YAML library to load files. Choices are "ruamel" or "pyyaml" (default).',
    )
    parser.add_argument(
        '--no-strict',
        action='store_true',
        help='Disable strict mode, unexpected elements in the data will be accepted.',
    )
    parser.add_argument(
        '--no-error',
        action='store_true',
        help='Ignore error when violation of schema is identified.',
    )
    parser.add_argument(
        '--ok',
        default='okh',
        help='This indicates which Open Know specification to use.'
    )
    return parser.parse_args()


def included_ok_schema(oktype):
    module_root = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(module_root, 'schemas', oktype.lower() + '.yaml')


def composite_error_message(result, root_validation_error=None):
    results = []
    for given_result in result:
        if given_result.isValid():
            continue
        results.append(str(given_result))
        if root_validation_error:
            for error_result in root_validation_error.results:
                for error in error_result.errors:
                    error_string = '\t{0}'.format(str(error))
                    results.append(error_string)
    if results:
        return '\n'.join(results)
    return None


def _handle_error_exit(error_messages):
    raise_python_exception = False
    error_string = '\n----\n'.join(set(error_messages))
    if raise_python_exception:
        raise ValueError(error_string)
    print(error_string)
    sys.exit(1)


def main():
    args = yamale_args_wrapper()
    validators = DefaultValidators.copy()
    schema_to_use = included_ok_schema(args.ok) if args.schema is None else args.schema
    results = []
    string_error_messages = []
    data_filename_arr = []
    path_to_use = args.path
    strict = not args.no_strict
    raise_error = not args.no_error
    
    schema = yamale.make_schema(schema_to_use, validators=validators)
    path_to_use = os.path.abspath(path_to_use)
    if os.path.isfile(path_to_use):
        if (path_to_use.endswith('.yaml') or path_to_use.endswith('.yml')):
            data_filename_arr.append(path_to_use)
    else:
        for root, _dirs, files in os.walk(path_to_use):
            for file in files:
                if (file.endswith('.yaml') or file.endswith('.yml')) and file != schema_to_use:
                    data_filename = os.path.join(root, file)
                    data_filename_arr.append(data_filename)

    file_count = 1

    for data_filename in data_filename_arr:
        data = yamale.make_data(data_filename)
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
        should_raise_error = False if data_filename_arr else raise_error
        result = yamale.validate(schema, data, strict, should_raise_error)
        error_message = composite_error_message(result, root_validation_error)
        if error_message:
            string_error_messages.append(error_message)
        results.extend(result)

        if file_count < len(data_filename_arr):
            file_count += 1

    if string_error_messages:
        _handle_error_exit(string_error_messages)

if __name__ == '__main__':
    main()

import argparse
# Import Yamale and make a schema object:
import yamale
import datetime
from yamale.validators import DefaultValidators
from .validators import License

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

def yamale_args_wrapper():
    parser = argparse.ArgumentParser(description='Validate yaml files.')
    parser.add_argument('path', metavar='PATH', default='./', nargs='?',
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


def use_validators():
    validators = DefaultValidators.copy()  # This is a dictionary
    validators[License.tag] = License
    return validators

def included_ok_schema(oktype):
    print("This doesn't work yet -- needs pkgutil or something comparable to work relative to the installed module")
    return './schemas/' + oktype + '.yaml'

def main():
    args = yamale_args_wrapper()

    # schema = yamale.make_schema('./schema.yaml')
    validators = use_validators()
    schema_to_use = included_ok_schema(args.ok) if args.schema is None else args.schema
    schema = yamale.make_schema(schema_to_use, validators=validators)
    # schema = yamale.make_schema(schema_to_use)

    # Create a Data object
    path_to_use = args.path
    data = yamale.make_data(path_to_use)

    # Validate data against the schema. Throws a ValueError if data is invalid.
    yamale.validate(schema, data, None, not args.no_strict)

if __name__ == '__main__':
    main()
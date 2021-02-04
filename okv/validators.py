from yamale.validators import DefaultValidators, Validator
from yamale.util import get_subclasses
from yaml import dump
from yamale import make_schema, make_data, validate

class License(Validator):
    """ Custom License validator """
    tag = 'license'

    def _valid_licenses(self):
        return [
            'Apache-2.0',
            'CERN-OHL-1.2',
            'TO-PARTY',
            'TO-KILL'
        ]

    def _is_valid(self, value):
        # If there are no keys declared for hardware, documentation, software
        # then this will evaluate to false
        if not bool(value):
            return False
        keys_to_check = ['hardware', 'documentation', 'software']
        valid_licenses = self._valid_licenses()
        for key in keys_to_check:
            if key in value:
                if value[key] not in valid_licenses:
                    return False
        return True
    
    def fail(self, value):
        """Override to define a custom fail message"""
        if value is None:
            return 'There must be at least one license specified for \'hardware\', \'documentation\', or \'software\''
        else:
            return '\'%s\' has an invalid SPDX license.' % (value)

class Key(Validator):
    """ Custom Key validator """
    tag = 'key'

    def __init__(self, *args, **kwargs):
        super(Key, self).__init__(*args, **kwargs)
        self.key_name = args[0]

    def _is_valid(self, value):
        if self.key_name in value:
            return True
        return False
    
    def fail(self, value):
        """Override to define a custom fail message"""
        return '\'%s\' is missing from the map.' % (self.key_name)

class RootValidation(object):
    key = '__root_validator__'
    # Appeasing pylint
    schema = None
    data = []
    validators = None
    args = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def validate(self):
        """ Used for applying validation at the root level of the schema """
        # This is an experimental process
        schema = self.schema
        for item in schema.includes.items():
            if item[0] == self.key:
                root_level = self.data[0][0]
                root_level_dict = {"%s" % (self.key): root_level}
                yaml_dump = str(dump(root_level_dict))
                root_data = make_data(content=str(yaml_dump))
                root_schema_string = '%s: %s' % (self.key, item[1].dict)
                root_schema = make_schema(path=None, validators=self.validators, content=root_schema_string)
                validate(root_schema, root_data, None, not self.args.no_strict)
                break

DefaultValidators = {}

for v in get_subclasses(Validator):
    # Allow validator nodes to contain either tags or actual name
    DefaultValidators[v.tag] = v
    DefaultValidators[v.__name__] = v
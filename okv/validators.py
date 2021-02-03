from yamale.validators import DefaultValidators, Validator

class License(Validator):
    """ Custom License validator """
    tag = 'license'

    def _valid_licenses(self):
        return [
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
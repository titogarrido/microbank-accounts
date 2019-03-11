import re
from datetime import datetime
from flask_restplus.fields import Raw, Nested, List
from flask_restplus import fields
from flask import abort


EMAIL_REGEX = re.compile(r'\S+@\S+\.\S+')
URI_REGEX = re.compile(r'(http|https|ftp)://\S+\.\S+')


class CustomField(Raw):
    """
    Custom Field base class with validate feature
    """
    __schema_type__ = 'string'

    def __init__(self, *args, **kwargs):
        super(CustomField, self).__init__(**kwargs)
        # custom params
        self.positive = kwargs.get('positive', True)

    def format(self, value):
        """
        format the text in database for output
        works only for GET requests
        """
        if not self.validate(value):
            print('Validation of field with value \"%s\" (%s) failed' % (
                value, str(self.__class__.__name__)))
            # raise MarshallingError
            # disabling for development purposes as the server crashes when
            # exception is raised. can be enabled when the project is mature
        if self.__schema_type__ == 'string':
            return value
        else:
            return value

    def validate_empty(self):
        """
        Return when value is empty or null
        """
        if self.required:
            return False
        else:
            return True

    def validate(self, value):
        """
        Validate the value. return True if valid
        """
        pass


class Email(CustomField):
    """
    Email field
    """
    __schema_format__ = 'email'
    __schema_example__ = 'email@domain.com'

    def validate(self, value):
        if not value:
            return self.validate_empty()
        if not EMAIL_REGEX.match(value):
            return False
        return True


class Uri(CustomField):
    """
    URI (link) field
    """
    __schema_format__ = 'uri'
    __schema_example__ = 'http://website.com'

    def validate(self, value):
        if not value:
            return self.validate_empty()
        if not URI_REGEX.match(value):
            return False
        return True


class ImageUri(Uri):
    """
    Image URL (url ends with image.ext) field
    """
    __schema_example__ = 'http://website.com/image.ext'


class DateTime(CustomField):
    """
    Custom DateTime field
    """
    __schema_format__ = 'date-time'
    __schema_example__ = '2016-06-06 11:22:33'
    dt_format = '%Y-%m-%d %H:%M:%S'

    def to_str(self, value):
        return None if not value \
            else value.strftime(self.dt_format)

    def from_str(self, value):
        return None if not value \
            else datetime.strptime(value, self.dt_format)

    def format(self, value):
        if not value.__class__.__name__ in ['unicode', 'str']:
            return self.to_str(value)
        else:
            return value

    def validate(self, value):
        if not value:
            return self.validate_empty()
        try:
            print(value.__class__)
            if value.__class__.__name__ in ['unicode', 'str']:
                self.from_str(value)
            else:
                self.to_str(value)
        except Exception:
            return False
        return True

class Date(CustomField):
    """
    Custom Date field
    """
    __schema_format__ = 'date'
    __schema_example__ = '2016-06-06'
    dt_format = '%Y-%m-%d'

    def to_str(self, value):
        return None if not value \
            else value.strftime(self.dt_format)

    def from_str(self, value):
        return None if not value \
            else datetime.strptime(value, self.dt_format)

    def format(self, value):
        if not value.__class__.__name__ in ['unicode', 'str']:
            return self.to_str(value)
        else:
            return value
        

    def validate(self, value):
        if not value:
            return self.validate_empty()
        try:
            if value.__class__.__name__ in ['unicode', 'str']:
                self.from_str(value)
            else:
                self.to_str(value)
        except Exception:
            return False
        return True

class String(CustomField):
    """
    Custom String Field
    """
    def validate(self, value):
        if not value:
            return self.validate_empty()
        if value.__class__.__name__ in ['unicode', 'str']:
            return True
        else:
            return False


class Integer(CustomField):
    """
    Custom Integer Field
    Args:
        :positive - accept only positive numbers, True by default
    """
    __schema_type__ = 'integer'
    __schema_format__ = 'int'
    __schema_example__ = 0

    def validate(self, value):
        if value is None:
            return self.validate_empty()
        if type(value) != int:
            return False
        if self.positive and value < 0:
            return False
        return True


class Float(CustomField):
    """
    Custom Float Field
    """
    __schema_type__ = 'number'
    __schema_format__ = 'float'
    __schema_example__ = 0

    def validate(self, value):
        if value is None:
            return self.validate_empty()
        try:
            float(value)
            return True
        except Exception:
            return False

def validate_payload(payload, api_model):
    """
    Validate payload against an api_model. Aborts in case of failure
    - This function is for custom fields as they can't be validated by
      flask restplus automatically.
    - This is to be called at the start of a post or put method
    """
    # check if any reqd fields are missing in payload
    for key in api_model:
        if api_model[key].required and key not in payload:
            abort(400, 'Required field \'%s\' missing' % key)
    # check payload
    for key in payload:
        field = api_model[key]
        if isinstance(field, fields.List):
            field = field.container
            data = payload[key]
        else:
            data = [payload[key]]
        if isinstance(field, CustomField) and hasattr(field, 'validate'):
            for i in data:
                if not field.validate(i):
                    abort(400, 'Validation of \'%s\' field failed' % key)
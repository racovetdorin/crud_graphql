import re
from pydantic import BaseModel, validator, constr



def validate_name_or_surname(value, field_name):
    pattern = r'^[a-zA-Z0-9_\-\. ]*$'
 
    if not re.match(pattern, value):
        raise ValueError(f'The {field_name} should not contain any special characters.')
    
    return value

def validate_lowercase_alphanumeric(value, field_name):
    pattern = r'^[a-z0-9]*$'
    if not re.match(pattern, value):
        raise ValueError(f'The {field_name} should not contain any special characters or uppercase letters.')
    return value


class PersonModel(BaseModel):
    name: constr(strip_whitespace=True, max_length=255) 
    surname: constr(strip_whitespace=True, max_length=255)

    @validator('name')
    def validate_name(cls, value):
        return validate_name_or_surname(value, 'name')
    
    @validator('surname')
    def validate_surname(cls, value):
        return validate_name_or_surname(value, 'surname')


class IdValidator(BaseModel):
    id: str

    @validator('id')
    def validate_name(cls, value):
        return validate_lowercase_alphanumeric(value, 'id')


class UpdatePersonModel(PersonModel, IdValidator):
    pass

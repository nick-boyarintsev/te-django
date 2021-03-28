from datetime import datetime
from json import loads
from re import match, IGNORECASE, UNICODE
from typing import Final, Union, TypedDict

from django.http import JsonResponse


def validate_registration_id(registrationId: str) -> bool:
    """
    Validation for `registrationId` query string resource. \\
    Required format: according to `ISO 639-1`.
    """
    if match(r'^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$', registrationId, IGNORECASE):
        return True
    return False


def validate_registration_date(registrationDate: str) -> bool:
    """
    Validation for `registrationDate` field. \\
    Required format: `%Y-%m-%dT%H:%M:%S.%f%z`.
    """
    try:
        datetime.strptime(registrationDate, '%Y-%m-%dT%H:%M:%S.%f%z')
        return True
    except ValueError:
        return False


def validate_locale(locale: str) -> bool:
    """
    Validation for `locale` field. \\
    Required format: according to `ISO 639-1`.
    """
    if len(locale) == 2 and match(r'^[A-Z]{2}$', locale, IGNORECASE):
        return True
    return False


def validate_person(person: str) -> bool:
    """
    Validation for `person` field. \\
    Required format: JSON string.
    """
    try:
        jperson = loads(person)
        if isinstance(jperson, dict):
            return True
        return False
    except ValueError:
        return False


def validate_name_part(name_part: str) -> bool:
    """
    Validation for `firstName` or `lastName` field. \\
    Required format: minimum 1 character, maximum 150 characters.
    """
    if match(r'^\w{1,150}$', name_part, UNICODE):
        return True
    return False


def validate_email(email: str) -> bool:
    """
    Validation for `email` field. \\
    Required format: RFC 2822.
    """
    if match(r'^(?:[a-zA-Z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-zA-Z0-9-]*[a-zA-Z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$', email):
        return True
    return False


class FieldError(TypedDict):
    """
    Typing for FieldError scheme.
    """
    field: Union[str, None]
    code: Union[str, None]
    message: Union[str, None]


FieldErrors = list[FieldError]


class ApiException(Exception):
    """
    Exception handler for REST API handlers.
    """
    ERROR_VALIDATION_FAILED: Final = 'ValidationFailed'
    ERROR_INTERNAL_SERVER: Final = 'InternalServerError'

    FIELD_ERROR_IS_REQUIRED_CODE: Final = 'IsRequired'
    FIELD_ERROR_INVALID_FORMAT_CODE: Final = 'InvalidFormat'

    FIELD_ERROR_IS_REQUIRED_MESSAGE: Final = 'The field is required'

    def __init__(self, http_code: int, request_id: str, error_code: str,
                 error_message: (str, None) = None,
                 field_errors: Union[FieldErrors, None] = None):
        self.http_code = http_code
        self.request_id = request_id
        self.error_code = error_code
        self.error_message = error_message
        self.field_errors = field_errors
        self.response = JsonResponse(
            data={
                'error': {
                    'code': self.error_code,
                    'message': self.error_message,
                },
                'fieldErrors': self.field_errors,
            },
            status=http_code
        )
        self.response['x-correlationid'] = self.request_id

import logging

from json import loads
from uuid import uuid4

from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from rest_api.errors import (
    ApiException,
    validate_registration_id,
    validate_registration_date,
    validate_locale,
    validate_person,
    validate_name_part,
    validate_email,
)

logger = logging.getLogger('django.request')


@csrf_exempt
@require_http_methods(['GET'])
def get_registrations(request, registrationId):
    """
    Handler for GET method of REST API \\
    It gets registration data of user by his ID.
    """
    try:
        existing_user = None
        logger.info('Requested user ID: ' + registrationId)
        try:
            if not registrationId or not validate_registration_id(registrationId):
                raise ApiException(
                    http_code=404,
                    request_id=request.META['x-correlationid'],
                    error_code=ApiException.ERROR_VALIDATION_FAILED,
                    error_message='The UUID-v4 string in the format according to standard RFC 4122 is required ' +
                                  'for query string resource'
                )
            existing_user = cache.get(registrationId.lower())
            if not existing_user:
                raise ApiException(
                    http_code=404,
                    request_id=request.META['x-correlationid'],
                    error_code=ApiException.ERROR_VALIDATION_FAILED,
                    error_message='User with this registration ID is not present in the system'
                )
        except ApiException as e:
            logger.error(e.error_message)
            return e.response
        logger.info('Requested user data: ' + str(existing_user))
        response = JsonResponse(data=existing_user)
        response['x-correlationid'] = request.META['x-correlationid']
        return response
    except Exception as e:
        logger.error(type(e))
        logger.error(e)
        response = JsonResponse(
            status=500,
            data={
                'error': {
                    'code': ApiException.ERROR_INTERNAL_SERVER,
                    'message': 'An unexpected error occurred. Please try again later.',
                },
                'fieldErrors': None,
            }
        )
        response['x-correlationid'] = request.META['x-correlationid']
        return response


@csrf_exempt
@require_http_methods(['POST'])
def post_registrations(request):
    """
    Handler for POST method of REST API. It registers a user.
    """
    try:
        data = None
        try:
            if request.body == b'':
                raise ApiException(
                    http_code=400,
                    request_id=request.META['x-correlationid'],
                    error_code=ApiException.ERROR_VALIDATION_FAILED,
                    error_message='The request body must not be empty'
                )
            data = loads(request.body)
            logger.info('Requested data for registration: ' + str(data))
            if 'registrationDate' not in data:
                raise ApiException(
                    http_code=400,
                    request_id=request.META['x-correlationid'],
                    error_code=ApiException.ERROR_VALIDATION_FAILED,
                    field_errors=[{
                        'field': 'registrationDate',
                        'code': ApiException.FIELD_ERROR_IS_REQUIRED_CODE,
                        'message': ApiException.FIELD_ERROR_IS_REQUIRED_MESSAGE,
                    }]
                )
            if not isinstance(data['registrationDate'], str) \
               or not validate_registration_date(data['registrationDate']):
                raise ApiException(
                    http_code=400,
                    request_id=request.META['x-correlationid'],
                    error_code=ApiException.ERROR_VALIDATION_FAILED,
                    field_errors=[{
                        'field': 'registrationDate',
                        'code': ApiException.FIELD_ERROR_INVALID_FORMAT_CODE,
                        'message': 'The datetime string in the format "%Y-%m-%dT%H:%M:%S.%f%z" is required',
                    }]
                )
            if 'locale' not in data:
                raise ApiException(
                    http_code=400,
                    request_id=request.META['x-correlationid'],
                    error_code=ApiException.ERROR_VALIDATION_FAILED,
                    field_errors=[{
                        'field': 'locale',
                        'code': ApiException.FIELD_ERROR_IS_REQUIRED_CODE,
                        'message': ApiException.FIELD_ERROR_IS_REQUIRED_MESSAGE,
                    }]
                )
            if not isinstance(data['locale'], str) or not validate_locale(data['locale']):
                raise ApiException(
                    http_code=400,
                    request_id=request.META['x-correlationid'],
                    error_code=ApiException.ERROR_VALIDATION_FAILED,
                    field_errors=[{
                        'field': 'locale',
                        'code': ApiException.FIELD_ERROR_INVALID_FORMAT_CODE,
                        'message': 'The string in the format according to standard ISO 639-1 is required',
                    }]
                )
            data['locale'] = data['locale'].lower()
            if 'person' not in data:
                raise ApiException(
                    http_code=400,
                    request_id=request.META['x-correlationid'],
                    error_code=ApiException.ERROR_VALIDATION_FAILED,
                    field_errors=[{
                        'field': 'person',
                        'code': ApiException.FIELD_ERROR_IS_REQUIRED_CODE,
                        'message': ApiException.FIELD_ERROR_IS_REQUIRED_MESSAGE,
                    }]
                )
            if not isinstance(data['person'], str) or not validate_person(data['person']):
                raise ApiException(
                    http_code=400,
                    request_id=request.META['x-correlationid'],
                    error_code=ApiException.ERROR_VALIDATION_FAILED,
                    field_errors=[{
                        'field': 'person',
                        'code': ApiException.FIELD_ERROR_INVALID_FORMAT_CODE,
                        'message': 'It must be the valid JSON string',
                    }]
                )
            data['person'] = loads(data['person'])
            if 'firstName' not in data['person']:
                raise ApiException(
                    http_code=400,
                    request_id=request.META['x-correlationid'],
                    error_code=ApiException.ERROR_VALIDATION_FAILED,
                    field_errors=[{
                        'field': 'firstName',
                        'code': ApiException.FIELD_ERROR_IS_REQUIRED_CODE,
                        'message': 'The field "person" includes "firstName". '
                                   + ApiException.FIELD_ERROR_IS_REQUIRED_MESSAGE,
                    }]
                )
            if not isinstance(data['person']['firstName'], str) or not validate_name_part(data['person']['firstName']):
                raise ApiException(
                    http_code=400,
                    request_id=request.META['x-correlationid'],
                    error_code=ApiException.ERROR_VALIDATION_FAILED,
                    field_errors=[{
                        'field': 'firstName',
                        'code': ApiException.FIELD_ERROR_INVALID_FORMAT_CODE,
                        'message': 'Does not match format: at least 1 character string, 150 characters maximum',
                    }]
                )
            if 'lastName' not in data['person']:
                raise ApiException(
                    http_code=400,
                    request_id=request.META['x-correlationid'],
                    error_code=ApiException.ERROR_VALIDATION_FAILED,
                    field_errors=[{
                        'field': 'lastName',
                        'code': ApiException.FIELD_ERROR_IS_REQUIRED_CODE,
                        'message': 'The field "person" includes "lastName". '
                                   + ApiException.FIELD_ERROR_IS_REQUIRED_MESSAGE,
                    }]
                )
            if not isinstance(data['person']['lastName'], str) or not validate_name_part(data['person']['lastName']):
                raise ApiException(
                    http_code=400,
                    request_id=request.META['x-correlationid'],
                    error_code=ApiException.ERROR_VALIDATION_FAILED,
                    field_errors=[{
                        'field': 'lastName',
                        'code': ApiException.FIELD_ERROR_INVALID_FORMAT_CODE,
                        'message': 'Does not match format: at least 1 character string, 150 characters maximum',
                    }]
                )
            if 'email' not in data['person']:
                raise ApiException(
                    http_code=400,
                    request_id=request.META['x-correlationid'],
                    error_code=ApiException.ERROR_VALIDATION_FAILED,
                    field_errors=[{
                        'field': 'email',
                        'code': ApiException.FIELD_ERROR_IS_REQUIRED_CODE,
                        'message': 'The field "person" includes "email". '
                                   + ApiException.FIELD_ERROR_IS_REQUIRED_MESSAGE,
                    }]
                )
            if not isinstance(data['person']['email'], str) or not validate_email(data['person']['email']):
                raise ApiException(
                    http_code=400,
                    request_id=request.META['x-correlationid'],
                    error_code=ApiException.ERROR_VALIDATION_FAILED,
                    field_errors=[{
                        'field': 'email',
                        'code': ApiException.FIELD_ERROR_INVALID_FORMAT_CODE,
                        'message': 'The string in the format according to standard RFC 2822 (or RFC 822) is required',
                    }]
                )
        except ApiException as e:
            logger.error(e.field_errors)
            return e.response
        new_uuid = None
        while(True):
            new_uuid = str(uuid4())
            existing_user = cache.get(new_uuid)
            if not existing_user:
                break
        logger.info('The new user is registered with ID: ' + new_uuid)
        cache.set(new_uuid, data, None)
        response = JsonResponse(status=201, data={'registrationId': new_uuid})
        response['x-correlationid'] = request.META['x-correlationid']
        return response
    except Exception as e:
        logger.error(type(e))
        logger.error(e)
        response = JsonResponse(
            status=500,
            data={
                'error': {
                    'code': ApiException.ERROR_INTERNAL_SERVER,
                    'message': 'An unexpected error occurred. Please try again later.',
                },
                'fieldErrors': None,
            }
        )
        response['x-correlationid'] = request.META['x-correlationid']
        return response

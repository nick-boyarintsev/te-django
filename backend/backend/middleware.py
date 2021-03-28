import uuid

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object
from backend import local


class XCorrelationIDMiddleware(MiddlewareMixin):
    """
    A middleware made to track a request and the processes that occur during its processing.
    """

    def process_request(self, request):
        if 'x-correlationid' not in request.META:
            local.request_id = uuid.uuid4().hex
            request.META['x-correlationid'] = local.request_id

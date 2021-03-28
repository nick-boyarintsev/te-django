import logging

from backend import get_current_request_id


class RequestFilter(logging.Filter):
    """
    A special filter for the correct display of the request tracker.
    """

    def filter(self, record):
        record.x_correlation_id = get_current_request_id()
        return True

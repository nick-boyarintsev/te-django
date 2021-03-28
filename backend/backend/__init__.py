import threading

local = threading.local()


def get_current_request_id():
    try:
        return local.request_id
    except AttributeError:
        return 'processing'

from typing import Callable

import requests


def timeout_exception(func: Callable) -> Callable:
    def wrapped_func(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except requests.exceptions.ConnectTimeout:
            print('Timeout exceeded')
    return wrapped_func

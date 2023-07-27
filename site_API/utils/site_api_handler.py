import requests

from typing import Dict


def _make_response(method: str, url: str, headers: Dict, params: Dict,
                   timeout: int, success=200):
    response = requests.request(
        method,
        url,
        headers=headers,
        params=params,
        timeout=timeout
    )

    status_code = response.status_code

    if status_code == success:
        return response

    return status_code


def _get_property(method: str, url: str, headers: Dict,
                  params: Dict, timeout: int, func=_make_response):

    url = "{0}".format(url)

    response = func(method, url, headers=headers, params=params,
                    timeout=timeout)

    return response


class SiteApiInterface():

    @staticmethod
    def get_property():
        return _get_property


if __name__=="__main__":
    _make_response()
    _get_property()

    SiteApiInterface()

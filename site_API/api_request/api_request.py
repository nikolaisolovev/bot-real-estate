from typing import List

from site_API.core import headers, params, site_api, url
from tg_API.utils.exception_handlers import timeout_exception


@timeout_exception
def request_from_user(user_city: str, user_ordering: str, user_units: int, id: int) -> List:
    prop_for_user = site_api.get_property()

    params = {
        "area": user_city,
        "category": "residential",
        "order_by": "price",
        "ordering": user_ordering,
        "page_number": "1",
        "page_size": user_units
    }

    response = prop_for_user("GET", url, headers, params, timeout=15)
    response = response.json()
    listing = response.get("listing", [])

    result_list = []

    for i_unit in range(user_units):
        price_per_month = listing[i_unit]["rental_prices"]["per_month"]
        address = listing[i_unit]["agent_address"]
        photo = listing[i_unit]["image_url"]

        data = {
            "city": user_city,
            "county": response.get("county", None),
            "price": price_per_month,
            "user_id": id,
            "address": address,
            "photo": photo
        }

        result_list.append(data)

    return result_list


@timeout_exception
def custom_request_from_user(user_city: str, user_min_value: int, user_max_value: int, user_units: int, id: int) -> List:
    prop_for_user = site_api.get_property()

    params = {
        "area": user_city,
        "order_by": "price",
        "ordering": "ascending",
        "page_number": "1",
        "page_size": str(user_units)
    }

    response = prop_for_user("GET", url, headers, params, timeout=15)
    response = response.json()
    listing = response.get("listing", [])

    result_list = []

    for i_unit in range(user_units):
        price_per_month = listing[i_unit]["rental_prices"]["per_month"]
        address = listing[i_unit]["agent_address"]
        photo = listing[i_unit]["image_url"]
        details_url = listing[i_unit]["details_url"]
        if price_per_month in range(user_min_value, user_max_value):

            data = {
                "city": user_city,
                "county": response.get("county", None),
                "price": price_per_month,
                "user_id": id,
                "address": address,
                "photo": photo,
                "url": details_url
            }

            result_list.append(data)

    return result_list

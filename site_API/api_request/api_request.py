from typing import List

from site_API.core import headers, params, site_api, url
from tg_API.utils.exception_handlers import timeout_exception


@timeout_exception
def request_from_user(user_city: str, user_ordering: str, user_units: int, id: int) -> List:
    prop_for_user = site_api.get_property()
    params = get_params(user_city, user_ordering, user_units)

    params["category"] = "residential"

    county, listing = get_county_and_listing_by_request(params, prop_for_user)

    result_list = get_result_list_from_user_units(county, id, listing, user_city, user_units,
                                                  user_max_value=None, user_min_value=None,
                                                  check_price_per_month=False)

    return result_list


@timeout_exception
def custom_request_from_user(user_city: str, user_min_value: int, user_max_value: int, user_units: int, id: int) -> List:
    user_ordering = "ascending"

    prop_for_user = site_api.get_property()
    params = get_params(user_city, user_ordering, user_units)

    county, listing = get_county_and_listing_by_request(params, prop_for_user)

    result_list = get_result_list_from_user_units(county, id, listing, user_city, user_units,
                                                  user_max_value, user_min_value,
                                                  check_price_per_month=True)

    return result_list


def get_result_list_from_user_units(county, id, listing,
                                    user_city, user_units,
                                    user_max_value, user_min_value,
                                    check_price_per_month):
    result_list = []
    for i_unit in range(user_units):
        price_per_month = listing[i_unit]["rental_prices"]["per_month"]
        address = listing[i_unit]["agent_address"]
        details_url = listing[i_unit]["details_url"]
        photo = listing[i_unit]["image_url"]

        if not check_price_per_month or price_per_month in range(user_min_value, user_max_value):
            data = {
                "city": user_city,
                "county": county,
                "price": price_per_month,
                "user_id": id,
                "address": address,
                "photo": photo,
                "url": details_url
            }

            result_list.append(data)
    return result_list


def get_county_and_listing_by_request(params, prop_for_user):
    response = prop_for_user("GET", url, headers, params, timeout=15)
    response = response.json()
    listing = response.get("listing", [])
    county = response.get("county", None)
    return county, listing


def get_params(user_city, user_ordering, user_units):
    params = {
        "area": user_city,
        "order_by": "price",
        "ordering": user_ordering,
        "page_number": "1",
        "page_size": str(user_units)
    }
    return params

import re

_CITY_MAP = {
    'new york': 'new york city',
    'mexico, ciudad de': 'mexico city',
    'delhi municipal corporation': 'delhi',
    'bogotá': 'bogota',
    'greater hyderabad municipal corporation': 'hyderabad',
    'hong kong sar': 'hong kong',
    'moskva': 'moscow'
}

def country1(country):
    """
    Normalize the given country. For example, take United Kingdom of Great
    Britain and Northern Ireland and make it United Kingdom. Right now this list
    is very fixed and not flexible.

    Args
    country: The country name to normalize.

    Returns
    The normalized country name.
    """
    tmp = re.sub('\s*\(.*?\)', '', country)
    tmp = tmp.replace('\xa0', ' ')

    return _norm(tmp.lower(), _COUNTRY_MAP)

def city(city):
    """
    Normalize the given city. For example, take Delhi Municipal Corporation to
    delhi. The returned name is not capitalized in any way.

    Args
    city: The city name to normalize.

    Returns
    The normalized city name.
    """
    return _norm(city.lower(), _CITY_MAP)

def _norm(text, m):
    try:
        norm = m[text]
    except KeyError:
        norm = text

    return norm

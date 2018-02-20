_COUNTRY_MAP = {
    'united kingdom of great britain and northern ireland': 'united kingdom',
    'russian federation': 'russia',
    'china, hong kong sar': 'hong kong',
    'united republic of tanzania': 'tanzania',
    'czechia': 'czech republic'
}

_CITY_MAP = {
    'new york': 'new york city',
    'mexico, ciudad de': 'mexico city',
    'delhi municipal corporation': 'delhi',
    'bogotá': 'bogota',
    'greater hyderabad municipal corporation': 'hyderabad',
    'hong kong sar': 'hong kong',
    'moskva': 'moscow'
}

def country(country):
    """
    Normalize the given country. For example, take United Kingdom of Great
    Britain and Northern Ireland and make it United Kingdom. Right now this list
    is very fixed and not flexible.

    Args
    country: The country name to normalize.

    Returns
    The normalized country name.
    """
    return _norm(country, _COUNTRY_MAP)

def city(city):
    """
    Normalize the given city. For example, take Delhi Municipal Corporation to
    Delhi.

    Args
    city: The city name to normalize.

    Returns
    The normalized city name.
    """
    return _norm(city, _CITY_MAP)

def _norm(text, m):
    try:
        norm = m[text.lower()]
    except KeyError:
        norm = text

    return norm.title()

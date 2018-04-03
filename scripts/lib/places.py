import requests

from lib.geo.country import Country
from lib.geo.region import Region

class LookupClient:
    """
    An abstract client to lookup information. This class by itself is useless
    and must be extended. Extending consists of defining the url template, the
    key if one is needed, and a method of picking the final result out of the
    response.
    """

    def __init__(self, key=''):
        """
        Create a new LookupClient.

        Args
        key: The key for this client. Optional and may be discarded.
        """
        self.key = key

    def _template(self):
        """
        The template for urls. The format method with strings will be used. In
        the template, put {0} where the key goes, and {n} for the n-th argument
        to the query.

        Returns
        The template for this url to be used with string format.
        """
        pass

    def _lookup(self, *args):
        """
        Lookup and return the desired option from the query. Extensions will use
        this method to lookup their information.

        Args
        *args: The arguments provided to this client.

        Returns
        The picked info from the received response.
        """
        return self._pick(self._query(self._mapper(*args)), *args)

    def _query(self, args):
        """
        Queries the service provided by the template passing in the key and var
        args passed into this method. If the response has an error code or is
        not parseable, then an HTTPError will be raised.

        Args
        args: The args to the template url in order.

        Returns
        The json response of the request. Throws an HTTPError if appropriate.
        """
        url = self._template().format(self.key, *args)

        r = requests.get(url)
        r.raise_for_status()

        return r.json()

    def _pick(self, resp, *args):
        """
        Given the actual query and the response from said query, pick the
        desired info out of the response.

        Args
        resp: The response from the service defined by the template.
        *args: The arguments that were used in a query to this client.

        Returns
        The desired bit of information out of the response.
        """
        pass

    def _mapper(self, *args):
        """
        Convert the input to the lookup to a string format of args that can be
        used in the query template.

        Args
        args: The arguments to use in the query.

        Returns
        The mapped arguments.
        """
        return args


class RegionLookupClient(LookupClient):
    """
    Lookup a region (continent) based on a country. This class must be extended
    to define the service that will be used to lookup the region and how to
    parse the result.
    """

    def __init__(self):
        super().__init__()

    def region(self, country):
        """
        Lookup the region for a given country.

        Args
        country: The country whose region we are looking for.

        Returns
        The region this country is in.
        """
        return self._lookup(country)

    # TODO
    def _mapper(self, *args):
        """
        Convert the input to the lookup to a string format of args that can be
        used in the query template. In this case, convert the Country enum to
        its value.

        Args
        args: The arguments to use in the query. In this case, the country.

        Returns
        The country name as a string.
        """
        return [args[0].value]


class RestCountriesClient(RegionLookupClient):
    """
    A client that lookups up regions using the RestCountries API.
    """
    _COUNTRIES_MAP = {
        Country.SOUTH_KOREA: 'korea (republic of)',
        Country.NORTH_KOREA: 'korea (democratic people\'s republic of)',
        Country.REPUBLIC_OF_THE_CONGO: 'congo',
    }

    def __init__(self):
        super().__init__()

    def _template(self):
        # TODO:
        return 'https://restcountries.eu/rest/v2/name/{1}'

    def _pick(self, resp, country):
        """
        Out of the response pick the result that has the exact same name as the
        passed in country. If none exists, simply return the first result.

        Args:
        resp: The response from the API.
        country: The country that was passed to the api to lookup the region.

        Returns:
        """
        for result in resp:
            if result['name'].upper() == country.name.upper():
                return Region[result['region'].upper()]

        return Region[resp[0]['region'].upper()]

    def _mapper(self, *args):
        """
        Convert the input to the lookup to a string format of args that can be
        used in the query template. In this case, convert the Country enum to
        its value. This mapper is specialize to handle idiosyncrasies in the
        API's country name.

        Args
        args: The arguments to use in the query. In this case, the country.

        Returns
        The country name as a string.
        """
        try:
            return [RestCountriesClient._COUNTRIES_MAP[args[0]]]
        except KeyError:
            return super()._mapper(*args)

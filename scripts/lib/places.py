import math

import editdistance
import requests

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
        return self._pick(self._query(args), *args)

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
        The desired bit of information out  of the response.
        """
        pass

class CountryLookupClient(LookupClient):
    """
    Lookup a country based on a city. This class must be extended to define the
    service that will be used to lookup the country and how to parse the
    response.
    """

    def country(self, city):
        """
        Lookup the country for a given city.

        Args
        city: The city whose country we are looking for.

        Returns
        The country this city is in.
        """
        return self._lookup(city)

class RegionLookupClient(LookupClient):
    """
    Lookup a region (continent) based on a country. This class must be extended
    to define the service that will be used to lookup the region and how to
    parse the result.
    """

    def region(self, country):
        """
        Lookup the region for a given country.

        Args
        country: The country whose region we are looking for.

        Returns
        The region this country is in.
        """
        return self._lookup(country)


class RestCountriesClient(RegionLookupClient):
    """
    A client that lookups up regions using the RestCountries API.
    """

    def __init__(self):
        super(RegionLookupClient, self).__init__()

    def _template(self):
        # TODO:
        return 'https://restcountries.eu/rest/v2/name/{1}'

    def _pick(self, resp, country):
        return resp[0]['region']


class GooglePlacesClient(CountryLookupClient):
    """
    A client that looks up countries using the Google Places API.
    """
    def _template(self):
        # TODO:
        return 'https://maps.googleapis.com/maps/api/place/autocomplete/json?input={1}&types=(cities)&key={0}'

    def _pick(self, resp, city):
        if resp['status'] == 'OK':
            min_ed_country = None
            min_ed = float('inf')

            for pred in resp['predictions']:
                pred_city = pred['terms'][0]['value']
                pred_country = pred['terms'][-1]['value']

                ed = editdistance.eval(city, pred_city)
                if ed < min_ed:
                    min_ed_country = pred_country
                    min_ed = ed

                if ed == 0:
                    break

            return min_ed_country
        
        return ''

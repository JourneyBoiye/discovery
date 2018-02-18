import math

import editdistance
import requests

# TODO: Add documentation.

class Client:
    def __init__(self, key):
        self.key = key

    def _template(self):
        pass

    def country(self, city):
        return self._pick(self._query(city), city)

    def _query(self, *args):
        url = self._template().format(self.key, *args)

        r = requests.get(url)
        r.raise_for_status()

        return r.json()

    def _pick(self, resp):
        pass

class GooglePlacesClient(Client):
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

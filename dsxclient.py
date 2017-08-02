from baseclient import BaseClient
import urllib


class DsxClient(BaseClient):
    def __init__(self, api_key, protocol=None, url=None):
        self.protocol = 'https'
        self.url = 'dsx.weather.com'
        self.api_key = api_key

    def search_locations(self, location):
        # lol url path
        a = ['x', 'v2', 'web', 'loc', 'en_US']
        # bunch of random numbers?
        b = ['1', '4', '5', '9', '11', '13', '19', '21', '1000', '1001', '1003']
        c = ['us^', urllib.parse.quote(location)]
        params = {
            'api': self.api_key,
            'format': 'json',
            'pg': '0,10'
        }
        response = self._get(path=a+b+c, params=params)
        try:
            return response.json()
        except:
            print(response.text)
            raise

    def get_past_observations(self, datetime, numdays, loc_key):
        path = ["wxd/v2/PastObsAvg", "en_US", datetime, numdays, loc_key]
        params = {
            'api': self.api_key,
            'format': 'json'
        }
        response = self._get(path=path, params=params)
        try:
            return response.json()
        except:
            print(response.text)
            raise

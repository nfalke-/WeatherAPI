from baseclient import BaseClient
from utils import parse

class ApiClient(BaseClient):
    def __init__(self, api_key, protocol=None, url=None):
        self.protocol = 'https'
        self.version = 'v2'
        self.api = 'turbo'
        self.url = 'api.weather.com'
        self.api_key = api_key
        #function
        self.get_precipitation = self.base_function(
                'vt1precipitation', 'startTime'
            )
        #function
        self.get_forecast = self.base_function(
                'vt1dailyForecast', 'sunrise'
            )
        #function
        self.get_fifteen = self.base_function(
                'vt1fifteenminute', 'icon'
            )

        #function
        self.get_hourly = self.base_function(
                'vt1hourlyForecast', 'icon'
            )

    def get_alminac(self, geocode, start, end, units='e'):
        geocode = geocode.split(',')
        path = ['v1/geocode', geocode[0], geocode[1], 'almanac/daily.json']
        params = {
            'apiKey': self.api_key,
            'end': end,
            'start': start,
            'units': units
        }
        response = self._get(path=path, params=params)
        try:
            return response.json()['almanac_summaries']
        except:
            print(response.text)
            raise


    def get_observation(self, geocode, language='en-US', units='e', format='json'):
        path = [self.version, self.api, 'vt1observation']
        params = {
            'apiKey': self.api_key,
            'geocode': geocode,
            'units': units,
            'language': language,
            'format': format
        }
        response = self._get(path=path, params=params)
        try:
            return [response.json()['vt1observation']]
        except:
            print(response.text)
            raise

    @parse('weed')
    def get_pollen(self, geocode, language='en-US', format='json'):
        endpoint = 'vt1pollenforecast'
        path = [self.version, self.api, endpoint]
        params = {
            'apiKey': self.api_key,
            'geocode': geocode,
            'language': language,
            'format': format
        }

        response = self._get(path=path, params=params)
        try:
            return response.json()[endpoint]
        except:
            print(response.text)
            raise


    def base_function(self, endpoint, key):
        @parse(key)
        def _sub(geocode, language='en-US', units='e', format='json'):
            path = [self.version, self.api, endpoint]
            params = {
                'apiKey': self.api_key,
                'geocode': geocode,
                'units': units,
                'language': language,
                'format': format
            }
            response = self._get(path=path, params=params)
            try:
                return response.json()[endpoint]
            except:
                print(response.text)
                raise
        return _sub


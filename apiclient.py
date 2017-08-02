from baseclient import BaseClient
from utils import parse


class ApiClient(BaseClient):
    def __init__(self, api_key, protocol=None, url=None):
        self.protocol = 'https'
        self.version = 'v2'
        self.api = 'turbo'
        self.url = 'api.weather.com'
        self.api_key = api_key

    def get_past_pollen(self, geocode, pollenDays, pollenStartDate,
                        language='en-US', format='json'):
        return self.base_function(
            'vt1pastPollen', 'weed'
        )(geocode, pollenDays=str(pollenDays),
          pollenStartDate=str(pollenStartDate), language=language,
          format=format)

    def get_precipitation(self, geocode, language='en-US',
                          units='e', format='json'):
        return self.base_function(
            'vt1precipitation', 'startTime'
        )(geocode, language=language, units=units, format=format)

    def get_forecast(self, geocode, language='en-US', units='e', format='json'):
        return self.base_function(
            'vt1dailyForecast', 'sunrise'
        )(geocode, language=language, units=units, format=format)

    def get_fifteen(self, geocode, language='en-US', units='e', format='json'):
        return self.base_function(
            'vt1fifteenminute', 'icon'
        )(geocode, language=language, units=units, format=format)

    def get_hourly(self, geocode, language='en-US', units='e', format='json'):
        return self.base_function(
            'vt1hourlyForecast', 'icon'
        )(geocode, language=language, units=units, format=format)

    def get_observation(self, geocode, language='en-US',
                        units='e', format='json'):
        return self.base_function(
            'vt1observation'
        )(geocode, language=language, units=units, format=format)

    def get_pollen(self, geocode, language='en-US', format='json'):
        return self.base_function(
            'vt1pollenforecast', 'weed'
        )(geocode, language=language, format=format)

    def get_sick(self, geocode, format='json'):
        return self.base_function(
            'vt1sickWeatherMarkerCount'
        )(geocode, format=format)

    def pollen_observation(self, geocode, language='en-US', format='json'):
        return self.base_function(
            'vt1pollenobs'
        )(geocode, language=language, format=format)

    def pollen_day_part(self, geocode, language='en-US', format='json'):
        return self.base_function(
            'vt1idxPollenDayPart', 'day', 'num'
        )(geocode, language=language, format=format)

    def breathing_day_part(self, geocode, language='en-US', format='json'):
        return self.base_function(
            'vt1idxBreathingDaypart', 'day', 'num'
        )(geocode, language=language, format=format)

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

    def base_function(self, endpoint, *keys):
        @parse(keys)
        def _sub(geocode, **kwargs):
            path = [self.version, self.api, endpoint]
            params = {
                'apiKey': self.api_key,
                'geocode': geocode,
            }
            params.update(kwargs)
            response = self._get(
                path=path,
                params={k: v for k, v in params.items() if v is not None}
            )
            try:
                return response.json()[endpoint]
            except:
                print(response.text)
                raise
        return _sub

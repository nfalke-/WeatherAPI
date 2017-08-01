import requests

class BaseClient:
    def _get(self, path=None, params=None):
        base = self.protocol+'://'+self.url
        url = '/'.join([base] + path)
        return requests.get(url, params)

import logging
import requests
import os

logging.basicConfig()
log = logging.getLogger(__name__)

class TroveAPI(object):
    """
    A generic client for Trove API
    """
    def __init__(self, host, credentials=None):
        self.base_url = "http://%s" % host
        self.credentials = credentials

    def _get(self, path, params={}, key=None):
        """Args: key (str) result dict value to return"""
        path = os.path.join(self.base_url, path)
        jresult = requests.get(path, params=params)
        result = jresult.json()
        return self._unpack(key, result, path) if key else result

    def _unpack(self, key, result, path):
        """
        Unpack the actual return object
        args : key (str) The dict key found in the result
               result (dict) The raw trove-api result dict.
        """
        status = result and result.get('status')
        if type(status) == dict and status.get('code') == 200:
            return key and result.get(key)
        else:
            log.warn('Trove API return status %s for path %s', status, path)
            return None

    def get_channels_result(self, channel_id, limit=None, _unpack=True):
        path = "channels/%s/result" % channel_id
        key = 'result'
        params = dict(limit=limit)
        return self._get(path, params, key=_unpack and key)




import functools
from . import utility as UTIL


class ProviderConfig:

    def __init__(self, env_var_name, client_factory):
        self.env_var_name = env_var_name
        self._api_key = None
        self._client_factory = client_factory

    @property
    def api_key(self):
        return self._api_key

    def is_configured(self):
        return self._api_key is not None

    def register_api_key(self, apikey):
        self._api_key = apikey

    def opt_register(self):
        UTIL.lookup_register(self.env_var_name, self.register_api_key, missingokay=True)

    def register_key_from_environment(self):
        UTIL.lookup_register(self.env_var_name, self.register_api_key)

    @functools.lru_cache(maxsize=1)
    def get_client(self):
        assert self._api_key is not None, f"You must register an API key before calling"
        return self._client_factory(self._api_key)

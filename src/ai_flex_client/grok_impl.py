
import os
import json
import functools

from . import utility as UTIL
from . import anthro_impl as ANTHRO
from .base_query import BaseQuery
from .data_wrapper import DataWrapper



GROK_41_FAST_NO_REASON = "grok-4-1-fast-non-reasoning"

GROK_41_FAST_REASONING = "grok-4-1-fast-reasoning"


IMPL_API_KEY = None

ENVIRON_VAR_NAME = "GROK_API_KEY"

def is_configured():
    return IMPL_API_KEY != None

def register_api_key(apikey):
    global IMPL_API_KEY
    IMPL_API_KEY = apikey


def register_key_from_environment():
    UTIL.lookup_register(ENVIRON_VAR_NAME, register_api_key)


def opt_register():
    UTIL.lookup_register(ENVIRON_VAR_NAME, register_api_key, missingokay=True)


@functools.lru_cache(maxsize=1)
def get_client():
    import anthropic
    return anthropic.Client(api_key=IMPL_API_KEY, base_url="https://api.x.ai")


def build_query():
    return GrokQuery()



# Grok's API is compatible with Anthropic's, so we use the Anthro library
class GrokQuery(ANTHRO.AnthroQuery):

    def __init__(self):

        super().__init__()
        self.model_code = GROK_41_FAST_NO_REASON
        self.max_token = 8192


    def set_small_tier(self):
        self.model_code = GROK_41_FAST_NO_REASON
        return self

    def set_medium_tier(self):
        self.model_code = GROK_41_FAST_REASONING
        return self


    def get_wrapper_builder(self):
        return GrokWrapper


    def _sub_run_query(self):

        return get_client().messages.create(
            model=self.model_code,
            max_tokens=self.max_token,
            messages=self.messages # type: ignore[arg-type]
        )



class GrokWrapper(ANTHRO.AnthroWrapper):


    # https://docs.x.ai/docs/models
    def get_cost_pair(self, modelcode):

        if modelcode == GROK_41_FAST_REASONING:
            return (0.2, 0.5)

        if modelcode == GROK_41_FAST_NO_REASON:
            return (0.2, 0.5)

        assert False, f"No cost info available for modelcode {modelcode}"

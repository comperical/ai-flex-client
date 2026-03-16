
import os
import json
import functools

from . import utility as UTIL
from . import openai_impl as OAI

IMPL_API_KEY = None

ENVIRON_VAR_NAME = "VENICE_API_KEY"

VENICE_UNCENSORED = "venice-uncensored"

GLM_47 = "zai-org-glm-4.7"

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
    from openai import OpenAI
    assert IMPL_API_KEY != None, f"You must register an API key before calling"
    return OpenAI(api_key=IMPL_API_KEY, base_url="https://api.venice.ai/api/v1")


def build_query():
    return VeniceQuery()


class VeniceQuery(OAI.OaiQuery):

    def __init__(self):
        super().__init__()
        self.max_token = 8192

        self.set_small_tier()


    def set_small_tier(self):
        self.model_code = VENICE_UNCENSORED
        return self


    def set_medium_tier(self):
        self.model_code = GLM_47
        return self

    def get_wrapper_builder(self):
        return VeniceWrapper


    def _sub_run_query(self):

        assert self.messages is not None, "You must initialize messages"

        return get_client().chat.completions.create(
            model=self.model_code,
            messages=self.messages, # type: ignore[arg-type]
            max_completion_tokens=self.max_token
        )



class VeniceWrapper(OAI.OaiWrapper):


    # https://docs.venice.ai/models/overview
    def get_cost_pair(self, modelcode):

        if modelcode == GLM_47:
            return (0.55, 2.65)

        if modelcode == VENICE_UNCENSORED:
            return (0.2, 0.9)

        return None



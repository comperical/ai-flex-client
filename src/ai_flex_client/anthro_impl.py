
import os
import json
import functools

from . import utility as UTIL
from .base_query import BaseQuery
from .data_wrapper import DataWrapper

SONNET_MODEL_CODE = "claude-sonnet-4-5-20250929"

HAIKU_MODEL_CODE = "claude-haiku-4-5-20251001"

IMPL_API_KEY = None

ENVIRON_VAR_NAME = "ANTHRO_API_KEY"

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
    return anthropic.Client(api_key=IMPL_API_KEY)


def build_query():
    return AnthroQuery()



class AnthroQuery(BaseQuery):

    def __init__(self):

        super().__init__()
        self.model_code = HAIKU_MODEL_CODE
        self.max_token = 8192

    def normalize_response(self, response):
        return json.loads(response.model_dump_json())


    def set_small_tier(self):
        self.model_code = HAIKU_MODEL_CODE
        return self

    def set_medium_tier(self):
        self.model_code = SONNET_MODEL_CODE
        return self


    def get_wrapper_builder(self):
        return AnthroWrapper

    def _sub_run_query(self):

        return get_client().messages.create(
            model=self.model_code,
            max_tokens=self.max_token,
            messages=self.messages # type: ignore[arg-type]
        )




class AnthroWrapper(DataWrapper):


    def get_basic_text(self):
        return self.normal_form["content"][0]["text"]

    def compose_basic_metadata(self):

        return {
            'message_id' : self.normal_form['id'],
            'model_family' : 'claude',
            'model_code' : self.normal_form['model'],
            'input_tokens' : self.normal_form['usage']['input_tokens'],
            'output_tokens' : self.normal_form['usage']['output_tokens']
        }


    # https://www.anthropic.com/pricing
    # https://docs.claude.com/en/docs/about-claude/pricing
    def get_cost_pair(self, modelcode):

        if modelcode.startswith("claude-sonnet-4-5") or modelcode.startswith("claude-sonnet-4-6"):
            return (3, 6)

        if modelcode.startswith("claude-3-7-sonnet") or modelcode.startswith("claude-3-5-sonnet"):
            return (3, 6)

        if modelcode.startswith("claude-haiku-4-5"):
            return (1, 2)

        if modelcode.startswith("claude-3-5-haiku"):
            return (0.8, 1.6)


        assert False, f"No cost info available for modelcode {modelcode}"

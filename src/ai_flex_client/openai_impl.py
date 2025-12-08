
import os
import json
import functools

from . import utility as UTIL
from .base_query import BaseQuery
from .data_wrapper import DataWrapper

GPT_4O = "gpt-4o"

GPT4O_MINI = "gpt-4o-mini"

GPT_5 = "gpt-5-2025-08-07"

GPT_5_MINI = "gpt-5-mini"

IMPL_API_KEY = None

ENVIRON_VAR_NAME = "OPENAI_API_KEY"

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
    return OpenAI(api_key=IMPL_API_KEY)


def build_query():
    return OaiQuery()


class OaiQuery(BaseQuery):

    def __init__(self):
        super().__init__()
        self.max_token = 8192

        self.set_small_tier()

    def run_get_data(self):
        self.od_run_query()
        return self.get_data_wrapper()


    def normalize_response(self, response):
        return response.to_dict()


    def set_small_tier(self):
        self.model_code = GPT_5_MINI
        return self


    def set_medium_tier(self):
        self.model_code = GPT_5
        return self


    def get_wrapper_builder(self):
        return OaiWrapper


    def _sub_run_query(self):

        assert self.messages is not None, "You must initialize messages"

        return get_client().chat.completions.create(
            model=self.model_code,
            messages=self.messages, # type: ignore[arg-type]
            max_completion_tokens=self.max_token
        )



class OaiWrapper(DataWrapper):


    def get_basic_text(self):
        return self.normal_form["choices"][0]["message"]["content"]


    # https://openai.com/api/pricing/
    def get_cost_pair(self, modelcode):

        if modelcode.startswith(GPT4O_MINI):
            return (0.15, 0.6)

        if modelcode.startswith(GPT_4O):
            return (2.5, 10)

        if modelcode.startswith(GPT_5_MINI):
            return (0.25, 2)

        assert False, f"No cost info available for modelcode {modelcode}"


    def compose_basic_metadata(self):

        usage = self.normal_form['usage']

        return {
            'message_id' : self.normal_form['id'],
            'model_family' : 'gpt',
            'model_code' : self.normal_form['model'],
            'input_tokens' : usage['prompt_tokens'],
            'output_tokens' : usage['completion_tokens']
        }


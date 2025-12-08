

import os
import json
import functools

from . import utility as UTIL
from .base_query import BaseQuery
from .data_wrapper import DataWrapper


from . import openai_impl as OAI_IMPL

GPT_OSS_120B = "hf:openai/gpt-oss-120b"

META_LLAMA_70B_INSTRUCT = "hf:meta-llama/Llama-3.3-70B-Instruct"

IMPL_API_KEY = None

ENVIRON_VAR_NAME = "SYNTHETIC_API_KEY"


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
    return OpenAI(api_key=IMPL_API_KEY, base_url="https://api.synthetic.new/v1")


def build_query():
    return SyntheticQuery()


class SyntheticQuery(OAI_IMPL.OaiQuery):

    def __init__(self):
        super().__init__()

        self.model_code = GPT_OSS_120B


    def get_wrapper_builder(self):
        return SyntheticWrapper



    def _sub_run_query(self):

        assert self.model_code.startswith("hf:"), f"Expected to see hf:/ prefix here"
        client = get_client()

        assert self.messages != None
        return client.chat.completions.create(
            model=self.model_code,
            messages=self.messages  # type: ignore[arg-type]
        )



class SyntheticWrapper(OAI_IMPL.OaiWrapper):


    # https://synthetic.new/pricing
    def get_cost_pair(self, modelcode):


        if "llama-v3p3" in modelcode:
            return (0.90, 0.90)

        if "gpt-oss-120b" in modelcode:
            return (0.10, 0.10)

        assert False, f"No cost info available for SYNTHETIC modelcode {modelcode}"




import os
import json
import functools

from . import utility as UTIL
from .base_query import BaseQuery
from .data_wrapper import DataWrapper


from . import openai_impl as OAI_IMPL

GPT_OSS_120B = "hf:openai/gpt-oss-120b"

META_LLAMA_70B_INSTRUCT = "hf:meta-llama/Llama-3.3-70B-Instruct"

SYNTH_API_KEY = None

def is_configured():
    return SYNTH_API_KEY != None


def register_api_key(apikey):
    global SYNTH_API_KEY
    SYNTH_API_KEY = apikey


def register_key_from_environment():
    envkey = os.environ.get("SYNTH_API_KEY", None)
    assert envkey != None, f"You must set the environment variable SYNTH_API_KEY"
    register_api_key(envkey)


@functools.lru_cache(maxsize=1)
def get_client():
    from openai import OpenAI
    return OpenAI(api_key=SYNTH_API_KEY, base_url="https://api.synthetic.new/v1")


def build_query():
    return SyntheticQuery()


class SyntheticQuery(OAI_IMPL.OaiQuery):

    def __init__(self):
        super().__init__()
        self.model_code = GPT_OSS_120B


    def get_data_wrapper(self):
        rjson = self.get_response_json()
        assert rjson != None, "You must either run the query, or load from DB"
        return SyntheticWrapper(json.loads(rjson))



    def _sub_run_query(self):

        assert self.model_code.startswith("hf:"), f"Expected to see hf:/ prefix here"
        client = get_client()

        assert self.messages != None
        return client.chat.completions.create(
            model=self.model_code,
            messages=self.messages  # type: ignore[arg-type]
        )



class SyntheticWrapper(OAI_IMPL.OaiWrapper):


    def __init__(self, rjson):
        super().__init__(rjson)


    # https://synthetic.new/pricing
    def get_cost_pair(self, modelcode):


        if "llama-v3p3" in modelcode:
            return (0.90, 0.90)

        if "gpt-oss-120b" in modelcode:
            return (0.10, 0.10)

        assert False, f"No cost info available for SYNTHETIC modelcode {modelcode}"


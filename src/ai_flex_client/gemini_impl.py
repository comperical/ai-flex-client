

import os
import json
import functools

from . import utility as UTIL
from .base_query import BaseQuery
from .data_wrapper import DataWrapper


GEMINI_25_FLASH = "gemini-2.5-flash"

GEMINI_25_PRO = "gemini-2.5-pro"

IMPL_API_KEY = None

ENVIRON_VAR_NAME = "GEMINI_API_KEY"

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

    import asyncio
    from google import genai

    # Issue here is that genai wants to do asyncio, but
    # Flask does not allow this by default. So we have to do some
    # incantations to get it to run in the Flask app
    try:
        return genai.Client(api_key=IMPL_API_KEY)
    except RuntimeError as e:
        if "no current event loop" in str(e).lower():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return genai.Client(api_key=IMPL_API_KEY)
        raise  # If another error occurs, re-raise it



def build_query():
    return GeminiQuery()



class GeminiQuery(BaseQuery):

    def __init__(self):
        super().__init__(GeminiWrapper)
        self.model_code = GEMINI_25_FLASH


    def convert_response2_json(self):
        assert self.response != None, "Response is null, you must generate it first or check before calling here"
        return self.response.model_dump_json()


    def normalize_response(self, response):
        return json.loads(response.model_dump_json())

    def set_small_tier(self):
        self.model_code = GEMINI_25_FLASH
        return self


    def set_medium_tier(self):
        self.model_code = GEMINI_25_PRO
        return self

    def run_get_data(self):
        self.od_run_query()
        return self.get_data_wrapper()


    def _sub_run_query(self):

        # Annoying issue here where Gemini can only handle a single message
        assert self.messages != None and len(self.messages) == 1, "Currently Gemini can only handle single outbound message"
        singlemssg = self.messages[0]['content']

        return get_client().models.generate_content(
            model=self.model_code,
            contents=singlemssg
        )


class GeminiWrapper(DataWrapper):

    def get_basic_text(self):

        #print(json.dumps(firstcand['content']['parts'][0]['text'], indent=4, sort_keys=True))

        candlist = self.normal_form['candidates']
        firstcand = candlist[0]
        return firstcand['content']['parts'][0]['text']


    def compose_basic_metadata(self):

        usage = self.normal_form['usage_metadata']

        return {
            'message_id' : None,
            'model_family' : 'gemini',
            'model_code' : self.normal_form['model_version'],
            'input_tokens' : usage['prompt_token_count'],
            'output_tokens' : usage['candidates_token_count']
        }


    # https://ai.google.dev/gemini-api/docs/pricing
    def get_cost_pair(self, modelcode):

        if modelcode.startswith(GEMINI_25_FLASH):
            return (0.10, 0.4)

        if modelcode.startswith(GEMINI_25_PRO):
            return (1.25, 10)

        assert False, f"No cost info available for modelcode {modelcode}"
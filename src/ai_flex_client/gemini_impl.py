

import json

from .base_query import BaseQuery
from .data_wrapper import DataWrapper
from .model_name import ModelName
from .provider_config import ProviderConfig


def _make_client(api_key):
    import asyncio
    from google import genai

    # genai wants asyncio, but Flask does not allow this by default
    try:
        return genai.Client(api_key=api_key)
    except RuntimeError as e:
        if "no current event loop" in str(e).lower():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return genai.Client(api_key=api_key)
        raise


CONFIG = ProviderConfig("GEMINI_API_KEY", _make_client)

is_configured = CONFIG.is_configured
opt_register = CONFIG.opt_register
register_api_key = CONFIG.register_api_key


class LlmQuery(BaseQuery):

    _small_model = ModelName.GEMINI_2_5_FLASH
    _medium_model = ModelName.GEMINI_2_5_PRO

    def __init__(self):
        super().__init__()
        self.set_small_tier()

    def normalize_response(self, response):
        return json.loads(response.model_dump_json())

    def get_wrapper_builder(self):
        return LlmResponseWrapper

    def _sub_run_query(self):
        assert self.messages is not None and len(self.messages) == 1, \
            "Currently Gemini can only handle single outbound message"
        singlemssg = self.messages[0]['content']
        return CONFIG.get_client().models.generate_content(
            model=self.model_code,
            contents=singlemssg
        )


class LlmResponseWrapper(DataWrapper):

    def get_basic_text(self):
        return self.normal_form['candidates'][0]['content']['parts'][0]['text']

    def compose_basic_metadata(self):
        usage = self.normal_form['usage_metadata']
        return {
            'message_id' : None,
            'model_family' : 'gemini',
            'model_code' : self.normal_form['model_version'],
            'input_tokens' : usage['prompt_token_count'],
            'output_tokens' : usage['candidates_token_count']
        }

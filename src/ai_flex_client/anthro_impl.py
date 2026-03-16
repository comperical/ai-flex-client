

import json

from .base_query import BaseQuery
from .data_wrapper import DataWrapper
from .model_name import ModelName
from .provider_config import ProviderConfig


def _make_client(api_key):
    import anthropic
    return anthropic.Client(api_key=api_key)


CONFIG = ProviderConfig("ANTHRO_API_KEY", _make_client)

is_configured = CONFIG.is_configured
opt_register = CONFIG.opt_register
register_api_key = CONFIG.register_api_key


class LlmQuery(BaseQuery):

    _small_model = ModelName.CLAUDE_HAIKU_4_5
    _medium_model = ModelName.CLAUDE_SONNET_4_5

    def __init__(self):
        super().__init__()
        self.model_code = self._small_model.code
        self.max_token = 8192

    def normalize_response(self, response):
        return json.loads(response.model_dump_json())

    def get_wrapper_builder(self):
        return LlmResponseWrapper

    def _sub_run_query(self):
        return CONFIG.get_client().messages.create(
            model=self.model_code,
            max_tokens=self.max_token,
            messages=self.messages
        )


class LlmResponseWrapper(DataWrapper):

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

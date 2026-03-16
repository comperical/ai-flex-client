

from .base_query import BaseQuery
from .data_wrapper import DataWrapper
from .model_name import ModelName
from .provider_config import ProviderConfig


def _make_client(api_key):
    from openai import OpenAI
    return OpenAI(api_key=api_key)


CONFIG = ProviderConfig("OPENAI_API_KEY", _make_client)

# Module-level API for backwards compatibility
is_configured = CONFIG.is_configured
opt_register = CONFIG.opt_register
register_api_key = CONFIG.register_api_key


def build_query():
    return OaiQuery()


class OaiQuery(BaseQuery):

    _small_model = ModelName.GPT_5_MINI
    _medium_model = ModelName.GPT_5

    def __init__(self):
        super().__init__()
        self.max_token = 8192
        self.set_small_tier()

    def normalize_response(self, response):
        return response.to_dict()

    def get_wrapper_builder(self):
        return OaiWrapper

    def _sub_run_query(self):
        assert self.messages is not None, "You must initialize messages"
        return CONFIG.get_client().chat.completions.create(
            model=self.model_code,
            messages=self.messages,
            max_completion_tokens=self.max_token
        )


class OaiWrapper(DataWrapper):

    def get_basic_text(self):
        return self.normal_form["choices"][0]["message"]["content"]

    def compose_basic_metadata(self):
        usage = self.normal_form['usage']
        return {
            'message_id' : self.normal_form['id'],
            'model_family' : 'gpt',
            'model_code' : self.normal_form['model'],
            'input_tokens' : usage['prompt_tokens'],
            'output_tokens' : usage['completion_tokens']
        }

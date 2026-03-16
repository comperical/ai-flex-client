

from . import openai_impl as OAI
from .model_name import ModelName
from .provider_config import ProviderConfig


def _make_client(api_key):
    from openai import OpenAI
    return OpenAI(api_key=api_key, base_url="https://api.venice.ai/api/v1")


CONFIG = ProviderConfig("VENICE_API_KEY", _make_client)

is_configured = CONFIG.is_configured
opt_register = CONFIG.opt_register
register_api_key = CONFIG.register_api_key


class LlmQuery(OAI.LlmQuery):

    _small_model = ModelName.VENICE_UNCENSORED
    _medium_model = ModelName.GLM_4_7

    def get_wrapper_builder(self):
        return OAI.LlmResponseWrapper

    def _sub_run_query(self):
        assert self.messages is not None, "You must initialize messages"
        return CONFIG.get_client().chat.completions.create(
            model=self.model_code,
            messages=self.messages,
            max_completion_tokens=self.max_token
        )

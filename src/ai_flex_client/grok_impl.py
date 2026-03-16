

from . import anthro_impl as ANTHRO
from .model_name import ModelName
from .provider_config import ProviderConfig


def _make_client(api_key):
    import anthropic
    return anthropic.Client(api_key=api_key, base_url="https://api.x.ai")


CONFIG = ProviderConfig("GROK_API_KEY", _make_client)

is_configured = CONFIG.is_configured
opt_register = CONFIG.opt_register
register_api_key = CONFIG.register_api_key


def build_query():
    return GrokQuery()


class GrokQuery(ANTHRO.AnthroQuery):

    _small_model = ModelName.GROK_4_1_FAST
    _medium_model = ModelName.GROK_4_1_FAST_REASONING

    def get_wrapper_builder(self):
        return ANTHRO.AnthroWrapper

    def _sub_run_query(self):
        return CONFIG.get_client().messages.create(
            model=self.model_code,
            max_tokens=self.max_token,
            messages=self.messages
        )

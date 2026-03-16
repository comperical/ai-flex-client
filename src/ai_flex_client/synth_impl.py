

from . import openai_impl as OAI
from .model_name import ModelName
from .provider_config import ProviderConfig


def _make_client(api_key):
    from openai import OpenAI
    return OpenAI(api_key=api_key, base_url="https://api.synthetic.new/v1")


CONFIG = ProviderConfig("SYNTHETIC_API_KEY", _make_client)

is_configured = CONFIG.is_configured
opt_register = CONFIG.opt_register
register_api_key = CONFIG.register_api_key


def build_query():
    return SyntheticQuery()


class SyntheticQuery(OAI.OaiQuery):

    _small_model = ModelName.GPT_OSS_120B

    def get_wrapper_builder(self):
        return OAI.OaiWrapper

    def _sub_run_query(self):
        assert self.model_code.startswith("hf:"), f"Expected to see hf:/ prefix here"
        assert self.messages is not None
        return CONFIG.get_client().chat.completions.create(
            model=self.model_code,
            messages=self.messages
        )


import json
from typing import Any

from . import utility as UTIL


class DataWrapper:

    def __init__(self, normal):
        assert type(normal) == dict, f"Expected JSON data in dictionary form"
        self.normal_form = normal


    def get_basic_text(self):
        assert False, "Subclasses must override"


    def get_standard_metadata(self):
        assert False, "Subclasses must override"


    def get_cost_dollar(self):
        metadata = self.compose_standard_metadata()
        return metadata['cost_dollar']


    def compose_basic_metadata(self) -> dict[str, Any]:
        assert False, "Subclasses must override"


    def _compute_cost_dollar(self, usage):

        registry = UTIL.get_registry()
        model_info = registry.lookup_model(usage['model_code'])
        if model_info is None:
            return None

        if model_info.input_price is None or model_info.output_price is None:
            return None

        itoken = usage['input_tokens'] / 1_000_000
        otoken = usage['output_tokens'] / 1_000_000
        return model_info.input_price * itoken + model_info.output_price * otoken


    def get_cost_dollar(self):
        basicdata = self.compose_standard_metadata()
        return basicdata['cost_dollar']

    # Compile the response metadata (tokens, model code, etc)
    # into a standard form that will work for all API endpoints
    # this does not include cost, but you can compute cost from it
    # TODO: probably want a dataclass here
    def compose_standard_metadata(self):

        usage = self.compose_basic_metadata()

        usage['cost_dollar'] = self._compute_cost_dollar(usage)

        return usage





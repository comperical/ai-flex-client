

import json


class ModelRegistry:

    def __init__(self, json_path):
        with open(json_path) as f:
            self._data = json.load(f)

    def providers(self):
        return list(self._data.keys())

    def model_codes(self, provider):
        return list(self._data[provider].keys())

    def all_model_codes(self):
        return [
            (provider, code)
            for provider in self._data
            for code in self._data[provider]
        ]

    def get_pricing(self, provider, model_code):
        return self._data[provider][model_code]

    def get_input_price(self, provider, model_code):
        return self._data[provider][model_code]["input_price"]

    def get_output_price(self, provider, model_code):
        return self._data[provider][model_code]["output_price"]

    def get_display(self, provider, model_code):
        return self._data[provider][model_code]["display"]

    def lookup_model(self, model_code):
        for provider, models in self._data.items():
            if model_code in models:
                return provider, models[model_code]
        return None

    def lookup_by_enum_name(self, enum_name):
        for provider, models in self._data.items():
            for code, info in models.items():
                if info.get("enum_name") == enum_name:
                    return code
        assert False, f"No model found with enum_name '{enum_name}'"




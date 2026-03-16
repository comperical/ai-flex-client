

import json
from typing import NamedTuple, Optional


class ModelInfo(NamedTuple):
    provider: str
    model_code: str
    enum_name: str
    display: str
    input_price: Optional[float]
    output_price: Optional[float]


class ModelRegistry:

    def __init__(self, json_path):
        with open(json_path) as f:
            raw = json.load(f)

        self._models = []
        for provider, models in raw.items():
            for code, info in models.items():
                self._models.append(ModelInfo(
                    provider=provider,
                    model_code=code,
                    enum_name=info["enum_name"],
                    display=info["display"],
                    input_price=info.get("input_price"),
                    output_price=info.get("output_price"),
                ))

    def all_models(self):
        return list(self._models)

    def lookup_model(self, model_code):

        # Exact match first
        for m in self._models:
            if m.model_code == model_code:
                return m

        # Prefix fallback: find the longest key that is a prefix of the query
        candidates = [m for m in self._models if model_code.startswith(m.model_code)]

        if not candidates:
            return None

        return max(candidates, key=lambda m: len(m.model_code))

    def lookup_by_enum_name(self, enum_name):
        for m in self._models:
            if m.enum_name == enum_name:
                return m.model_code
        assert False, f"No model found with enum_name '{enum_name}'"

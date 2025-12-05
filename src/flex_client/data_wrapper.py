
import json
import utility as UTIL
from typing import Any


class DataWrapper:

    def __init__(self, rjson):
        assert type(rjson) == dict, f"Expected JSON data in dictionary form"
        self.responsejson = rjson


    def get_basic_text(self):
        assert False, "Subclasses must override"


    def get_standard_metadata(self):
        assert False, "Subclasses must override"


    def get_cost_dollar(self):
        metadata = self.compose_standard_metadata()
        return metadata['cost_dollar']


    def compose_basic_metadata(self) -> dict[str, Any]:
        assert False, "Subclasses must override"


    def get_cost_pair(self, modelcode) -> tuple[float, float]:
        assert False, "Subclasses must override"


    def compute_cost_dollar(self, usage):
        icost, ocost = self.get_cost_pair(usage['model_code'])
        itoken = usage['input_tokens'] / 1_000_000
        otoken = usage['output_tokens'] / 1_000_000
        return icost * itoken + ocost * otoken


    # Compile the response metadata (tokens, model code, etc)
    # into a standard form that will work for all API endpoints
    # this does not include cost, but you can compute cost from it
    # TODO: probably want a dataclass here
    def compose_standard_metadata(self):

        usage = self.compose_basic_metadata()

        usage['cost_dollar'] = self.compute_cost_dollar(usage)

        return usage






class OaiWrapper(ApiDataWrapper):


    def __init__(self, rjson):
        super().__init__(rjson)


    def get_basic_text(self):
        return self.responsejson["choices"][0]["message"]["content"]


    # https://openai.com/api/pricing/
    def get_cost_pair(self, modelcode):

        if modelcode.startswith(UTIL.GPT4O_MINI):
            return (0.15, 0.6)


        if modelcode.startswith(UTIL.GPT_4O):
            return (2.5, 10)

        if modelcode.startswith(UTIL.GPT_5_MINI):
            return (0.25, 2)

        assert False, f"No cost info available for modelcode {modelcode}"




    def compose_basic_metadata(self):

        usage = self.responsejson['usage']

        return {
            'message_id' : self.responsejson['id'],
            'model_family' : 'gpt',
            'model_code' : self.responsejson['model'],
            'input_tokens' : usage['prompt_tokens'],
            'output_tokens' : usage['completion_tokens']
        }


class SyntheticWrapper(OaiWrapper):


    def __init__(self, rjson):
        super().__init__(rjson)


    # https://synthetic.new/pricing
    def get_cost_pair(self, modelcode):


        if "llama-v3p3" in modelcode:
            return (0.90, 0.90)

        if "gpt-oss-120b" in modelcode:
            return (0.10, 0.10)

        assert False, f"No cost info available for SYNTHETIC modelcode {modelcode}"




class GeminiWrapper(ApiDataWrapper):


    def __init__(self, rjson):
        super().__init__(rjson)


    def get_basic_text(self):

        #print(json.dumps(firstcand['content']['parts'][0]['text'], indent=4, sort_keys=True))

        candlist = self.responsejson['candidates']
        firstcand = candlist[0]
        return firstcand['content']['parts'][0]['text']


    def compose_basic_metadata(self):

        usage = self.responsejson['usage_metadata']

        return {
            'message_id' : None,
            'model_family' : 'gemini',
            'model_code' : self.responsejson['model_version'],
            'input_tokens' : usage['prompt_token_count'],
            'output_tokens' : usage['candidates_token_count']
        }


    # https://ai.google.dev/gemini-api/docs/pricing
    def get_cost_pair(self, modelcode):

        if modelcode.startswith(UTIL.GEMINI_20_FLASH):
            return (0.10, 0.4)

        if modelcode.startswith(UTIL.GEMINI_25_PRO):
            return (1.25, 10)

        assert False, f"No cost info available for modelcode {modelcode}"



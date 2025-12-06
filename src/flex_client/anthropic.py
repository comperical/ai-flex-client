

class AnthroQuery(BaseQuery):

    def __init__(self):

        super().__init__()
        self.model_code = UTIL.HAIKU_MODEL_CODE
        self.max_token = 8192

    def convert_response2_json(self):
        assert self.response != None, "Response is null, you must generate it first or check before calling here"
        return self.response.model_dump_json()


    def set_small_tier(self):
        self.model_code = UTIL.HAIKU_MODEL_CODE
        return self

    def set_medium_tier(self):
        self.model_code = UTIL.SONNET_MODEL_CODE
        return self

    def get_data_wrapper(self):
        rjson = self.get_response_json()
        assert rjson != None, "You must either run the query, or load from DB"
        return WRAPPER.AnthroWrapper(json.loads(rjson))

    def _sub_run_query(self):

        return UTIL.get_anthro_client().messages.create(
            model=self.model_code,
            max_tokens=self.max_token,
            messages=self.messages # type: ignore[arg-type]
        )




class AnthroWrapper(DataWrapper):


    def __init__(self, rjson):
        super().__init__(rjson)


    def get_basic_text(self):
        return self.responsejson["content"][0]["text"]

    def compose_basic_metadata(self):

        return {
            'message_id' : self.responsejson['id'],
            'model_family' : 'claude',
            'model_code' : self.responsejson['model'],
            'input_tokens' : self.responsejson['usage']['input_tokens'],
            'output_tokens' : self.responsejson['usage']['output_tokens']
        }


    # https://www.anthropic.com/pricing
    # https://docs.claude.com/en/docs/about-claude/pricing
    def get_cost_pair(self, modelcode):

        if modelcode.startswith("claude-sonnet-4-5"):
            return (3, 6)

        if modelcode.startswith("claude-3-7-sonnet") or modelcode.startswith("claude-3-5-sonnet"):
            return (3, 6)

        if modelcode.startswith("claude-haiku-4-5"):
            return (1, 2)

        if modelcode.startswith("claude-3-5-haiku"):
            return (0.8, 1.6)


        assert False, f"No cost info available for modelcode {modelcode}"

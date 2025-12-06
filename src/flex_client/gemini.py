

class GeminiQuery(GaiQuery):

    def __init__(self):
        super().__init__()
        self.model_code = UTIL.GEMINI_20_FLASH


    def convert_response2_json(self):
        assert self.response != None, "Response is null, you must generate it first or check before calling here"
        return self.response.model_dump_json()


    def run_get_data(self):
        self.od_run_query()
        return self.get_data_wrapper()

    def get_data_wrapper(self):
        rjson = self.get_response_json()
        assert rjson != None, "You must either run the query, or load from DB"
        return WRAPPER.GeminiWrapper(json.loads(rjson))

    def _sub_run_query(self):

        # Annoying issue here where Gemini can only handle a single message
        assert self.messages != None and len(self.messages) == 1, "Currently Gemini can only handle single outbound message"
        singlemssg = self.messages[0]['content']

        return UTIL.get_gemini_client().models.generate_content(
            model=self.model_code,
            contents=singlemssg
        )

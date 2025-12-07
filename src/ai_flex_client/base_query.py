


import os
import sys
import json
from typing import Any

from . import utility as UTIL



class BaseQuery:

    def __init__(self):
        
        self.response = None

        self.messages = None

        self.model_code = None

        self.send_time_milli = None
        self.resp_time_milli = None



    def is_complete():
        return self.resp_time_milli is not None


    @staticmethod
    def load_from_db(queryid):
        dbrec = UTIL.lookup_record_direct("gai_query", queryid)
        return GaiQuery.load_from_dbrec(dbrec)


    @staticmethod
    def load_from_dbrec(dbrec):
        assert dbrec != None

        modelcode = dbrec['model_code']

        tool = None

        # Gotcha, the gpt-oss-120b both starts with hf: and has "gpt" in the name
        if modelcode.startswith("hf:"):
            tool = SyntheticQuery()
        else:
            if 'gpt' in modelcode:
                tool = OaiQuery()

            if 'claude' in modelcode:
                tool = AnthroQuery()

            if 'gemini' in modelcode:
                tool = GeminiQuery()

        assert tool != None, f"Invalid model code {modelcode}"

        tool.set_model_code(modelcode).set_simple_prompt(dbrec['full_prompt'])

        tool.db_record = dbrec

        return tool



    def set_model_code(self, modelcode):
        self.model_code = modelcode
        return self

    def set_small_tier(self) -> "BaseQuery":
        assert False, "Subclass must override"

    def set_medium_tier(self) -> "BaseQuery":
        assert False, "Subclass must override"

    def set_large_tier(self) -> "BaseQuery":
        assert False, "Subclass must override"

    def get_data_wrapper(self) -> "DataWrapper":
        assert False, "Subclass must override"


    def with_max_token(self, mt) -> "BaseQuery":
        assert False, "Subclass must override, probably only allow this for ANTHRO queries"
        return self


    def set_simple_prompt(self, theprompt):
        assert self.messages == None, "Messages were already set!!"
        self.messages = [{ "role" : "user", "content" : theprompt }]
        return self


    def get_response_json(self):

        if self.response != None:
            return self.convert_response2_json()

        return None



    # Okay, different library implementations from the GenAI providers
    # represent this JSON response in different ways
    # If you can't call to_json(),
    def convert_response2_json(self) -> str:
        assert False, "Subclasses must override to convert response object to JSON"

    def save_response2_db(self, queryid):

        LOGGER = self.__get_logger()
        alphatime = UTIL.curtime_milli()
        self.od_run_query()
        timesec = (UTIL.curtime_milli() - alphatime) / 1000
        LOGGER.info(f"Query {queryid} with builder {self.__class__.__name__}, model {self.model_code} took {timesec:.03f} seconds")


        with UTIL.get_work_conn() as conn:
            update = "UPDATE gai_query SET full_response = %s, sent_at_est = %s, resp_at_est = %s, total_cost = %s WHERE id = %s"
            responsejson = self.get_response_json()
            sentat = UTIL.iso_format_milli_est(self.send_time_milli)
            respat = UTIL.iso_format_milli_est(self.resp_time_milli)
            totalcost = self._get_total_cost()
            conn.execute(update, (responsejson, sentat, respat, totalcost, queryid))


    def _get_total_cost(self):

        wrapper = self.get_data_wrapper()
        return wrapper.compose_standard_metadata()['cost_dollar']



    def od_run_query(self):

        assert self.messages != None, "Message data must be ready at this stage!"

        self._configure_params()

        if self.response == None:
            self.send_time_milli = UTIL.curtime_milli()
            self.response = self._sub_run_query() # type: ignore[arg-type]
            self.resp_time_milli = UTIL.curtime_milli()



    def _configure_params(self):

        """
        source = json.loads(self.db_record['source_data'])

        if "max_token" in source:
            self.with_max_token(source["max_token"])

        """


    # This returns whatever the provider returns from a query
    def _sub_run_query(self) -> Any :
        assert False, "Subclasses must override!!"






"""
# This is a hosted service that apparently uses the same exact API as OpenAI
class SyntheticQuery(OaiQuery):

    def __init__(self):
        super().__init__()
        self.model_code = UTIL.META_LLAMA_70B_INSTRUCT


    def get_data_wrapper(self):
        rjson = self.get_response_json()
        assert rjson != None, "You must either run the query, or load from DB"
        return WRAPPER.SyntheticWrapper(json.loads(rjson))



    def _sub_run_query(self):

        assert self.model_code.startswith("hf:"), f"Expected to see hf:/ prefix here"
        client = UTIL.get_synthetic_client()

        assert self.messages != None
        return client.chat.completions.create(
            model=self.model_code,
            messages=self.messages  # type: ignore[arg-type]
        )
"""



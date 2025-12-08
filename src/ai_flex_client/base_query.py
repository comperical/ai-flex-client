


import os
import sys
import json
from typing import Any

from . import utility as UTIL



class BaseQuery:

    def __init__(self):
        

        # This is the JSON-ified form of the object returned by the endpoint
        # It is stripped of any of its original identity based on the particular library
        # It must be serializable with json.dumps(...)
        # (though clients may persist using native JSON datatypes)
        self.normal_form = None

        # Error code returned by the system
        self.error_info = None

        # These are the internal message objects
        # these are hashes with role : content records
        self.messages = []

        self.model_code = None

        self.send_time_milli = None
        self.resp_time_milli = None


    def is_complete(self):
        return self.resp_time_milli is not None

    def is_success(self):
        return self.is_complete() and self.error_info == None

    def set_model_code(self, modelcode):
        self.model_code = modelcode
        return self

    def get_normal_form(self):
        assert self.is_success(), f"This query has not completed successfully"
        return self.normal_form


    def set_small_tier(self) -> "BaseQuery":
        assert False, "Subclass must override"

    def set_medium_tier(self) -> "BaseQuery":
        assert False, "Subclass must override"

    def set_large_tier(self) -> "BaseQuery":
        assert False, "Subclass must override"

    def get_wrapper_builder(self):
        assert False, "Subclass must override"

    def get_data_wrapper(self) -> "DataWrapper":
        builder = self.get_wrapper_builder()
        normal = self.get_normal_form()
        assert normal != None, "Response is not ready, you must run request"
        return builder(normal)

    def with_max_token(self, mt) -> "BaseQuery":
        assert False, "Subclass must override, probably only allow this for ANTHRO queries"


    def set_simple_prompt(self, theprompt: str) -> "BaseQuery":
        assert len(self.messages) == 0, f"Only use this method to add a single content record"
        return self.add_message(role="user", content=theprompt)


    def add_message(self, *, role, content):
        self.messages.append({ "role" : role, "content" : content })
        return self


    # Transform the library response object into a "normal" Python object
    # The contract of this object is that 
    # json.load(json.dump(norm_ob)) == norm_ob
    # With the == implying "moral" equivalence, if not strict byte-level equivalence
    def normalize_response(self, response) -> dict:
        assert False, "Subclasses must override to convert response object to JSON"


    def _get_total_cost(self):

        wrapper = self.get_data_wrapper()
        return wrapper.compose_standard_metadata()['cost_dollar']



    def od_run_query(self):

        assert len(self.messages) > 0, "Message data must be ready at this stage!"

        self._configure_params()

        if self.normal_form == None:

            self.send_time_milli = UTIL.curtime_milli()
            response = self._sub_run_query() # type: ignore[arg-type]
            self.normal_form = self.normalize_response(response)
            self.resp_time_milli = UTIL.curtime_milli()
            assert type(self.normal_form) == dict, "Normal form of repsonse must be regular dict"

        # print(f"Response is {self.normal_form}, type is {type(self.normal_form)}")



    def _configure_params(self):

        """
        source = json.loads(self.db_record['source_data'])

        if "max_token" in source:
            self.with_max_token(source["max_token"])

        """
        pass


    # This returns whatever the provider returns from a query
    def _sub_run_query(self) -> Any :
        assert False, "Subclasses must override!!"






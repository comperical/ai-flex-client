

from . import openai_impl as OAI
from . import anthro_impl as ANTHRO
from . import gemini_impl as GEMINI
from . import synth_impl as SYNTH
from . import grok_impl as GROK


def run_simple_query(query):

    query.set_simple_prompt("Please respond with a single word: ELEPHANT")
    query.od_run_query()
    wrapper = query.get_data_wrapper()

    print(f"Model is {query.model_code}, Response is {wrapper.get_basic_text()}, cost is {wrapper.get_cost_dollar()}")



def run_all_configured_test():


    for impl in [OAI, ANTHRO, GEMINI, SYNTH, GROK]:
        if not impl.is_configured():
            continue

        run_simple_query(impl.build_query())


if __name__ == '__main__':

    for impl in [OAI, ANTHRO, GEMINI, SYNTH, GROK]:
        impl.opt_register()


    run_all_configured_test()
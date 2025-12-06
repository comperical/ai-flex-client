

import openai_impl as OAI
import anthro_impl as ANTHRO


def run_simple_query(query):

    query.set_simple_prompt("Please respond with a single word: ELEPHANT")
    query.od_run_query()
    wrapper = query.get_data_wrapper()

    print(f"Response is {wrapper.get_basic_text()}, cost is {wrapper.get_cost_dollar()}")



if __name__ == '__main__':

    print("Going to run a test")


    impl = ANTHRO

    impl.register_key_from_environment()

    #OAI.register_key_from_environment()

    run_simple_query(impl.build_query())


from . import utility as UTIL
from . import openai_impl as OAI
from . import anthro_impl as ANTHRO
from . import gemini_impl as GEMINI
from . import synth_impl as SYNTH
from . import grok_impl as GROK
from . import venice_impl as VENICE


ALL_IMPL = [OAI, ANTHRO, GEMINI, SYNTH, GROK, VENICE]


def run_simple_query(query):

    query.set_simple_prompt("Please respond with a single word: ELEPHANT")
    query.od_run_query()
    wrapper = query.get_data_wrapper()

    print(f"Model is {query.model_code}, Response is {wrapper.get_basic_text()}, cost is {wrapper.get_cost_dollar()}")



def run_all_configured_test(register=False):

    for impl in ALL_IMPL:

        if register:
            impl.opt_register()

        if not impl.is_configured():
            continue

        run_simple_query(impl.LlmQuery())


def verify_model_registry():

    from .model_name import ModelName
    from . import utility as UTIL

    registry = UTIL.get_registry()
    failures = []

    for model in ModelName:
        code = model.code
        info = registry.lookup_model(code)
        if info is None:
            failures.append(model)
        else:
            print(f"  OK: {model.name:30s} -> {info.provider:12s} {info.display}")

    if failures:
        names = ", ".join(m.name for m in failures)
        raise AssertionError(f"Models not found in registry: {names}")

    print(f"\nAll {len(ModelName)} model names verified in registry")


def verify_lookup_implementation():

    from .model_name import ModelName

    failures = []

    for model in ModelName:
        code = model.code
        try:
            query_class = UTIL.lookup_implementation(code)
            print(f"  OK: {model.name:30s} -> {query_class.__name__}")
        except AssertionError:
            failures.append(model)
            print(f"  FAIL: {model.name:30s} ({code})")

    if failures:
        names = ", ".join(m.name for m in failures)
        raise AssertionError(f"No implementation found for: {names}")

    print(f"\nAll {len(ModelName)} model names resolved to implementations")


if __name__ == '__main__':

    verify_model_registry()
    verify_lookup_implementation()

    for impl in ALL_IMPL:
        impl.opt_register()

    run_all_configured_test()
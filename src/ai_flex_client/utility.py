
import os
import time
import functools

def curtime_milli():
    return time.time() * 1000



def lookup_implementation(modelcode):


    if "claude" in modelcode:
        from . import anthro_impl as ANTHRO
        return ANTHRO.LlmQuery


    if "gemini" in modelcode:
        from . import gemini_impl as GEMINI
        return GEMINI.LlmQuery


    if "venice" in modelcode:
        from . import venice_impl as VENICE
        return VENICE.LlmQuery


    if "glm" in modelcode:
        from . import venice_impl as VENICE
        return VENICE.LlmQuery


    if "grok" in modelcode:
        from . import grok_impl as GROK
        return GROK.LlmQuery

    # Gotcha, the gpt-oss-120b both starts with hf: and has "gpt" in the name
    if modelcode.startswith("hf:"):
        from . import synth_impl as SYNTH
        return SYNTH.LlmQuery

    # Matches gpt-* models and o-series reasoning models (o3, o4-mini, etc.)
    if "gpt" in modelcode or modelcode.startswith("o"):
        from . import openai_impl as OAI
        return OAI.LlmQuery

    assert False, f"Failed to find good implementation for model code {modelcode}"


# Path to the data/ directory inside the package
_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# JSON file with per-model pricing info for all providers
_MODEL_JSON_PATH = os.path.join(_DATA_DIR, "llm_models.json")


@functools.lru_cache(maxsize=1)
def get_registry():
    from .model_registry import ModelRegistry
    return ModelRegistry(_MODEL_JSON_PATH)


def lookup_register(envname, regcb, missingokay=False):
    envkey = os.environ.get(envname, None)
    if envkey == None and missingokay:
        return

    assert envkey != None, f"You must set the environment variable {envname}"
    regcb(envkey)



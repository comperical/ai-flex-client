
import os
import time
import functools

def curtime_milli():
    return time.time() * 1000



def lookup_implementation(modelcode):


    if "claude" in modelcode:
        from . import anthro_impl as ANTHRO
        return ANTHRO.AnthroQuery


    if "gemini" in modelcode:
        from . import gemini_impl as GEMINI
        return GEMINI.GeminiQuery


    if "venice" in modelcode:
        from . import venice_impl as VENICE
        return VENICE.VeniceQuery


    if "glm" in modelcode:
        from . import venice_impl as VENICE
        return VENICE.VeniceQuery


    if "grok" in modelcode:
        from . import grok_impl as GROK
        return GROK.GrokQuery

    # Gotcha, the gpt-oss-120b both starts with hf: and has "gpt" in the name
    if modelcode.startswith("hf:"):
        from . import synth_impl as SYNTH
        return SYNTH.SyntheticQuery

    if "gpt" in modelcode:
        from . import openai_impl as OAI
        return OAI.OaiQuery

    assert False, f"Failed to find good implementation for model code {modelcode}"


# Path to the data/ directory at the repo root, sibling of src/
_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")

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



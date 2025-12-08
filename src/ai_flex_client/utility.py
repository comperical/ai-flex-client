
import os
import time

def curtime_milli():
    return time.time() * 1000



def lookup_implementation(modelcode):


    if "claude" in modelcode:
        from . import anthro_impl as ANTHRO
        return ANTHRO.AnthroQuery

    if "gemini" in modelcode:
        from . import gemini_impl as GEMINI
        return GEMINI.GeminiQuery


    # Gotcha, the gpt-oss-120b both starts with hf: and has "gpt" in the name
    if modelcode.startswith("hf:"):
        from . import synth_impl as SYNTH
        return SYNTH.SyntheticQuery

    if "gpt" in modelcode:
        from . import openai_impl as OAI
        return OAI.OaiQuery

    assert False, f"Failed to find good implementation for model code {modelcode}"


def lookup_register(envname, regcb, missingokay=False):
    envkey = os.environ.get(envname, None)
    if envkey == None and missingokay:
        return

    assert envkey != None, f"You must set the environment variable {envname}"
    regcb(envkey)



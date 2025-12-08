
import os
import time

def curtime_milli():
    return time.time() * 1000

def lookup_register(envname, regcb, missingokay=False):
    envkey = os.environ.get(envname, None)
    if envkey == None and missingokay:
        return

    assert envkey != None, f"You must set the environment variable {envname}"
    regcb(envkey)



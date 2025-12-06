
import os
import time


CLIENT_FACTORY_INFO = {}

def curtime_milli():
    return time.time() * 1000


def get_client_by_code(clientcode):

    factory = CLIENT_FACTORY_INFO.get(clientcode, None)
    assert factory != None, f"Attempt to get client for unregistered code {clientcode}, please call register_client_factory(...)"

def get_openai_client():
    return get_client_by_code("openai")


def register_client_factory(clientcode, clifactory):

    assert not clientcode in CLIENT_FACTORY_INFO, f"Client is already registered: {clientcode}"
    CLIENT_FACTORY_INFO[clientcode] = clifactory
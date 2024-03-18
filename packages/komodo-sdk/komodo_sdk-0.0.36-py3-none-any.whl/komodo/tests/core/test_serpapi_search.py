import os

from serpapi import GoogleSearch

from komodo.core.tools.web.serpapi_search import SerpapiSearch
from komodo.testdata.config import TestConfig


def test_serpapi_google():
    search = GoogleSearch({
        "q": "kineo capital",
        "location": "New York, New York",
        "api_key": os.environ["SERP_API_KEY"]
    })
    result = search.get_dict()
    print(f'result:{result}')
    return result


def test_serpapi_bing():
    search = GoogleSearch({
        "engine": "bing",
        "q": "kineo capital",
        "location": "New York, New York",
        "api_key": os.environ["SERP_API_KEY"]
    })
    result = search.get_dict()
    print(f'result:{result}')
    return result


def test_serpapi_search():
    api_key = TestConfig.get_serp_api_key()
    search = SerpapiSearch(api_key)
    print(search.definition)
    print(search.action({"query": "Nvidia news"}))


def test_serpapi_search_action():
    api_key = TestConfig.get_serp_api_key()
    search = SerpapiSearch(api_key)
    print(search.action({"query": "Kineo Capital"}))


def test_serpapi_search_action_bing():
    api_key = TestConfig.get_serp_api_key()
    search = SerpapiSearch(api_key)
    print(search.action({"query": "Kineo Capital", "engine": "bing"}))


def test_serpapi_search_action_params():
    api_key = TestConfig.get_serp_api_key()
    search = SerpapiSearch(api_key)
    print(search.action({"query": "Kineo Capital", "engine": "bing", "params": {"hl": "fr"}}))

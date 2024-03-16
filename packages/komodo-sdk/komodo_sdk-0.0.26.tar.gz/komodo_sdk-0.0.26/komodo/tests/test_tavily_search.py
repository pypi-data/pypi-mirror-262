from komodo.core.tools.web.tavily_search_tool import tavily_search_action, tavily_search_definition


def test_tavily_api():
    query = "\"Kineo Capital\" +information +safe"
    result = tavily_search_action({"query": query})
    print(f'search_result:{result}')
    return result


def test_tavily_description():
    print(tavily_search_definition())


def test_tavily_search_action():
    print(tavily_search_action({"query": "Kineo Capital"}))

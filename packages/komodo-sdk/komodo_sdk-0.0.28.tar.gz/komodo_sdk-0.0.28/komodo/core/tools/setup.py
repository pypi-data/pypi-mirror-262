from komodo.core.tools.folder.data_lister import setup_data_lister_action
from komodo.core.tools.folder.data_reader import setup_data_reader_action
from komodo.core.tools.web.action_scrape import setup_scraper_action
from komodo.core.tools.web.action_serpapi_search import setup_serpapi_search_action
from komodo.core.tools.web.tavily_search_tool import setup_tavily_search_action


def setup_all_tools():
    setup_scraper_action()
    setup_serpapi_search_action()
    setup_tavily_search_action()
    setup_data_reader_action()
    setup_data_lister_action()

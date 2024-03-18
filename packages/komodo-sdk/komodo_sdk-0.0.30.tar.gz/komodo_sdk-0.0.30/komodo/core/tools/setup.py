from komodo.core.tools.files.directory_reader import DirectoryReader
from komodo.core.tools.files.file_reader import FileReader
from komodo.core.tools.web.serpapi_search import SerpapiSearch
from komodo.core.tools.web.tavily_search import TavilySearch
from komodo.core.tools.web.web_scraper import WebScraper
from komodo.framework.komodo_tool_registry import KomodoToolRegistry


def get_all_core_tools():
    return [FileReader(), DirectoryReader(), SerpapiSearch(), TavilySearch(), WebScraper()]


def setup_all_core_tools():
    tools = [FileReader(), DirectoryReader(), SerpapiSearch(), TavilySearch(), WebScraper()]
    for tool in tools:
        KomodoToolRegistry.add_komodo_tool(tool)

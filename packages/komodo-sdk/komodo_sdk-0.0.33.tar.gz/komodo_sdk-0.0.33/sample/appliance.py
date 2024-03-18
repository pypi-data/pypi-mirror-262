from komodo import KomodoApp
from komodo.core.agents.default import translator_agent, summarizer_agent
from komodo.core.agents.docsearch_agent import DocSearchAgent

from komodo.core.agents.librarian_agent import LibrarianAgent
from komodo.core.tools.web.serpapi_search import SerpapiSearch
from komodo.framework.komodo_datasource import default_data_directory
from komodo.loaders.appliance_loader import ApplianceLoader
from komodo.models.framework.appliance_runner import ApplianceRunner


class SampleAppliance(KomodoApp):
    def __init__(self):
        super().__init__(shortcode='sample', name='Sample', purpose='To test the Komodo Appliances SDK')
        self.add_agent(LibrarianAgent.create(path=default_data_directory(), collection_name="default"))
        self.add_agent(DocSearchAgent.create(path=default_data_directory()))
        self.add_agent(summarizer_agent())
        self.add_agent(translator_agent())
        self.add_tool(SerpapiSearch())
        self.index()


def build_and_run():
    appliance = SampleAppliance()
    prompt = '''
        Summarize the following text in 5 words and then translate into Spanish, Hindi and German:
        This is a sample application using the new Komodo SDK.
    '''
    runner = ApplianceRunner(appliance)
    response = runner.run(prompt)
    print(response.text)


def build_and_search():
    appliance = SampleAppliance()
    appliance.index()
    prompt = '''
        what is NCC?
    '''
    runner = ApplianceRunner(appliance)
    response = runner.run(prompt)
    print(response.text)


def load_and_run():
    appliance = ApplianceLoader.load('sample')
    prompt = '''
        Summarize the following text in 5 words and translate into Spanish, Hindi and German:
        This is a sample application using the new Komodo 9 SDK.
    '''
    runner = ApplianceRunner(appliance)
    response = runner.run(prompt)
    print(response.text)


if __name__ == '__main__':
    build_and_search()

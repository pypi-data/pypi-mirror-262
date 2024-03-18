from komodo import KomodoApp
from komodo.core.agents.default import translator_agent, summarizer_agent
from komodo.core.tools.setup import get_all_core_tools
from komodo.core.vector_stores.qdrant_store import QdrantStore
from komodo.loaders.appliance_loader import ApplianceLoader
from komodo.models.framework.appliance_runner import ApplianceRunner
from komodo.server.fast import prepare_fastapi_app


class SampleAppliance(KomodoApp):
    def __init__(self):
        super().__init__(shortcode='sample', name='Sample', purpose='To test the Komodo Appliances SDK')
        self.add_agent(summarizer_agent())
        self.add_agent(translator_agent())
        self.add_tool('komodo_serpapi_search')

        #for tool in get_all_core_tools():
        #    self.add_tool(tool)

        qdrant = QdrantStore(shortcode="default", name="Appliance Vector Store", collection_name="sample")
        self.add_vector_store(qdrant)


def build_and_run():
    appliance = SampleAppliance()
    prompt = '''
        Summarize the following text in 5 words and then translate into Spanish, Hindi and German:
        This is a sample application using the new Komodo SDK.
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


SERVER = prepare_fastapi_app(SampleAppliance())


def run_server():
    import uvicorn
    uvicorn.run(SERVER, host="127.0.0.1", port=8000)  # noinspection PyTypeChecker


if __name__ == '__main__':
    build_and_run()
    # run_server()

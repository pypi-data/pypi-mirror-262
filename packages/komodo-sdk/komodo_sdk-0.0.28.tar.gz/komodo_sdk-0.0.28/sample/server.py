from komodo import KomodoApp
from komodo.core.agents.default import translator_agent, summarizer_agent
from komodo.core.vector_stores.qdrant_store import QdrantStore
from komodo.loaders.appliance_loader import ApplianceLoader
from komodo.models.framework.runners import run_appliance, list_capabilities
from komodo.server.fast import app
from komodo.server.globals import set_appliance_for_fastapi


def build() -> KomodoApp:
    app = KomodoApp(shortcode='sample', name='Sample', purpose='To test the Komodo Appliances SDK')
    app.add_agent(summarizer_agent())
    app.add_agent(translator_agent())
    app.add_tool('komodo_data_reader')
    app.add_tool('komodo_data_lister')
    app.add_tool('komodo_serpapi_search')
    app.add_tool('komodo_web_content_extractor')

    qdrant = QdrantStore(shortcode="default", name="Appliance Vector Store", collection_name="sample")
    app.add_vector_store(qdrant)
    print(list_capabilities(app))
    return app


def build_and_run():
    app = build()
    prompt = '''
        Summarize the following text in 5 words and translate into Spanish, Hindi and German:
        This is a sample application using the new Komodo 9 SDK.
    '''
    response = run_appliance(app, prompt)
    print(response.text)


def load_and_run():
    app = ApplianceLoader.load('sample')
    prompt = '''
        Summarize the following text in 5 words and translate into Spanish, Hindi and German:
        This is a sample application using the new Komodo 9 SDK.
    '''
    response = run_appliance(app, prompt)
    print(response.text)


SAMPLE_APP = app
set_appliance_for_fastapi(build())


def run_server():
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)  # noinspection PyTypeChecker


if __name__ == '__main__':
    # build_and_run()
    run_server()

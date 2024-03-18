from komodo.core.tools.search.vector_search import VectorSearchToolFactory
from komodo.core.utils.indexer import Indexer
from komodo.framework.komodo_agent import KomodoAgent
from komodo.models.framework.agent_runner import AgentRunner
from komodo.shared.utils.digest import get_text_digest
from komodo.shared.utils.term_colors import print_info


class DocSearchAgent(KomodoAgent):
    shortcode = "docsearch"
    name = "Document Search Agent"
    purpose = "Answer questions based on documents provided."
    instructions = "You are a Document QnA Agent. You will be given a document and a question. " \
                   "Use the vector_search_tool before using other tools " \
                   "Use the vector_search_tool tool to fetch relevant portions of the documents. " \
                   "You must answer the question based on the document. " \
                   "Do not use any external sources. Use only the document to answer the question. "

    def __init__(self, shortcode, path, collection_name):
        super().__init__(shortcode=shortcode,
                         name=self.name,
                         purpose=self.purpose,
                         instructions=self.instructions,
                         temperature=0.2)

        print_info(f"Creating DocSearchAgent for path: {path} and collection_name: {collection_name}")
        self.path = path
        self.collection_name = collection_name
        search_tool = VectorSearchToolFactory.qdrant(self.collection_name)
        self.add_tool(search_tool)

    @classmethod
    def create(cls, path, collection_name=None):
        collection_name = get_text_digest(str(path)) if collection_name is None else collection_name
        shortcode = cls.shortcode + "_" + collection_name if collection_name != 'default' else cls.shortcode
        return cls(shortcode, path, collection_name)

    def index(self, reindex=False):
        indexer = Indexer(self.collection_name, self.path)
        indexer.run(reindex=reindex)


def run_search():
    agent = DocSearchAgent.create(path="./data/test1")
    agent.index()
    runner = AgentRunner(agent)
    response = runner.run("What did the G20 leaders agreed in 2009?")
    print(response.text)

    response = runner.run("tell me more about unique swap identifiers (USI) of each clearing swap?")
    print(response.text)


if __name__ == "__main__":
    run_search()

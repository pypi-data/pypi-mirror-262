import json

from komodo.framework.komodo_agent import KomodoAgent
from komodo.framework.komodo_tool import KomodoTool
from komodo.models.framework.models import OPENAI_GPT4_MODEL


class LibrarianTool(KomodoTool):

    def __init__(self, app):
        self.app = app
        super().__init__(shortcode=self.shortcode,
                         definition=self.definition,
                         action=self.action)

    shortcode = "komodo_data_search"
    definition = {
        "type": "function",
        "function": {
            "name": "komodo_data_search",
            "description": "Search available data sources",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search across all available data using vector search"
                    }
                },
                "required": ["query"]
            }
        }
    }

    def action(self, args):
        text = args['query']
        store = self.app.get_vector_store()
        result = store.search(text, top_k=3)
        if len(result) > 0:
            return json.dumps(result)
        return "No results found for: {}".format(args['query'])


def librarian_agent(app):
    librarian_tool = LibrarianTool(app)
    shortcode = "librarian"
    name = 'Librarian Agent'
    purpose = 'Retrieves knowledge from private data sources'
    instructions = 'You MUST use the data sources available to retrieve the information needed for the task. ' \
                   'Do not use any other sources. ' \
                   'Describe answers in detail of up to 600 words and cite the sources.'
    return KomodoAgent(shortcode=shortcode,
                       name=name,
                       purpose=purpose,
                       model=OPENAI_GPT4_MODEL,
                       instructions=instructions,
                       tools=[librarian_tool])

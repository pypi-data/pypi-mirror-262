from komodo.framework.komodo_agent import KomodoAgent
from komodo.framework.komodo_librarian import LibrarianTool, librarian_agent
from komodo.framework.komodo_tool import KomodoTool
from komodo.framework.komodo_tool_registry import KomodoToolRegistry
from komodo.framework.komodo_vectorstore import KomodoVectorStore


class KomodoApp:
    def __init__(self, shortcode, name, purpose):
        self.shortcode = shortcode
        self.name = name
        self.purpose = purpose
        self.agents: [KomodoAgent] = []
        self.tools: [KomodoTool] = []
        self.vector_stores: [KomodoVectorStore] = []

    def add_agent(self, agent):
        self.agents += [agent]

    def add_tool(self, tool):
        if isinstance(tool, str):
            tool = KomodoToolRegistry.get_tool_by_shortcode(tool)
        elif isinstance(tool, dict):
            tool = KomodoTool(**tool)
        if isinstance(tool, KomodoTool):
            self.tools.append(tool)
            return
        raise ValueError(f"Invalid tool: {tool}")

    def add_vector_store(self, store: KomodoVectorStore):
        self.vector_stores.append(store)
        if store.shortcode == 'default':
            librarian_tool = LibrarianTool(self)
            self.tools = [librarian_tool] + self.tools
            self.agents = [librarian_agent(self)] + self.agents

    def get_vector_store(self, shortcode='default'):
        for a in self.vector_stores:
            if a.shortcode == shortcode:
                return a
        return None

    def get_default_vector_store(self):
        return self.get_vector_store('default')

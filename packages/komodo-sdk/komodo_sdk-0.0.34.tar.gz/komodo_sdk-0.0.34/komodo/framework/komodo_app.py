from komodo.framework.komodo_agent import KomodoAgent
from komodo.framework.komodo_tool import KomodoTool
from komodo.framework.komodo_tool_registry import KomodoToolRegistry


class KomodoApp:
    def __init__(self, shortcode, name, purpose):
        self.shortcode = shortcode
        self.name = name
        self.purpose = purpose
        self.agents: [KomodoAgent] = []
        self.tools: [KomodoTool] = []

    def add_agent(self, agent):
        self.agents += [agent]

    def add_tool(self, tool):
        self.tools.extend(KomodoToolRegistry.get_tools([tool]))

    def generate_context(self):
        return None

    def index(self, reindex=False):
        for agent in self.agents:
            agent.index(reindex=reindex)

    @staticmethod
    def default():
        return KomodoApp(name="Placeholder", shortcode="placeholder", purpose="Placeholder")

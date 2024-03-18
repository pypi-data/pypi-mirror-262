from komodo.framework.komodo_tool import KomodoTool
from komodo.framework.komodo_tool_registry import KomodoToolRegistry
from komodo.models.framework.models import OPENAI_GPT35_MODEL


class KomodoAgent:
    def __init__(self, *, shortcode, name, instructions, email=None, purpose=None,
                 model=OPENAI_GPT35_MODEL, provider="openai", tools=None,
                 temperature=None, seed=None, top_p=None, max_tokens=None, output_format=None):
        self.shortcode = shortcode or name.lower().replace(" ", "_")
        self.name = name
        self.instructions = instructions
        self.email = email or f"{self.shortcode}@kmdo.app"
        self.purpose = purpose or f"An agent to {instructions}"
        self.model = model
        self.provider = provider
        self.tools: [KomodoTool] = KomodoToolRegistry.get_tools(tools)
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.seed = seed
        self.top_p = top_p
        self.output_format = output_format

    def __str__(self):
        return f"KomodoAgent: {self.name} ({self.email}), {self.purpose}"

    def to_dict(self):
        return {
            "shortcode": self.shortcode,
            "name": self.name,
            "instructions": self.instructions,
            "email": self.email,
            "purpose": self.purpose,
            "model": self.model,
            "provider": self.provider,
            "tools": [t.to_dict() for t in self.tools],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "seed": self.seed,
            "top_p": self.top_p,
            "output_format": None
        }

    def add_tool(self, tool):
        self.tools.extend(KomodoToolRegistry.get_tools([tool]))

    def generate_context(self):
        return None

    @staticmethod
    def default():
        return KomodoAgent(shortcode="komodo", name="Komodo",
                           instructions="Please provide a response to the prompt below.")


if __name__ == '__main__':
    agent = KomodoAgent.default()
    print(agent)
    print(agent.to_dict())

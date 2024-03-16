from komodo.framework.komodo_tool import KomodoTool
from komodo.framework.komodo_tool_registry import KomodoToolRegistry
from komodo.models.framework.models import OPENAI_GPT35_MODEL


class KomodoAgent:
    def __init__(self, name, instructions, purpose=None, model=OPENAI_GPT35_MODEL, provider="openai",
                 shortcode=None, email=None, reply_as=None, phone=None, chatbot=False, assistant_id=None, tools=None,
                 output_format=None, footer=None):
        self.shortcode = shortcode or name.lower().replace(" ", "_")
        self.name = name
        self.email = email or f"{self.shortcode}@kmdo.app"
        self.reply_as = reply_as or self.email
        self.purpose = purpose or f"An agent to {instructions}"
        self.instructions = instructions
        self.model = model
        self.provider = provider
        self.assistant_id = assistant_id
        self.tools: [KomodoTool] = []
        self.output_format = output_format
        self.footer = footer
        self.phone = phone
        self.chatbot = chatbot
        for tool in tools or []:
            self.add_tool(tool)

    def __str__(self):
        return f"KomodoAgent: {self.name} ({self.email}), {self.purpose}"

    def to_dict(self):
        return {
            'shortcode': self.shortcode,
            'name': self.name,
            'email': self.email,
            'reply_as': self.reply_as,
            'purpose': self.purpose,
            'instructions': self.instructions,
            'model': self.model,
            'provider': self.provider,
            'assistant_id': self.assistant_id,
            'tools': [tool.to_dict() for tool in self.tools],
            'output_format': self.output_format,
            'footer': self.footer,
            'phone': self.phone,
            'chatbot': self.chatbot
        }

    def add_tool(self, tool):
        if isinstance(tool, str):
            tool = KomodoToolRegistry.get_tool_by_shortcode(tool)
        if isinstance(tool, KomodoTool):
            self.tools.append(tool)
            return
        raise ValueError(f"Invalid tool: {tool}")

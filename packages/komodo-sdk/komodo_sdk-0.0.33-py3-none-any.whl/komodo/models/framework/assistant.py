from datetime import datetime

from komodo.framework.komodo_agent import KomodoAgent
from komodo.framework.komodo_tool_registry import KomodoToolRegistry
from komodo.framework.komodo_user import KomodoUser
from komodo.models.framework.models import OPENAI_GPT4_MODEL


class CompletionMetaData:
    def __init__(self, user: KomodoUser, agent: KomodoAgent):
        self.user = user
        self.agent = agent
        self.model = agent.model

    def max_function_output_len(self):
        return 12000 if self.model == OPENAI_GPT4_MODEL else 6000


class ModelRequest:
    def __init__(self, user: KomodoUser, agent: KomodoAgent, prompt: str, history=None):
        self.user = user
        self.agent = agent
        self.prompt = prompt
        self.context = self.build_context(agent.generate_context())
        self.history = history

    def __str__(self):
        template = "From: {} To: {} Name: {} (provider: {}, model: {})"
        return template.format(self.user.email,
                               self.agent.email,
                               self.agent.name,
                               self.agent.provider,
                               self.agent.model)

    def prepare_messages(self):
        instructions = self.build_message("INSTRUCTIONS", self.agent.instructions)
        caution = self.build_message("CAUTION", "Do not make up fake data or hallucinate information.")
        guidance = self.build_message("GUIDANCE", "Prioritize tools provided to you to answer the questions.")
        context = [] if self.context is None else self.context
        history = [] if self.history is None else self.history
        messages = [instructions, caution, guidance] + context + history
        return messages

    def prepare_metadata(self):
        return CompletionMetaData(self.user, self.agent)

    def build_openai_params(self, stream=False):
        params = {
            "model": self.agent.model,
            "messages": self.prepare_messages(),
            "stream": stream,
            "temperature": self.agent.temperature,
            "top_p": self.agent.top_p,
            "seed": self.agent.seed,
            "max_tokens": self.agent.max_tokens,
        }

        if self.agent.tools:
            params["tools"] = KomodoToolRegistry.get_definitions(self.agent.tools)

        if self.agent.provider == "openai" and self.agent.output_format and 'json' in self.agent.output_format:
            from openai.types.chat.completion_create_params import ResponseFormat
            params['response_format'] = ResponseFormat(type="json_object")

        return params

    def prepare_detailed_prompt(self):
        conversation = []
        messages = self.prepare_messages()
        for message in messages:
            conversation.append(message['role'] + ": " + message['content'])
        conversation.append("Prompt: " + self.prompt)
        return "\n".join(conversation)

    @staticmethod
    def build_message(tag, message, role="system"):
        return {"role": role, "content": tag + ": " + message}

    @staticmethod
    def build_context(context):
        if isinstance(context, dict):
            return [context]
        if isinstance(context, list):
            return context
        if isinstance(context, str):
            return [ModelRequest.build_message("IMPORTANT", context)]
        return []


class ModelResponse:
    model: str
    status: str
    output: None
    text: str
    has_markdown: bool
    has_quotes: bool
    is_json: bool
    run_id: str
    started: int
    completed: int

    def __init__(self, model, status, output, text, has_markdown=False, has_quotes=True, is_json=False, run_id=None):
        self.model = model
        self.status = status
        self.output = output
        self.text = text
        self.has_markdown = has_markdown
        self.has_quotes = has_quotes
        self.is_json = is_json
        self.run_id = run_id if run_id else datetime.now().strftime("%Y%m%d%H%M%S")

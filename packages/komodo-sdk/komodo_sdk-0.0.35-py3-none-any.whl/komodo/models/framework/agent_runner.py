from komodo.core.agents.summarizer_agent import SummarizerAgent
from komodo.core.tools.files.directory_reader import DirectoryReader
from komodo.framework.komodo_agent import KomodoAgent
from komodo.framework.komodo_user import KomodoUser
from komodo.models.framework.assistant import ModelRequest, ModelResponse
from komodo.models.framework.responder import get_model_response
from komodo.models.openai.openai_api_streamed import openai_chat_response_streamed


class AgentRunner:
    def __init__(self, agent: KomodoAgent):
        self.user = KomodoUser.default()
        self.agent = agent

    def run(self, prompt, history=None) -> ModelResponse:
        request = ModelRequest(user=self.user, agent=self.agent, prompt=prompt, history=history)
        response = get_model_response(request)
        return response

    def run_streamed(self, prompt, history=None):
        request = ModelRequest(user=self.user, agent=self.agent, prompt=prompt, history=history)
        for response in openai_chat_response_streamed(request):
            yield response


if __name__ == '__main__':

    agent = SummarizerAgent.create(100)
    print(agent.instructions)

    agent = SummarizerAgent(n=200)
    print(agent.instructions)

    runner = AgentRunner(agent)
    result = runner.run("Summarize the iliad in 5 words")
    print(result.text)

    agent = KomodoAgent.default()
    agent.tools = [DirectoryReader()]
    runner = AgentRunner(agent)

    prompt = "list files available to you"
    response = runner.run(prompt)
    print(response.text)

    for response in runner.run_streamed(prompt):
        print(response, end="")
    print()

    prompt = "whats up in nyc today? search for event and then search for additional details on the first event found"
    agent.tools = ["komodo_serpapi_search"]
    for response in runner.run_streamed(prompt):
        print(response, end="")
    print()

    response = runner.run(prompt)
    print(response.text)

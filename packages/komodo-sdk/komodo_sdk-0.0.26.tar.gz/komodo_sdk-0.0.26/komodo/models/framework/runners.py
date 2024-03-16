from komodo.framework.komodo_agent import KomodoAgent
from komodo.framework.komodo_tool import KomodoTool
from komodo.framework.komodo_user import KomodoUser
from komodo.models.framework.assistant import AssistantRequest, AssistantResponse
from komodo.models.framework.models import OPENAI_GPT4_MODEL
from komodo.models.framework.responder import get_assistant_response
from komodo.models.openai.openai_api_streamed import openai_chat_response_streamed


def run_appliance(appliance, prompt):
    agent = coordinator_agent(appliance)
    return run_agent(appliance, agent, prompt)


def run_agent(appliance, agent, prompt, history=None) -> AssistantResponse:
    user = KomodoUser.default_user().to_dict()
    assistant = agent.to_dict()
    assistant['tools'] = agent.tools + appliance.tools
    request = AssistantRequest(user=user, assistant=assistant, prompt=prompt, history=history)
    response = get_assistant_response(request)
    return response


def run_agent_streamed(appliance, agent, prompt, history=None):
    user = KomodoUser.default_user().to_dict()
    assistant = agent.to_dict()
    assistant['tools'] = agent.tools + appliance.tools
    request = AssistantRequest(user=user, assistant=assistant, prompt=prompt, history=history)
    for response in openai_chat_response_streamed(request):
        yield response


def run_agent_as_tool(appliance, agent, args) -> str:
    response = run_agent(appliance, agent, args['system'] + "\n\n" + args['user'])
    return response.text


def agent_function_definition(agent):
    return {
        "type": "function",
        "function": {
            "name": agent.shortcode,
            "description": agent.purpose,
            "parameters": {
                "type": "object",
                "properties": {
                    "system": {
                        "type": "string",
                        "description": "Specify context and what exactly you need the agent to do in English."
                    },
                    "user": {
                        "type": "string",
                        "description": "The input to be processed by the agent."
                    },
                },
                "required": ["system", "user"]
            }
        }
    }


def get_agent_as_tool(appliance, agent):
    action = lambda args: run_agent_as_tool(appliance, agent, args)
    return KomodoTool(shortcode=agent.shortcode,
                      definition=agent_function_definition(agent),
                      action=action)


def coordinator_shortcode(appliance):
    return appliance.shortcode + "_coordinator"


def coordinator_agent(appliance):
    return KomodoAgent(shortcode=coordinator_shortcode(appliance),
                       name='Appliance Default Agent',
                       purpose='Coordinate other agents in the appliance to achieve the goal',
                       model=OPENAI_GPT4_MODEL,
                       instructions='Coordinate the other agents to achieve the goal. Create system and user prompts for each agent based on task requirements and inputs.',
                       tools=[get_agent_as_tool(appliance, agent) for agent in appliance.agents])


def get_all_agents(appliance):
    return [coordinator_agent(appliance)] + appliance.agents


def get_agent(appliance, shortcode):
    for a in get_all_agents(appliance):
        if a.shortcode == shortcode:
            return a
    return None


def get_capabilities_of_agents(appliance):
    t = [
        "{}. {} ({}): {}".format(i, a.name, a.shortcode, a.purpose)
        for i, a in enumerate(get_all_agents(appliance), start=1)
        if a.purpose is not None
    ]
    return '\n'.join(t)


def get_capabilities_of_tools(self):
    # Filter tools with a purpose and enumerate, then format the string
    t = ["{}. {}: {}".format(i + 1, tool.shortcode, tool.purpose)
         for i, tool in enumerate(filter(lambda x: x.purpose is not None, self.tools))]
    return '\n'.join(t)


def list_capabilities(appliance):
    return "I am " + appliance.name + \
        " appliance and my purpose is " + appliance.purpose + "." + \
        "\n\nI have agents with these capabilities: \n" + get_capabilities_of_agents(appliance) + \
        "\n\nI have tools with these capabilities: \n" + get_capabilities_of_tools(appliance)

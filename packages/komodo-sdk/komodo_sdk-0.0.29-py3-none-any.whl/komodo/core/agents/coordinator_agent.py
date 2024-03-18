from komodo.core.agents.groot_agent import GrootAgent
from komodo.framework.komodo_agent import KomodoAgent
from komodo.framework.komodo_app import KomodoApp
from komodo.framework.komodo_tool import KomodoTool
from komodo.models.framework.models import OPENAI_GPT4_MODEL


class CoordinatorAgent(KomodoAgent):
    model = OPENAI_GPT4_MODEL
    instructions = '''
    Act like an authoritative orchestrator of tasks. 
    You are responsible for managing the other agents and their interactions.
    Create user prompts for each agent based on task requirements and inputs.
    For each task breakdown step, describe your thinking to the tool "chain_of_thought" and then 
    proceed to invoke the agents in the right order.
        
    Orchestrate other agents that are provided as tools to achieve the goal.
    You MUST wait for response from one agent to feed into the other agents.
    
    Take time to understand the context and the goal of the task, break down the 
    tasks and order in which to call the other agents.
    
    The conversation has tool outputs of the agents. You must manage the conversation by 
    providing the right prompts and inputs to the agents. 
    
    Make useful assumptions when talking to these agents.
    
    The librarian tool is available to you to fetch information from the vector store, it should not be used 
    for internet searches or external sources.
    '''

    def __init__(self, appliance: KomodoApp, run_agent_as_tool):
        super().__init__(shortcode=appliance.shortcode + "_coordinator",
                         name=appliance.name + " Coordinator Agent",
                         purpose=appliance.purpose,
                         model=self.model,
                         instructions=self.instructions)
        self.appliance = appliance
        self.add_tool(self.get_chain_of_thought_tool())
        for agent in appliance.agents:
            self.add_tool(self.get_agent_as_tool(agent, run_agent_as_tool))
        for tool in appliance.tools:
            self.add_tool(tool)

    def generate_context(self):
        return self.appliance.generate_context()

    def get_agent_as_tool(self, agent, run_agent_as_tool):
        definiton = {
            "type": "function",
            "function": {
                "name": agent.shortcode,
                "description": f'The tool is an AI agent whose purpose is: {agent.purpose}.',
                "parameters": {
                    "type": "object",
                    "properties": {
                        "system": {
                            "type": "string",
                            "description": "Instructions to the agent. You can use it to provide context, parameters, hints and suggestions."
                        },
                        "user": {
                            "type": "string",
                            "description": "The prompt to be processed by the agent."
                        },
                    },
                    "required": ["system", "user"],
                    "notes": "Do not provide any other parameters. The agent will not understand them."
                }
            }
        }
        return KomodoTool(shortcode=agent.shortcode,
                          definition=definiton,
                          action=lambda args: run_agent_as_tool(agent, args))

    def get_chain_of_thought_tool(self):
        definition = {
            "type": "function",
            "function": {
                "name": "chain_of_thought",
                "description": "Describe your thinking to the tool",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "thought": {
                            "type": "string",
                            "description": "Describe your thinking to the tool"
                        }
                    },
                    "required": ["thought"]
                }
            }
        }
        return KomodoTool(shortcode="chain_of_thought",
                          definition=definition,
                          action=lambda args: "You have described your thinking to the tool. Proceed.")


if __name__ == '__main__':
    appliance = KomodoApp.default()
    appliance.add_agent(GrootAgent())
    agent = CoordinatorAgent(appliance, lambda agent: KomodoTool.default())
    print(agent)
    print(agent.to_dict())
    print(agent.generate_context())

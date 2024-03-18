from komodo.core.agents.groot_agent import GrootAgent
from komodo.core.tools.files.directory_reader import DirectoryReader
from komodo.core.tools.files.file_reader import FileReader
from komodo.core.tools.utils.agent_tool import AgentAsTool
from komodo.core.tools.utils.thought_tool import ChainOfThought
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
        self.add_tool(ChainOfThought())
        self.add_tool(DirectoryReader())
        self.add_tool(FileReader())

        for agent in appliance.agents:
            self.add_tool(AgentAsTool(agent, run_agent_as_tool))

        for tool in appliance.tools:
            self.add_tool(tool)

    def generate_context(self):
        return self.appliance.generate_context()


if __name__ == '__main__':
    appliance = KomodoApp.default()
    appliance.add_agent(GrootAgent())
    agent = CoordinatorAgent(appliance, lambda agent: KomodoTool.default())
    print(agent)
    print(agent.to_dict())
    print(agent.generate_context())

from komodo.core.agents.coordinator_agent import CoordinatorAgent
from komodo.core.agents.groot_agent import GrootAgent
from komodo.framework.komodo_app import KomodoApp
from komodo.models.framework.agent_runner import AgentRunner


class ApplianceRuntime:

    def __init__(self, appliance):
        self.appliance = appliance

    @staticmethod
    def run_agent_as_tool(agent, args) -> str:
        runner = AgentRunner(agent)
        history = [{'role': "system", 'content': args['system']}]
        response = runner.run(prompt=args['user'], history=history)
        return response.text

    def coordinator_agent(self):
        return CoordinatorAgent(self.appliance, ApplianceRuntime.run_agent_as_tool)

    def get_all_agents(self):
        return [self.coordinator_agent()] + self.appliance.agents

    def get_agent(self, shortcode):
        for a in self.get_all_agents():
            if a.shortcode == shortcode:
                return a
        return None

    def get_capabilities_of_agents(self):
        t = [
            "{}. {} ({}): {}".format(i, a.name, a.shortcode, a.purpose)
            for i, a in enumerate(self.get_all_agents(), start=1)
            if a.purpose is not None
        ]
        return '\n'.join(t)

    def get_capabilities_of_tools(self):
        t = ["{}. {}: {}".format(i + 1, tool.shortcode, tool.purpose)
             for i, tool in enumerate(filter(lambda x: x.purpose is not None, self.appliance.tools))]
        return '\n'.join(t)

    def list_capabilities(self):
        return "I am " + self.appliance.name + \
            " appliance and my purpose is " + self.appliance.purpose + "." + \
            "\n\nI have agents with these capabilities: \n" + self.get_capabilities_of_agents() + \
            "\n\nI have tools with these capabilities: \n" + self.get_capabilities_of_tools()


if __name__ == '__main__':
    appliance = KomodoApp.default()
    appliance.add_agent(GrootAgent())
    runtime = ApplianceRuntime(appliance)
    print(runtime.list_capabilities())

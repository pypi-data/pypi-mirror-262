from komodo.core.agents.groot_agent import GrootAgent
from komodo.framework.komodo_app import KomodoApp
from komodo.models.framework.agent_runner import AgentRunner
from komodo.models.framework.appliance_runtime import ApplianceRuntime


class ApplianceRunner:
    def __init__(self, appliance):
        self.runner = AgentRunner(ApplianceRuntime(appliance).coordinator_agent())

    def run(self, prompt):
        return self.runner.run(prompt)

    def run_streamed(self, prompt):
        for response in self.runner.run_streamed(prompt):
            yield response


if __name__ == '__main__':
    appliance = KomodoApp.default()
    appliance.add_agent(GrootAgent())
    runner = ApplianceRunner(appliance)
    result = runner.run("Tell me a joke using groot_agent.")
    print(result.text)

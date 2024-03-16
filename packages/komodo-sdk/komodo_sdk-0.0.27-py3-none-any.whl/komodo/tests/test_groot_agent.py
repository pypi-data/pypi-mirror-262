from komodo.core.agents.groot_agent import GrootAgent
from komodo.framework.komodo_app import KomodoApp
from komodo.models.framework.runners import run_agent


def test_groot():
    groot_agent = GrootAgent()
    print(groot_agent.to_dict())
    print(groot_agent.generate_context())

    appliance = KomodoApp(shortcode='groot', name='Groot', purpose='Test Appliance')
    appliance.add_agent(groot_agent)

    response = run_agent(appliance, groot_agent, "What is the purpose of groot?")
    print(response.text)

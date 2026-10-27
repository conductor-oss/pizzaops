# lab4.py: a plain LangGraph agent, run durably on Conductor
import sys
from conductor.ai.agents import AgentRuntime
from conductor.client.configuration.configuration import Configuration
from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
import pizza_data as pd


@tool
def get_incident_team(incident_id: str) -> str:
    """The on-call team for an incident and each person's dietary needs."""
    return pd.incident_team(incident_id)


@tool
def get_meal_budget(incident_id: str) -> str:
    """Remaining meal budget in USD for an incident."""
    return pd.meal_budget(incident_id)


@tool
def list_restaurants() -> str:
    """Restaurants that deliver to the office, with delivery times."""
    return pd.list_restaurants()


@tool
def get_menu(restaurant: str) -> str:
    """A restaurant's pizzas with prices in USD and dietary tags."""
    return pd.menu(restaurant)


graph = create_react_agent(
    ChatAnthropic(model="claude-haiku-5-5", temperature=0),
    tools=[get_incident_team, get_meal_budget, list_restaurants, get_menu],
    prompt="You are PizzaOps. Plan a food order for an incident's on-call team: "
           "everyone gets something they can eat, within budget, as fast as possible.",
    name="pizzaops_langgraph",
)

if __name__ == "__main__":
    request = " ".join(sys.argv[1:]) or "What should we order for INC-1042?"
    with AgentRuntime(Configuration()) as runtime:          # the only Conductor-specific lines
        runtime.run(graph, request).print_result()

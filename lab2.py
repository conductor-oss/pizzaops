# lab2.py: PizzaOps as a Conductor Agent
import sys
from conductor.ai.agents import Agent, AgentRuntime, tool
from conductor.client.configuration.configuration import Configuration
import pizza_data as pd

INSTRUCTIONS = (
    "You are PizzaOps. When an incident runs long, you feed the on-call team. "
    "Look up the team and their dietary needs, check the meal budget and compare menus. "
    "Plan an order where everyone gets at least one pizza they can eat, the total stays "
    "within budget and food arrives as soon as possible. Explain your choice briefly. "
    "If you have a place_order tool, place the order."
)


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


pizzaops = Agent(
    name="pizzaops",
    model="anthropic/claude-haiku-5-5",
    instructions=INSTRUCTIONS,
    tools=[get_incident_team, get_meal_budget, list_restaurants, get_menu],
)


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or \
        "INC-1042 has been running for 3 hours. What should we order for the team?"
    with AgentRuntime(Configuration()) as runtime:
        runtime.run(pizzaops, question).print_result()

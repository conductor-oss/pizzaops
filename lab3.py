# lab3.py: PizzaOps with a no-pineapple guardrail
import sys
from conductor.ai.agents import Agent, AgentRuntime, tool
from conductor.ai.agents import OnFail, Position, RegexGuardrail
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


no_pineapple = RegexGuardrail(
    patterns=[r"[Pp]ineapple|[Hh]awaiian"],  # JavaScript regex: no (?i)
    name="no_pineapple_on_company_time",
    position=Position.INPUT,
    on_fail=OnFail.RAISE,
    message="Policy: PizzaOps does not order pineapple. This is not up for discussion.",
)


@tool(guardrails=[no_pineapple])
def place_order(incident_id: str, restaurant: str, items: str, total_usd: float) -> str:
    """Place a food order. items is a comma-separated list."""
    return pd.place_order(incident_id, restaurant, items, total_usd)


pizzaops = Agent(
    name="pizzaops_guardrail",
    model="anthropic/claude-haiku-5-5",
    instructions=INSTRUCTIONS,
    tools=[get_incident_team, get_meal_budget, list_restaurants, get_menu, place_order],
)


if __name__ == "__main__":
    request = " ".join(sys.argv[1:]) or "Feed the on-call team for INC-1042."
    with AgentRuntime(Configuration()) as runtime:
        runtime.run(pizzaops, request).print_result()

# pizza_data.py: mock incident, team and restaurant data, identical for everyone
INCIDENTS = {
    "INC-1042": {
        "title": "checkout-api returning 500s",
        "running_for": "3 hours",
        "team": [("dana", "vegetarian"), ("li", "gluten-free"),
                 ("priya", "vegan"), ("sam", "no restrictions")],
        "meal_budget_usd": 60,
    },
}

RESTAURANTS = {
    "Crust Issues": {"eta_min": 25, "menu": [
        ("Margherita", 14, "vegetarian"),
        ("Pepperoni", 16, ""),
        ("Gluten-free Margherita", 18, "vegetarian, gluten-free"),
        ("Hawaiian (ham and pineapple)", 17, ""),
    ]},
    "The Pizza Cache": {"eta_min": 35, "menu": [
        ("Vegan Garden", 17, "vegan, vegetarian"),
        ("Four Cheese", 16, "vegetarian"),
        ("Pepperoni", 15, ""),
    ]},
    "Slice of Heaven": {"eta_min": 55, "menu": [
        ("Gluten-free Vegan Supreme", 19, "vegan, vegetarian, gluten-free"),
        ("Margherita", 13, "vegetarian"),
        ("Pepperoni", 15, ""),
    ]},
}

ORDERS = []


def _incident(incident_id):
    inc = INCIDENTS.get((incident_id or "").strip().upper())
    if inc is None:
        raise LookupError(f"No incident '{incident_id}'. Known: {', '.join(INCIDENTS)}.")
    return inc


def _restaurant(name):
    for key, value in RESTAURANTS.items():
        if key.lower() == (name or "").strip().lower():
            return key, value
    raise LookupError(f"No restaurant '{name}'. Options: {', '.join(RESTAURANTS)}.")


def incident_team(incident_id: str) -> str:
    try:
        inc = _incident(incident_id)
    except LookupError as e:
        return str(e)
    people = ", ".join(f"{name} ({diet})" for name, diet in inc["team"])
    return (f"{incident_id}: {inc['title']}, running for {inc['running_for']}. "
            f"On-call team: {people}.")


def meal_budget(incident_id: str) -> str:
    try:
        inc = _incident(incident_id)
    except LookupError as e:
        return str(e)
    return f"Meal budget for {incident_id}: ${inc['meal_budget_usd']} remaining."


def list_restaurants() -> str:
    return "; ".join(f"{name} (delivers in ~{r['eta_min']} min)"
                     for name, r in RESTAURANTS.items())


def menu(restaurant: str) -> str:
    try:
        name, r = _restaurant(restaurant)
    except LookupError as e:
        return str(e)
    items = "; ".join(f"{item} ${price}" + (f" [{tags}]" if tags else "")
                      for item, price, tags in r["menu"])
    return f"{name} menu: {items}."


def place_order(incident_id: str, restaurant: str, items: str, total_usd: float) -> str:
    try:
        inc = _incident(incident_id)
        name, r = _restaurant(restaurant)
    except LookupError as e:
        return str(e)
    if total_usd > inc["meal_budget_usd"]:
        return f"Rejected: ${total_usd} is over the ${inc['meal_budget_usd']} budget."
    inc["meal_budget_usd"] -= total_usd
    ORDERS.append((incident_id, name, items, total_usd))
    return (f"Order #{len(ORDERS)} placed at {name}: {items}. Total ${total_usd}. "
            f"Arrives in ~{r['eta_min']} min.")

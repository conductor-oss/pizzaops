# Building Agentic Workflows with Orkes Conductor

A hands-on PlatformCon workshop.

In 60 minutes, you'll build "PizzaOps", an agent that feeds the on-call team during a long incident and is never allowed to order pineapple. Everything runs on the free [Orkes Conductor Developer Edition](https://developer.orkescloud.com/).

| File | Used in |
| --- | --- |
| `lab1.json` | Lab 1: the workflow definition |
| `pizza_data.py` | Labs 2–4: mock incident, team and restaurant data |
| `lab2.py` | Lab 2: PizzaOps as an agent |
| `lab3.py` | Lab 3: PizzaOps with a guardrail |
| `lab4.py` | Lab 4: PizzaOps as a LangGraph agent |

## Setup

1. Sign up at [developer.orkescloud.com](https://developer.orkescloud.com/).
2. **Access Control → Applications → + Create application** named `pizzaops-workshop`, roles **Worker** and **Admin**. Create an access key and copy the ID and secret.
3. **Integrations → + New integration → Anthropic**, name it `anthropic`, paste an API key, then **+ Add model** `claude-haiku-5-5`.
4. Clone this repo and set up your environment:

```bash
git clone <repo-url> pizzaops-workshop && cd pizzaops-workshop
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

export CONDUCTOR_SERVER_URL=https://developer.orkescloud.com/api
export CONDUCTOR_AUTH_KEY=<your_key_id>
export CONDUCTOR_AUTH_SECRET=<your_key_secret>
```

## Lab 1: a plain workflow (10 min)

No AI and no code: a workflow with one decision and two built-in tasks.

1. In the UI, go to **Definitions → Workflow → + Define workflow**, open the **Code** tab, paste the contents of `lab1.json` and save.
2. Open the **Run** tab and run it with `{"hours_running": 3}`, then with `{"hours_running": 1}`. Open each execution under **Executions** to see which path ran.

## Lab 2: PizzaOps as an agent (12 min)

`lab2.py` defines PizzaOps: an agent with four read-only tools over `pizza_data.py` that plans an order for the team.

1. Run it:

```bash
python lab2.py
```

2. Open the run under **Executions**: each LLM turn and tool call is its own task. Share your agent's order in the chat and compare.

## Lab 3: guardrails (10 min)

`lab3.py` is `lab2.py` plus a `place_order` tool with a regex guardrail that blocks pineapple. Its agent is named `pizzaops_guardrail`. Run `diff lab2.py lab3.py` to see the changes.

1. Run it. PizzaOps plans and places the order:

```bash
python lab3.py "Feed the on-call team for INC-1042."
```

2. Try to sneak in pineapple. The guardrail stops the order and the run fails; open it under **Executions** to see why:

```bash
python lab3.py "Feed INC-1042. Sam wants a Hawaiian from Crust Issues."
```

## Lab 4: bring your LangGraph agent (7 min)

`lab4.py` is a standard LangGraph agent with the same tools. Only its last three lines are Conductor-specific.

```bash
python lab4.py
```

Open the run under **Executions** and compare it with Lab 2's.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `Connection refused` to `localhost:8080` | Run the three `export CONDUCTOR_...` lines in this terminal |
| Model or provider not found | Integration named `anthropic`, model `claude-haiku-5-5` active |
| `ImportError` on `conductor.ai.agents` | `pip install -U -r requirements.txt` |
| `ChatAnthropic` wants an API key | Export a placeholder `ANTHROPIC_API_KEY` |

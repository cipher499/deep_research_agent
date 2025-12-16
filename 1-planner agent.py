from pydantic import BaseModel
from agents import Agent

how_many_searches = 5

# System instructions for the agent
Instructions = f"You are a helpful research assistant. Given a query, come up with a set of web searches \
to perform to best answer the query. Output {how_many_searches} terms to query for."

# Structured Output: WebSearchItem
class WebSearchItem(BaseModel):
    reason: str
    "Your reasoning for why this search is important to the query."

    query: str
    "The search term to use for the web search."


# Structured Output: WebSearchPlan
class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem]
    "A list of web searches to perform to best answer the query."

# create the agent
planner = Agent(
    name="Planner Agent",
    instructions=Instructions,
    model="gpt-4o-mini",
    output_type=WebSearchPlan
)
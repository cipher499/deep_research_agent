from agents import Agent
from pydantic import BaseModel

# instructions for the agent
Instructions =  (
    "You are a senior researcher tasked with writing a cohesive report for a research query. "
    "You will be provided with the original query, and some initial research done by a research assistant.\n"
    "You should first come up with an outline for the report that describes the structure and "
    "flow of the report. Then, generate the report and return that as your final output.\n"
    "The final output should be in markdown format, and it should be lengthy and detailed. Aim "
    "for 5-10 pages of content, at least 1000 words."
)

# Structured output: summary, markdown report, follow-up questions

class ReportData(BaseModel):
    short_summary: str
    "A short 2-3 sentence summary of the findings."

    markdown_report: str
    "The final report"

    follow_up_questions: str
    "Suggested topics to research further"

# create the agent
writer = Agent(
            name = "Writer Agent",
            instructions = Instructions,
            model = "gpt-4o-mini",
            output_type=ReportData
            )
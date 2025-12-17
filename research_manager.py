from agents import Runner, trace, gen_trace_id
from search_agent import searcher
from planner_agent import planner, WebSearchItem, WebSearchPlan
from writer_agent import writer, ReportData
from email_agent import emailer
import asyncio

class ResearchManager:

    async def run(self, query: str):
        """ Run the deep research process, yielding the status updates and the final report"""
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):

            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}") # view trace
            yield(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}") # stream the trace back to the user
            print("Starting research...")

            search_plan = await self.plan_searches(query)
            yield("Searches planned. Starting to search...")

            search_results = await self.perform_searches(search_plan)
            yield("Searching done. Writing report...")

            report = await self.write_report(query, search_results)
            yield("Report written. Sending email...")

            await self.send_email(report)
            yield("Email sent. Research complete")
            yield report.markdown_report

    async def plan_searches(self, query: str) ->  WebSearchPlan:
        """Come up with a set of search queries and the reasons behind choosing them"""
        print("Planning searches...")

        result = await Runner.run(planner, f"Query: {query}")

        print(f"Will perform {len(result.final_output.searches)} searches")
        return result.final_output_as(WebSearchPlan)

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """Performs searches on the list of queries in the search plan"""
        print("Searching...")
        n_completed = 0
        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
        results = []

        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
            n_completed += 1
            print(f"Searching...{n_completed}/{len(tasks)} searches completed.")
            
        print("Finished searching")
        return results

    async def search(self, item: WebSearchItem) -> str | None:
        """Search the web for a given query"""
        input = f"Search query: {item.query}\n Reason for searching: {item.reason}"

        try:
            result = await Runner.run(searcher, input)
            return str(result.final_output)
        except Exception:
                return None
                
    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """Write the report based on the query and the search results."""
        print("Thinking about the report...")
        input = f"User query: {query} \n Summarized search results: {search_results}"

        result = await Runner.run(writer, input)

        print("Finished writting the report")
        return result.final_output_as(ReportData)

    async def send_email(self, report: ReportData) -> None:
        print("Writing email...")
        result = await Runner.run(
                emailer,
                report.markdown_report,
            )
        print("Email sent")
        return None
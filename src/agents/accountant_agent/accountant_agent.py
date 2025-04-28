from crewai import Agent
from src.agents.accountant_agent.accountant_tools import calculate_totals, generate_markdown_report
from src.llm_adapter import llm
class AccountantAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Accountant Agent",
            goal="Process structured invoice data and generate financial reports",
            backstory="You will be given path to structured invoice data, and your task is to calculate the totals and generate a financial report.",
            tools=[calculate_totals, generate_markdown_report],
            llm=llm,
            prompt_type="react",
            verbose=True
        )

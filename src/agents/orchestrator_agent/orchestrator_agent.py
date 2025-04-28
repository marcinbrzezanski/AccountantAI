from crewai import Agent
from src.agents.orchestrator_agent.orchestrator_tools import read_directory, process_invoice, generate_report
from src.llm_adapter import llm
class OrchestratorAgent(Agent):
    def __init__(self, directory_path: str = None):
        super().__init__(
            role="Orchestrator",
            goal=f"Orchestrate invoice processing pipeline. Check given directory: {directory_path} for invoices. Pay attention to number of invoices. Do not process invoice muiltiple times. Then delegate tasks to other agents.",
            backstory="Read invoices, process OCR & structuring, then summarize.",
            tools=[read_directory],
            llm=llm,
            prompt_type="react",
            verbose=True,
            allow_delegation=True,
        )
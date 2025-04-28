from agents.orchestrator_agent.orchestrator_agent import OrchestratorAgent
from agents.accountant_agent.accountant_agent import AccountantAgent
from agents.ocr_agent.ocr_agent import OCRAgent
from crewai import Task, Crew

def process_invoices(directory_path: str):
    orchestrator_agent = OrchestratorAgent(directory_path=directory_path)
    ocr_agent = OCRAgent()
    accountant_agent = AccountantAgent()

    task1 = Task(
        description="Find files in the directory",
        agent=orchestrator_agent,
        expected_output="List of file paths",
        inputs_schema={"directory_path": str},
    )

    task2 = Task(
        description="Extract, structure data from invoices and save as JSON's",
        agent=ocr_agent,
        expected_output="Path to structured invoice JSON files",
        inputs_schema={"file_path": str},
    )

    task3 = Task(
        description="Generate financial report from structured invoices saved in directory.",
        agent=accountant_agent,
        expected_output="Financial report",
    )

    crew = Crew(
        tasks=[task1, task2, task3],
        manager_agent=orchestrator_agent,
        agents=[ocr_agent, accountant_agent],
        verbose=True,
    )

    result = crew.kickoff(inputs={"directory_path": directory_path})
    print("Generated Report:", result)

if __name__ == "__main__":
    directory_path = r"C:\Users\Marcin\OneDrive\Pulpit\AccountantAI\invoices"
    process_invoices(directory_path)

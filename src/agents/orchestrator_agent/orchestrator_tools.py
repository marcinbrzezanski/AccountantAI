import os
from typing import List, Dict
from crewai.tools import tool
from crewai import Crew, Task
from src.agents.ocr_agent.ocr_agent import OCRAgent
from src.agents.accountant_agent.accountant_agent import AccountantAgent

@tool("read_directory")
def read_directory(directory_path: str) -> List[str]:
    """
    Read all files in a directory and return a list of file paths.
    """
    if not os.path.isdir(directory_path):
        raise NotADirectoryError(f"Not a directory: {directory_path}")
    matches = []
    for root, _, files in os.walk(directory_path):
        for name in files:
            if name.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf')):
                matches.append(os.path.join(root, name))
    return matches

@tool("process_invoice")
def process_invoice(file_path: str) -> Dict:
    """
    Process a single invoice file using OCR and structure the results.
    """
    task = Task(
        description=f"Process invoice {file_path}",
        agent=OCRAgent(),
        expected_output="Invoice JSON"
    )
    crew = Crew(agents=[OCRAgent()], tasks=[task], verbose=False)
    result = crew.kickoff(inputs={"file_path": file_path})
    return result[0]

@tool("generate_report")
def generate_report(invoices: List[Dict]) -> Dict:
    """
    Generate a report from structured invoices using the Accountant agent.
    Each invoice is a dictionary containing structured data.
    """
    task = Task(
        description="Generate report from structured invoices",
        agent=AccountantAgent(),
        expected_output="Report JSON"
    )
    crew = Crew(agents=[AccountantAgent()], tasks=[task], verbose=False)
    report = crew.kickoff(inputs={"invoices": invoices})
    return report[0]
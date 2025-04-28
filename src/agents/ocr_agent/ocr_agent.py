from crewai import Agent
from src.agents.ocr_agent.ocr_tools import ocr_tool, structure_ocr_results
from src.llm_adapter import llm
class OCRAgent(Agent):
    def __init__(self):
        super().__init__(
            role="OCR & Structuring Agent",
            goal="Extract and structure invoice data from images or PDFs.",
            backstory="You will perform OCR on invoice files and structure the results into the Invoice model.",
            tools=[ocr_tool, structure_ocr_results],
            llm=llm,
            prompt_type="react",
            verbose=True,
            allow_delegation=True
        )

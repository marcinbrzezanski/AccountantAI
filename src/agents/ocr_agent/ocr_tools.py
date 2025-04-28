import easyocr
import os
from crewai.tools import tool
from crewai.llm import LLM
from ...models.pydantic_models import Invoice
import json

@tool("ocr")
def ocr_tool(file_path: str) -> str:
    """
    Extract raw text from an invoice image or PDF using EasyOCR.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Brak pliku: {file_path}")

    reader = easyocr.Reader(['pl'], gpu=True)

    results = reader.readtext(file_path)

    extracted_text = "\n".join([text for (_, text, _) in results])
    
    return extracted_text

@tool("structure_ocr_results")
def structure_ocr_results(raw_text: str, original_filename: str = "invoice") -> dict:
    """
    Call LLM to structure the OCR results and save them as JSON in 'processed_invoices/'.
    """
    structured_data_provider = LLM(
        model="openai/gpt-4o-mini",
        temperature=0.8,
        top_p=0.9,
        frequency_penalty=0.1,
        presence_penalty=0.1,
        stop=["END"],
        seed=42,
        response_format=Invoice
    )

    prompt = f"""
    Przekształć poniższy tekst z faktury w ustrukturyzowane dane.
    Oto twoje surowe dane:
    {raw_text}
    """

    structured_data = structured_data_provider.call(prompt)

    output_dir = os.path.join(os.getcwd(), "processed_invoices")

    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{original_filename}.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(structured_data, f, ensure_ascii=False, indent=2)

    return output_path
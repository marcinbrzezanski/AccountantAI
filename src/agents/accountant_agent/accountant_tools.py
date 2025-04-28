import os
import json
from crewai.tools import tool

@tool('calculate_totals')
def calculate_totals() -> dict:
    """
    Calculate total net and gross amounts from structured invoice JSON files in the given directory.
    Returns total summary and detailed data for each invoice.
    """

    directory_path = r"C:\Users\Marcin\OneDrive\Pulpit\AccountantAI\processed_invoices"
    
    if not os.path.isdir(directory_path):
        raise NotADirectoryError(f"Directory not found: {directory_path}")

    total_net = 0.0
    total_gross = 0.0
    invoices_data = []

    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    invoice = json.load(f)

                if isinstance(invoice, str):
                    invoice = json.loads(invoice)

                invoice_total_net = 0.0
                invoice_total_gross = 0.0
                items = invoice.get('items', [])
                
                for item in items:
                    quantity = item.get('quantity', 0)
                    net_price = item.get('net_price', 0.0)
                    vat_rate = item.get('vat_rate', 0.0)

                    item_net_total = quantity * net_price
                    item_gross_total = item_net_total * (1 + vat_rate)

                    invoice_total_net += item_net_total
                    invoice_total_gross += item_gross_total

                total_net += invoice_total_net
                total_gross += invoice_total_gross

                # Collect structured invoice data
                invoices_data.append({
                    "invoice_number": invoice.get('invoice_number', 'N/A'),
                    "issue_date": invoice.get('issue_date', 'N/A'),
                    "seller": invoice.get('seller', {}).get('name', 'Unknown Seller'),
                    "buyer": invoice.get('buyer', {}).get('name', 'Unknown Buyer'),
                    "total_net": round(invoice_total_net, 2),
                    "total_gross": round(invoice_total_gross, 2)
                })

            except (json.JSONDecodeError, ValueError, KeyError) as e:
                print(f"Skipping file {filename} due to error: {e}")

    return {
        "summary": {
            "total_net": round(total_net, 2),
            "total_gross": round(total_gross, 2)
        },
        "invoices": invoices_data
    }

@tool('generate_markdown_report')
def generate_markdown_report(data: dict, output_file: str) -> str:
    """
    Generate a Markdown report from the invoice data and save it to a file.
    
    Args:
        data (dict): The invoice data output from 'calculate_totals'.
        output_file (str): Path to save the generated Markdown file.
    
    Returns:
        str: A confirmation message or error.
    """

    invoices = data.get('invoices', [])
    summary = data.get('summary', {})

    if not invoices:
        return "No invoices found to generate a report."

    markdown = "| Invoice Number | Issue Date | Seller | Buyer | Net Amount | Gross Amount |\n"
    markdown += "|:--------------|:-----------|:-------|:------|-----------:|-------------:|\n"

    for inv in invoices:
        markdown += (
            f"| {inv['invoice_number']} "
            f"| {inv['issue_date']} "
            f"| {inv['seller']} "
            f"| {inv['buyer']} "
            f"| {inv['total_net']:.2f} "
            f"| {inv['total_gross']:.2f} |\n"
        )

    markdown += "\n"
    markdown += f"**Total Net:** {summary.get('total_net', 0.0):.2f}  \n"
    markdown += f"**Total Gross:** {summary.get('total_gross', 0.0):.2f}  \n"

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown)
    except Exception as e:
        return f"Failed to save report: {e}"

    return f"Report successfully saved to {output_file}"

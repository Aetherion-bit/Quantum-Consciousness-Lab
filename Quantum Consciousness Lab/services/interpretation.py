from services.exports import create_pdf_report
from services.ai_commentary import explainable_commentary

def generate_report(data: dict, filename: str = "report.pdf"):
    """
    Generates a scientific report.
    """
    commentary = explainable_commentary(data)
    report_data = {
        "C(t)": data.get("C(t)", "N/A"),
        "C_sigma(t)": data.get("C_sigma(t)", "N/A"),
        "Commentary": commentary["commentary"]
    }
    create_pdf_report(report_data, filename)
    return {"status": "generated", "file": filename}

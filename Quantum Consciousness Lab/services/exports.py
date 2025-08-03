import csv
from fpdf import FPDF
from rdflib import Graph, Literal, RDF, URIRef
import numpy as np

def export_to_csv(data: list, filename: str = "export.csv"):
    """
    Exports data to CSV.
    """
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def export_to_jsonld(data: dict, filename: str = "export.jsonld"):
    """
    Exports data to JSON-LD.
    """
    g = Graph()
    session = URIRef("http://example.org/session/1")
    g.add((session, RDF.type, URIRef("http://example.org/Document")))
    for key, value in data.items():
        g.add((session, URIRef(f"http://example.org/{key}"), Literal(value)))
    g.serialize(destination=filename, format='json-ld')

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(200, 10, 'Quantum Consciousness Report', 0, 1, 'C')

def create_pdf_report(data: dict, filename: str = "report.pdf"):
    """
    Creates a PDF report.
    """
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    pdf.output(filename)

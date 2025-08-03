import shap
from transformers import pipeline

def explainable_commentary(data: dict) -> dict:
    """
    Generates and explains AI commentary.
    """
    nlp = pipeline("text-generation", model="distilbert-base-uncased")
    prompt = f"C(t): {data.get('C(t)', 'N/A')}, Phi_QM: {data.get('phi_qm', 'N/A')}"
    commentary = nlp(prompt, max_length=200)[0]["generated_text"]
    
    explainer = shap.Explainer(nlp)
    shap_values = explainer([prompt])
    return {"commentary": commentary, "shap_values": shap_values.values.tolist()}

import requests
import os
import json

# Backend URL - defaulting to 127.0.0.1 for faster Windows resolution
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

def analyze_contract(text, filename="upload.pdf"):
    """Call POST /analyze"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/analyze",
            json={"text": text, "filename": filename}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API Error: {str(e)}"}

def get_contracts(skip=0, limit=100):
    """Call GET /contracts"""
    try:
        response = requests.get(f"{API_BASE_URL}/contracts?skip={skip}&limit={limit}")
        response.raise_for_status()
        # The backend models.Contract has fields: id, filename, content_summary, upload_date, lifecycle_status, compliance_score, analysis_json
        # app.py expects a list of tuples or similar structure.
        # Let's return raw JSON list and let app.py adapt, or adapt here.
        # app.py expects: (id, filename, summary, date, status, score, json_str)
        data = response.json()
        adapted = []
        for c in data:
            adapted.append((
                c['id'],
                c['filename'],
                c['content_summary'],
                c['upload_date'],
                c['lifecycle_status'],
                c['compliance_score'],
                c['analysis_json'],
                c.get('contract_text', '') 
            ))
        return adapted
    except Exception as e:
        print(f"Failed to fetch contracts: {e}")
        return []

def chat_with_contract(contract_text, query):
    """Call POST /chat"""
    try:
        response = requests.post(f"{API_BASE_URL}/chat", json={"contract_text": contract_text, "query": query})
        response.raise_for_status()
        return response.json()['response']
    except Exception as e:
        return f"Error: {e}"

def compare_contracts(text_a, text_b):
    """Call POST /compare"""
    try:
        response = requests.post(f"{API_BASE_URL}/compare", json={"text_a": text_a, "text_b": text_b})
        response.raise_for_status()
        return response.json()['comparison_markdown']
    except Exception as e:
        return f"Error: {e}"

def audit_contract(text):
    """Call POST /audit"""
    try:
        response = requests.post(f"{API_BASE_URL}/audit", json={"contract_text": text})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def validate_security(action_type, user_data):
    """Call POST /security/validate"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/security/validate", 
            json={"action_type": action_type, "user_data": user_data}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Re-export extract functions as they are client-side processing (or could be moved to backend, but usually done on client before upload)
# Actually, the original analysis.py had extract_text_from_pdf. 
# So we still need analysis.py or a utils file for PDF extraction.

def translate_contract(text, target_language):
    """Call POST /translate"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/translate",
            json={"text": text, "target_language": target_language}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"translated_text": f"Error: {e}"}

def check_alerts(trigger_email=False):
    """Call POST /alerts/check"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/alerts/check",
            json={"trigger_email": trigger_email}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

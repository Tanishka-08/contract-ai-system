import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

candidates = [
    "gemini-1.5-pro-preview-12-2025",
    "gemini-1.5-flash",
    "gemini-1.5-pro-latest",
    "gemini-pro",
    "gemini-1.0-pro"
]

print(f"[INFO] Testing {len(candidates)} models with key: {api_key[:5]}...")

for model_name in candidates:
    print(f"\n[TESTING]: {model_name}")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say 'It works'")
        print(f"[SUCCESS] {model_name} is working.")
        print(f"Response: {response.text}")
        break 
    except Exception as e:
        print(f"[FAILED] {model_name}: {e}")

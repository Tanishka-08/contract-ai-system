import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

candidates = [
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-1.5-flash-001",
    "gemini-1.5-pro-001",
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro-latest",
    "gemini-1.0-pro",
    "gemini-pro",
    "gemini-pro-vision",
]

print(f"Checking API Key: {api_key[:5]}...{api_key[-5:] if api_key else 'None'}")

print("\n--- Testing Candidates ---")
working_model = None

for model_name in candidates:
    print(f"Testing {model_name}...", end=" ", flush=True)
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hi")
        print(f"✅ WORKS!")
        if working_model is None:
            working_model = model_name
    except Exception as e:
        print(f"❌ Failed: {e}")

print("\n--- Listing All Available Models (from API) ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")

if working_model:
    print(f"\nExample working model found: {working_model}")
else:
    print("\n❌ NO WORKING MODELS FOUND.")

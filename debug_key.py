import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("[ERROR] GOOGLE_API_KEY not found in .env")
    exit()

print(f"[INFO] Testing API Key: {api_key[:5]}...{api_key[-5:]}")
genai.configure(api_key=api_key)

print("\n--- 1. Testing Model Availability ---")
try:
    models = genai.list_models()
    found = False
    for m in models:
        # print(f"Found: {m.name}") # Uncomment to see all
        if 'generateContent' in m.supported_generation_methods:
            print(f"[OK] Available: {m.name}")
            if "gemini-1.5-pro-002" in m.name:
                found = True
            if "gemini-pro" in m.name:
                print(f"[INFO] gemini-pro is available.")
    
    if found:
        print("\n[OK] Target model 'gemini-1.5-pro-002' matches a known entry.")
    else:
        print("\n[WARN] Target model 'gemini-1.5-pro-002' NOT explicitly in list.")

except Exception as e:
    print(f"[ERROR] Error listing models: {e}")

print("\n--- 2. Testing Direct Generation ---")
target_model = 'gemini-1.5-pro-002'
print(f"Attempting to generate with: {target_model}")

try:
    model = genai.GenerativeModel(target_model)
    response = model.generate_content("Hello, system check.")
    print(f"[OK] Success! Response: {response.text}")
except Exception as e:
    print(f"[ERROR] Generation Failed: {e}")

    print("\n--- 3. Testing Fallback 'gemini-pro' ---")
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content("Hello, fallback check.")
        print(f"[OK] Fallback 'gemini-pro' Success! Response: {response.text}")
    except Exception as ex:
        print(f"[ERROR] Fallback also failed: {ex}")

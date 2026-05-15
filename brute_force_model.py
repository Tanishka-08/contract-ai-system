import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# All likely candidates including older ones
candidates = [
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-1.5-flash-001",
    "gemini-1.5-flash-002",
    "gemini-1.5-pro",
    "gemini-1.5-pro-latest",
    "gemini-1.5-pro-001",
    "gemini-1.5-pro-002",
    "gemini-1.0-pro",
    "gemini-pro",
    "examples/gemini-pro",
    "models/gemini-1.5-flash",
    "models/gemini-1.5-pro"
]

print("Starting Brute Force Check...")
found = False
with open("working_model.txt", "w", encoding="utf-8") as f:
    for model_name in candidates:
        print(f"Testing {model_name}...")
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Ping")
            print(f"✅ WORKS: {model_name}")
            f.write(model_name)
            found = True
            break
        except Exception as e:
            print(f"❌ {model_name}: {str(e)[:100]}")

    if not found:
        # Last ditch: try listing and testing whatever comes back
        print("Checking listed models...")
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    try:
                        name = m.name # usually models/foo
                        print(f"Testing listed {name}...")
                        model = genai.GenerativeModel(name)
                        response = model.generate_content("Ping")
                        print(f"✅ WORKS: {name}")
                        f.write(name)
                        found = True
                        break
                    except:
                        pass
        except:
            pass

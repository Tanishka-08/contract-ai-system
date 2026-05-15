import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

try:
    with open("my_models.txt", "w", encoding="utf-8") as f:
        f.write("--- MODELS ---\n")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                f.write(f"{m.name}\n")
        f.write("--- END ---\n")
    print("Models listed to my_models.txt")
except Exception as e:
    print(f"Error: {e}")

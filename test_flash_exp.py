import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

model_name = "gemini-2.0-flash-exp"
print(f"Testing {model_name}...")
try:
    model = genai.GenerativeModel(model_name)
    response = model.generate_content("Ping")
    print(f"✅ WORKS! {model_name}")
except Exception as e:
    print(f"❌ Failed: {e}")

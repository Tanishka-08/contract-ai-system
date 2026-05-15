import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

model_name = "gemini-1.5-flash"

try:
    print(f"Testing model: {model_name}...")
    model = genai.GenerativeModel(model_name)
    response = model.generate_content("Hello")
    print(f"✅ Success! Response: {response.text}")
except Exception as e:
    print(f"❌ Failed: {e}")

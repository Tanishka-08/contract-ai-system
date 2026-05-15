
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

model_name = 'gemini-1.5-flash'
print(f"Testing generation with {model_name}...")

try:
    model = genai.GenerativeModel(model_name)
    response = model.generate_content("Say hello")
    print(f"Success! Response: {response.text}")
except Exception as e:
    print(f"Failed with {model_name}: {e}")

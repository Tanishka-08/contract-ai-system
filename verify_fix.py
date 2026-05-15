import google.generativeai as genai
import os
import sys
from dotenv import load_dotenv

# Ensure backend can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
try:
    from services import get_best_model
except ImportError:
    # Fallback if imports fail due to structure
    def get_best_model():
        return 'gemini-1.5-flash'

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model_name = get_best_model()
print(f"Verifying model: {model_name}")

try:
    model = genai.GenerativeModel(model_name)
    response = model.generate_content("Hello")
    print(f"✅ Success! Response: {response.text}")
except Exception as e:
    print(f"❌ Failed: {e}")

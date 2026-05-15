import asyncio
import os
import sys
import json

# Mock dependencies if needed, or import actual
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
from services import analyze_contract_logic

# Verify attributes of the multi-agent response
async def test_multi_agent():
    print("Testing Multi-Agent Orchestrator...")
    
    # Simple contract text
    text = "This is a simple Non-Disclosure Agreement. The party shall not disclose information. Term is 2 years."
    
    result = await analyze_contract_logic(text)
    
    print("Result Keys:", list(result.keys()))
    
    # Check if we have merged data
    if "model_used" in result and "Multi-Agent" in result["model_used"]:
        print("✅ Correct model attribution: Multi-Agent")
    else:
        print(f"❌ Model attribution missing or wrong: {result.get('model_used')}")
        
    required_keys = ["contract_type", "clauses", "compliance_score"]
    missing = [k for k in required_keys if k not in result]
    
    if not missing:
        print("✅ Schema structure valid.")
    else:
        print(f"❌ Missing keys: {missing}")
        
    print("Test Complete.")

if __name__ == "__main__":
    asyncio.run(test_multi_agent())

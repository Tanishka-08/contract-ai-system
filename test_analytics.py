import json
from analytics import generate_analytics_report

# Mock Data
mock_contracts = [
    {
        "id": "C001",
        "contract_type": "NDA",
        "compliance_score": 95,
        "upload_date": "2025-11-15",
        "contract_text": "This Non-Disclosure Agreement shall expire on 2026-02-15...", # Expiring soon (13 days from 2026-02-02)
        "highlight_summary": {"high_risk_count": 0, "medium_risk_count": 1},
        "clauses": [{"clause_name": "Confidentiality", "risk_level": "Low"}, {"clause_name": "term", "risk_level": "Medium"}]
    },
    {
        "id": "C002",
        "contract_type": "Employment",
        "compliance_score": 82,
        "upload_date": "2025-01-10",
        "contract_text": "Employment is at-will. Start date: Jan 10 2025.", # No expiry explicit, will be predicted
        "highlight_summary": {"high_risk_count": 1, "medium_risk_count": 2},
        "clauses": [{"clause_name": "Non-Compete", "risk_level": "High"}]
    },
    {
        "id": "C003",
        "contract_type": "SaaS",
        "compliance_score": 60,
        "upload_date": "2024-05-20",
        "contract_text": "Service agreement valid until 2025-05-20.", # Expired
        "highlight_summary": {"high_risk_count": 3, "medium_risk_count": 0},
        "clauses": [{"clause_name": "Liability Cap", "risk_level": "High"}, {"clause_name": "Data Privacy", "risk_level": "High"}]
    },
    {
        "id": "C004",
        "contract_type": "Employment",
        "compliance_score": 88,
        "upload_date": "2026-01-05",
        "contract_text": "Term: Infinite", 
        "highlight_summary": {"high_risk_count": 0, "medium_risk_count": 0},
        "clauses": []
    },
    {
        "id": "C005",
        "contract_type": "NDA",
        "compliance_score": 90,
        "upload_date": "2026-01-20",
        "contract_text": "Expiry: 2027-01-20", # Active, future
        "highlight_summary": {"high_risk_count": 0, "medium_risk_count": 0},
        "clauses": []
    }
]

print("Running Analytics on Mock Data...")
report = generate_analytics_report(mock_contracts)

print("\n--- JSON OUTPUT ---")
print(json.dumps(report, indent=2))

# Basic Assertions
assert len(report['trend_analysis']['risk_trends']) > 0
assert len(report['expiry_analysis']['expired_contracts']) == 1 # C003
assert len(report['expiry_analysis']['expiring_within_30_days']) == 1 # C001
assert len(report['insights']) >= 1

print("\nTests Passed!")

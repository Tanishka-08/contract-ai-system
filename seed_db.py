import sqlite3
import json
import datetime
DB_NAME = "contracts.db"

# Mock Data (from test_analytics.py)
mock_contracts = [
    {
        "filename": "Review_NDA_2025.pdf",
        "contract_type": "NDA",
        "compliance_score": 95,
        "upload_date": "2025-11-15 10:00:00",
        "contract_text": "This Non-Disclosure Agreement shall expire on 2026-02-15...", 
        "highlight_summary": {"high_risk_count": 0, "medium_risk_count": 1},
        "clauses": [{"clause_name": "Confidentiality", "risk_level": "Low"}, {"clause_name": "term", "risk_level": "Medium"}]
    },
    {
        "filename": "Employee_JohnDoe.pdf",
        "contract_type": "Employment",
        "compliance_score": 82,
        "upload_date": "2025-01-10 09:30:00",
        "contract_text": "Employment is at-will. Start date: Jan 10 2025.", 
        "highlight_summary": {"high_risk_count": 1, "medium_risk_count": 2},
        "clauses": [{"clause_name": "Non-Compete", "risk_level": "High"}]
    },
    {
        "filename": "Legacy_SaaS_Agreement.docx",
        "contract_type": "SaaS",
        "compliance_score": 60,
        "upload_date": "2024-05-20 14:00:00",
        "contract_text": "Service agreement valid until 2025-05-20.", 
        "highlight_summary": {"high_risk_count": 3, "medium_risk_count": 0},
        "clauses": [{"clause_name": "Liability Cap", "risk_level": "High"}, {"clause_name": "Data Privacy", "risk_level": "High"}]
    },
    {
        "filename": "New_Hire_Draft.pdf",
        "contract_type": "Employment",
        "compliance_score": 88,
        "upload_date": "2026-01-05 11:15:00",
        "contract_text": "Term: Infinite. Standard employment terms.", 
        "highlight_summary": {"high_risk_count": 0, "medium_risk_count": 0},
        "clauses": []
    },
    {
        "filename": "Vendor_NDA_2026.pdf",
        "contract_type": "NDA",
        "compliance_score": 90,
        "upload_date": "2026-01-20 16:45:00",
        "contract_text": "Expiry: 2027-01-20. Mutual protection of data.", 
        "highlight_summary": {"high_risk_count": 0, "medium_risk_count": 0},
        "clauses": []
    }
]

def seed():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    print(f"Connected to {DB_NAME}...")
    
    # Ensure table exists (just in case)
    c.execute('''
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            content_summary TEXT,
            upload_date TIMESTAMP,
            lifecycle_status TEXT,
            compliance_score TEXT,
            analysis_json TEXT,
            contract_text TEXT
        )
    ''')

    count = 0
    for m in mock_contracts:
        # Prepare the full JSON blob analysis.analyze_contract would return
        # We need to preserve the specific structure including the text for the newly integrated app to read it
        analysis_json = {
            "contract_type": m['contract_type'],
            "contract_summary": f"Simulated analysis for {m['filename']}",
            "lifecycle_status": "Active" if m['compliance_score'] > 70 else "Expired",
            "compliance_score": m['compliance_score'],
            "document_source": "Digital (Mock)",
            "key_clauses_summary": [c['clause_name'] for c in m['clauses']],
            "clauses": m['clauses'],
            "highlight_summary": m['highlight_summary'],
            "contract_text": m['contract_text'] # Important for regex expiry
        }
        
        c.execute('''
            INSERT INTO contracts (filename, content_summary, upload_date, lifecycle_status, compliance_score, analysis_json, contract_text)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            m['filename'], 
            m['contract_text'], 
            m['upload_date'], 
            analysis_json['lifecycle_status'], 
            str(m['compliance_score']), 
            json.dumps(analysis_json),
            m['contract_text']
        ))
        count += 1
        
    conn.commit()
    conn.close()
    print(f"Success! Seeded {count} historical contracts into the database.")

if __name__ == "__main__":
    seed()

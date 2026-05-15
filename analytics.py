import json
import re
from datetime import datetime, timedelta
from collections import Counter, defaultdict

# Current system date for reference
CURRENT_DATE = datetime(2026, 2, 2)

def parse_date(date_str):
    """
    Parses date/time strings into datetime objects.
    Supports ISO formats and common DD/MM/YYYY text formats.
    """
    if not date_str:
        return None
    try:
        # Try ISO format first
        return datetime.fromisoformat(date_str)
    except ValueError:
        pass
    
    # Try other common formats
    formats = [
        "%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%d/%m/%Y", 
        "%B %d, %Y", "%d %B %Y", "%Y/%m/%d"
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None

def extract_expiry_date(text):
    """
    Attempts to detect an expiry/termination date from contract text using Regex.
    """
    # Patterns for finding dates near "expiry", "termination", "end date"
    patterns = [
        # ISO Format YYYY-MM-DD
        r"(?:expir\w*|terminat\w*|end)\s+(?:date|period|on)?\s*[:\-]?\s*(\d{4}[-/]\d{1,2}[-/]\d{1,2})",
        # Common DD-MM-YYYY or MM-DD-YYYY
        r"(?:expir\w*|terminat\w*|end)\s+(?:date|period|on)?\s*[:\-]?\s*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})",
        # Wordy dates
        r"(?:expir\w*|terminat\w*|end)\s+(?:date|period|on)?\s*[:\-]?\s*(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})",
        # Valid until
        r"(?:valid|effective)\s+until\s+(\d{4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}[-/]\d{1,2}[-/]\d{2,4})"
    ]
    
    for pat in patterns:
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            date_str = match.group(1)
            parsed = parse_date(date_str)
            if parsed:
                return parsed
    return None

def predict_expiry(contract):
    """
    Predicts expiry based on historical patterns or contract type defaults if not found.
    (Simplified logic for demonstration)
    """
    c_type = contract.get('contract_type', 'General').lower()
    upload_date = parse_date(contract.get('upload_date'))
    if not upload_date:
        upload_date = CURRENT_DATE

    # Default durations in days
    defaults = {
        'employment': 365 * 2, # Assume 2 year default view for analysis
        'nda': 365,
        'rental': 365,
        'saas': 365,
        'general': 365
    }
    
    days = defaults.get(c_type, 365)
    predicted_date = upload_date + timedelta(days=days)
    return predicted_date, f"Predicted based on {c_type} typical duration ({days} days)"

def generate_analytics_report(contracts):
    """
    Main function to analyze a list of contract dictionaries and return the structured JSON report.
    """
    report = {
        "trend_analysis": {
            "average_compliance_over_time": [],
            "risk_trends": [],
            "most_common_risky_clauses": []
        },
        "compliance_comparison": {
            "by_contract_type": [],
            "time_based_comparison": []
        },
        "expiry_analysis": {
            "expiring_within_30_days": [],
            "expired_contracts": [],
            "predicted_upcoming_expiries": []
        },
        "insights": [],
        "alerts": []
    }

    # Data aggregators
    compliance_by_month = defaultdict(list)
    risk_by_month = defaultdict(lambda: {"high": 0, "medium": 0})
    risky_clauses_counter = Counter()
    compliance_by_type = defaultdict(list)
    
    # Expiry Lists
    expiring_soon = []
    expired = []
    upcoming = []

    for contract in contracts:
        # data extraction
        c_score = contract.get('compliance_score', 0)
        c_type = contract.get('contract_type', 'Unclassified')
        c_text = contract.get('contract_text', '')
        u_date_str = contract.get('upload_date')
        u_date = parse_date(u_date_str) if u_date_str else CURRENT_DATE
        
        # 1. Trend Analysis Helpers
        month_key = u_date.strftime("%Y-%m")
        compliance_by_month[month_key].append(c_score)
        
        # Risk counts
        # Assuming contract['risk_levels'] is a dict like {'High': 2, 'Medium': 5} or similar provided summary
        # Or parsing from 'clauses' if available. 
        # Using keys from prompt: "risk_levels"
        r_levels = contract.get('risk_levels', {})
        # Handle if risk_levels is just a string or list, but assuming dict based on typical structure
        # If it's the structure from analysis.py: highlight_summary: {high_risk_count, ...}
        # Adapting to flexible input:
        h_count = r_levels.get('High', 0) if isinstance(r_levels, dict) else 0
        m_count = r_levels.get('Medium', 0) if isinstance(r_levels, dict) else 0
        
        # Alternative: look for 'highlight_summary' from our previous schema
        if 'highlight_summary' in contract:
            h_count = contract['highlight_summary'].get('high_risk_count', 0)
            m_count = contract['highlight_summary'].get('medium_risk_count', 0)

        risk_by_month[month_key]['high'] += h_count
        risk_by_month[month_key]['medium'] += m_count

        # Risky Clauses
        # Assuming contract['clauses'] exists and has risk
        if 'clauses' in contract and isinstance(contract['clauses'], list):
            for clause in contract['clauses']:
                if isinstance(clause, dict) and clause.get('risk_level') in ['High', 'Medium']:
                    risky_clauses_counter[clause.get('clause_name', 'Unknown')] += 1
        
        # 2. Compliance Comparison Helpers
        compliance_by_type[c_type].append(c_score)

        # 3. Expiry Analysis
        expiry_date = extract_expiry_date(c_text)
        is_predicted = False
        prediction_reason = ""
        
        if not expiry_date:
            expiry_date, prediction_reason = predict_expiry(contract)
            is_predicted = True
        
        days_diff = (expiry_date - CURRENT_DATE).days
        
        expiry_info = {
            "contract_id": contract.get("id", "Unknown"),
            "contract_type": c_type,
            "expiry_date": expiry_date.strftime("%Y-%m-%d"),
            "is_predicted": is_predicted
        }

        if days_diff < 0:
            report['expiry_analysis']['expired_contracts'].append(expiry_info)
            if not is_predicted: # High priority alert
                 report['alerts'].append(f"Contract {expiry_info['contract_id']} ({c_type}) has EXPIRED on {expiry_info['expiry_date']}.")
        elif 0 <= days_diff <= 30:
            report['expiry_analysis']['expiring_within_30_days'].append(expiry_info)
            report['alerts'].append(f"Contract {expiry_info['contract_id']} ({c_type}) is expiring soon on {expiry_info['expiry_date']}.")
        else:
            if is_predicted:
                expiry_info['reason'] = prediction_reason
                report['expiry_analysis']['predicted_upcoming_expiries'].append(expiry_info)

    # --- POPULATE REPORT ---

    # Trend: Avg Compliance Over Time
    sorted_months = sorted(compliance_by_month.keys())
    for m in sorted_months:
        scores = compliance_by_month[m]
        avg = sum(scores) / len(scores) if scores else 0
        report['trend_analysis']['average_compliance_over_time'].append({
            "period": m,
            "average_score": round(avg, 2)
        })

    # Trend: Risk Trends
    for m in sorted_months:
        report['trend_analysis']['risk_trends'].append({
            "period": m,
            "high_risk_count": risk_by_month[m]['high'],
            "medium_risk_count": risk_by_month[m]['medium']
        })

    # Trend: Most Common Risky Clauses (Top 5)
    for name, count in risky_clauses_counter.most_common(5):
        report['trend_analysis']['most_common_risky_clauses'].append({
            "clause_name": name,
            "count": count
        })

    # Comparison: By Contract Type
    for c_type, scores in compliance_by_type.items():
        avg = sum(scores) / len(scores) if scores else 0
        report['compliance_comparison']['by_contract_type'].append({
            "contract_type": c_type,
            "average_compliance_score": round(avg, 2)
        })
    
    # Comparison: Time Based (Quarterly - derived from monthly)
    # Simplified aggregation for demo
    report['compliance_comparison']['time_based_comparison'] = report['trend_analysis']['average_compliance_over_time']

    # Insights Generation
    # 1. Overall score
    all_scores = [s for sublist in compliance_by_month.values() for s in sublist]
    global_avg = sum(all_scores) / len(all_scores) if all_scores else 0
    report['insights'].append(f"Overall average compliance score across all contracts is {global_avg:.1f}/100.")

    # 2. Risk Insight
    total_high_risk = sum(r['high'] for r in risk_by_month.values())
    if total_high_risk > 0:
        report['insights'].append(f"Identified {total_high_risk} cumulative high-risk clauses that require immediate attention.")

    # 3. Type Insight
    if report['compliance_comparison']['by_contract_type']:
        best_type = max(report['compliance_comparison']['by_contract_type'], key=lambda x: x['average_compliance_score'])
        worst_type = min(report['compliance_comparison']['by_contract_type'], key=lambda x: x['average_compliance_score'])
        report['insights'].append(f"{best_type['contract_type']} contracts have the highest compliance ({best_type['average_compliance_score']}), while {worst_type['contract_type']} lag behind ({worst_type['average_compliance_score']}).")

    return report

if __name__ == "__main__":
    # Simple self-test if run directly
    print("Analytics module loaded. Run 'test_analytics.py' to verify.")

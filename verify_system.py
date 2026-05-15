import sqlite3
import os
import sys

def check_db():
    db_path = "contracts.db"
    if not os.path.exists(db_path):
        print("❌ contracts.db not found!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Check rows
        c.execute("SELECT Count(*) FROM contracts")
        count = c.fetchone()[0]
        print(f"✅ Database contains {count} contracts.")
        
        # Check columns
        c.execute("PRAGMA table_info(contracts)")
        cols = [info[1] for info in c.fetchall()]
        print(f"ℹ️  Columns: {cols}")
        
        if "contract_text" in cols:
            print("✅ 'contract_text' column exists.")
        else:
            print("❌ 'contract_text' column MISSING!")
            return False
            
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def check_requirements():
    try:
        import streamlit
        import google.generativeai
        import PyPDF2
        import docx
        print("✅ Core dependencies available.")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

if __name__ == "__main__":
    print("--- System Verification ---")
    reqs = check_requirements()
    db = check_db()
    
    if reqs and db:
        print("\n🎉 System is repaired and ready!")
        print("To run the application:")
        print("1. Open a terminal and run the backend:")
        print("   uvicorn backend.main:app --reload")
        print("2. Open another terminal and run the frontend:")
        print("   streamlit run app.py")
    else:
        print("\n⚠️  System verification FAILED.")

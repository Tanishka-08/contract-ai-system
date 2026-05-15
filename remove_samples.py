import sqlite3
import os

DB_NAME = "contracts.db"

# The specific sample files we added
SAMPLES = [
    "Review_NDA_2025.pdf",
    "Employee_JohnDoe.pdf",
    "Legacy_SaaS_Agreement.docx",
    "New_Hire_Draft.pdf",
    "Vendor_NDA_2026.pdf"
]

def remove_samples():
    if not os.path.exists(DB_NAME):
        print("Database not found.")
        return

    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        
        print(f"Targeting samples: {SAMPLES}")
        
        # Build the placeholder string
        placeholders = ', '.join('?' for _ in SAMPLES)
        query = f"DELETE FROM contracts WHERE filename IN ({placeholders})"
        
        c.execute(query, SAMPLES)
        rows_deleted = c.rowcount
        
        conn.commit()
        conn.close()
        
        if rows_deleted > 0:
            print(f"✅ Success: Removed {rows_deleted} sample contracts.")
        else:
            print("ℹ️  No sample contracts found to delete.")
            
    except Exception as e:
        print(f"Error removing samples: {e}")

if __name__ == "__main__":
    remove_samples()

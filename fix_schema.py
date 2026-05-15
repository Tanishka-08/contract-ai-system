import sqlite3
from seed_db import DB_NAME

def fix():
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        print("Attempting to add column...")
        try:
            c.execute("ALTER TABLE contracts ADD COLUMN contract_text TEXT")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("Column already exists.")
            else:
                raise e
        
        print("Clearing table...")
        c.execute("DELETE FROM contracts")
        
        conn.commit()
        print("Schema fixed and table cleared.")
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix()

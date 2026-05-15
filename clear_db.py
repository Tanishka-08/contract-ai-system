import sqlite3
import os

DB_NAME = "contracts.db"

def clear_db():
    if not os.path.exists(DB_NAME):
        print("Database not found.")
        return

    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("DELETE FROM contracts")
        c.execute("DELETE FROM sqlite_sequence WHERE name='contracts'") # Reset ID counter
        conn.commit()
        
        # Verify
        c.execute("SELECT Count(*) FROM contracts")
        count = c.fetchone()[0]
        conn.close()
        
        if count == 0:
            print("✅ Success: All contracts have been removed from the database.")
        else:
            print(f"❌ Error: {count} contracts still remain.")
            
    except Exception as e:
        print(f"Error clearing database: {e}")

if __name__ == "__main__":
    clear_db()

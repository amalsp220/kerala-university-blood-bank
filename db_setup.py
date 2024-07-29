import sqlite3

def create_db():
    conn = sqlite3.connect('blood_bank.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS donors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        blood_group TEXT,
        department TEXT,
        contact_number TEXT,
        status TEXT,
        last_donation_date DATE
    )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
    print("Database and table created successfully.")

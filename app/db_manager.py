import sqlite3

DB_PATH = "data/database.db"

def initialize_database():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Create knowledge base table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            type TEXT NOT NULL
        )
    """)

    # Create interaction logs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            contact_info TEXT,
            query TEXT,
            resolution TEXT,
            status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()

def add_to_knowledge_base(category, question, answer, type_):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO knowledge_base (category, question, answer, type) VALUES (?, ?, ?, ?)",
                   (category, question, answer, type_))
    connection.commit()
    connection.close()

def search_knowledge_base(query):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM knowledge_base WHERE question LIKE ? OR answer LIKE ?", (f"%{query}%", f"%{query}%"))
    results = cursor.fetchall()
    connection.close()
    return results

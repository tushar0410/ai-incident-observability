import sqlite3

DB_PATH = "incidents.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        metric TEXT,
        value REAL,
        mean REAL,
        std REAL
    )
    """)
    
    conn.commit()
    conn.close()

def insert_incident(incident):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO incidents (timestamp, metric, value, mean, std)
    VALUES (?, ?, ?, ?, ?)
    """, (
        incident["timestamp"],
        incident["metric"],
        incident["value"],
        incident["mean"],
        incident["std"]
    ))
    
    conn.commit()
    conn.close()

def get_all_incidents():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM incidents ORDER BY id DESC")
    rows = cursor.fetchall()
    
    conn.close()
    
    return rows

import sqlite3
import time
import mh_z19
from datetime import datetime

# === Configuration ===
DB_FILE = 'co2_data.db'
CO2_THRESHOLD = 1000  # for optional future use

def initialize_database():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS co2_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                co2 INTEGER
            )
        ''')
        conn.commit()
        print("Database initialized.")

def write_to_db(timestamp, co2_value):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO co2_readings (timestamp, co2) VALUES (?, ?)', (timestamp, co2_value))
        conn.commit()

def read_co2():
    data = mh_z19.read()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if data is None:
        return timestamp, None
    return timestamp, data.get('co2')

def log_co2():
    initialize_database()
    try:
        while True:
            timestamp, co2 = read_co2()
            if co2 is not None:
                write_to_db(timestamp, co2)
                print(f"{timestamp};{co2} ppm")
            else:
                print(f"{timestamp};Error reading CO₂")
            time.sleep(10)
    except Exception as e:
        print(f"CO₂ logging interrupted due to an error: {e}")

if __name__ == "__main__":
    log_co2()
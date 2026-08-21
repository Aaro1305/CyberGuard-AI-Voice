import sqlite3
import os
from datetime import datetime

DB_FILE = "cyberguard_history.db"

def get_connection(db_path=DB_FILE):
    """
    Establishes and returns a connection to the SQLite database.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enables accessing columns by name like dictionary keys
    return conn

def init_db(db_path=DB_FILE):
    """
    Initializes the SQLite database and creates the 'scans' table if it does not exist.
    Handles column migrations if schema expands.
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            verdict TEXT NOT NULL,
            confidence REAL NOT NULL,
            risk_level TEXT,
            file_path TEXT,
            spectral_flatness TEXT,
            zero_crossing_rate TEXT,
            mfcc_mean TEXT,
            scan_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Auto-migration check for existing databases
    cursor.execute("PRAGMA table_info(scans)")
    columns = [row['name'] for row in cursor.fetchall()]
    if 'spectral_flatness' not in columns:
        cursor.execute("ALTER TABLE scans ADD COLUMN spectral_flatness TEXT")
    if 'zero_crossing_rate' not in columns:
        cursor.execute("ALTER TABLE scans ADD COLUMN zero_crossing_rate TEXT")
    if 'mfcc_mean' not in columns:
        cursor.execute("ALTER TABLE scans ADD COLUMN mfcc_mean TEXT")
        
    conn.commit()
    conn.close()

def save_scan(filename, verdict, confidence, risk_level=None, file_path=None, 
              spectral_flatness=None, zero_crossing_rate=None, mfcc_mean=None, db_path=DB_FILE):
    """
    Saves a complete audio scan result into the database using parameterized queries.
    Returns the ID of the newly inserted record.
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    # Ensure database table exists before saving
    init_db(db_path)
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    query = """
        INSERT INTO scans (filename, verdict, confidence, risk_level, file_path, 
                           spectral_flatness, zero_crossing_rate, mfcc_mean, scan_timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    cursor.execute(query, (filename, verdict, confidence, risk_level, file_path, 
                           spectral_flatness, zero_crossing_rate, mfcc_mean, current_time))
    scan_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    return scan_id

def get_all_scans(db_path=DB_FILE):
    """
    Retrieves all past audio scans ordered by most recent first.
    Returns a list of dictionaries representing each scan.
    """
    init_db(db_path)
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    query = """
        SELECT id, filename, verdict, confidence, risk_level, file_path, 
               spectral_flatness, zero_crossing_rate, mfcc_mean, scan_timestamp 
        FROM scans ORDER BY id DESC
    """
    cursor.execute(query)
    
    rows = cursor.fetchall()
    conn.close()
    
    # Convert sqlite3.Row objects to standard Python dictionaries
    return [dict(row) for row in rows]

def delete_scan(scan_id, db_path=DB_FILE):
    """
    Deletes a specific scan record from the database by its ID using parameterized query.
    Returns True if a row was deleted, False otherwise.
    """
    init_db(db_path)
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    query = "DELETE FROM scans WHERE id = ?"
    cursor.execute(query, (scan_id,))
    
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    
    return rows_affected > 0

def clear_all_scans(db_path=DB_FILE):
    """
    Deletes all scan records from the database.
    """
    init_db(db_path)
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM scans")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Test initialization
    init_db()
    print("Database schema updated and initialized successfully!")

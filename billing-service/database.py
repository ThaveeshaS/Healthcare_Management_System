import sqlite3
from models import BillCreate, BillUpdate

DB_FILE = "bills.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            status TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_all():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bills")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_by_id(bid: int):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bills WHERE id = ?", (bid,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def create(bill: BillCreate):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bills (patient_id, amount, status, date)
        VALUES (?, ?, ?, ?)
    ''', (bill.patient_id, bill.amount, bill.status, bill.date.isoformat()))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return get_by_id(new_id)

def update(bid: int, bill: BillUpdate):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    updates = []
    values = []
    if bill.patient_id is not None:
        updates.append("patient_id = ?")
        values.append(bill.patient_id)
    if bill.amount is not None:
        updates.append("amount = ?")
        values.append(bill.amount)
    if bill.status is not None:
        updates.append("status = ?")
        values.append(bill.status)
    if bill.date is not None:
        updates.append("date = ?")
        values.append(bill.date.isoformat())
    if not updates:
        return get_by_id(bid)
    values.append(bid)
    query = f"UPDATE bills SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    return get_by_id(bid)

def delete(bid: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bills WHERE id = ?", (bid,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

init_db()
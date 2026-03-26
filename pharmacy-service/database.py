import sqlite3
from models import MedicineCreate, MedicineUpdate

DB_FILE = "pharmacy.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_name TEXT NOT NULL,
            category TEXT NOT NULL,
            dosage TEXT NOT NULL,
            expiry_date TEXT NOT NULL,
            price REAL NOT NULL,
            doctor_note TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_all():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicines")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_by_id(mid: int):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicines WHERE id = ?", (mid,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def create(med: MedicineCreate):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO medicines (medicine_name, category, dosage, expiry_date, price, doctor_note)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (med.medicine_name, med.category, med.dosage, med.expiry_date.isoformat(), med.price, med.doctor_note))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return get_by_id(new_id)

def update(mid: int, med: MedicineUpdate):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    updates = []
    values = []
    if med.medicine_name is not None:
        updates.append("medicine_name = ?")
        values.append(med.medicine_name)
    if med.category is not None:
        updates.append("category = ?")
        values.append(med.category)
    if med.dosage is not None:
        updates.append("dosage = ?")
        values.append(med.dosage)
    if med.expiry_date is not None:
        updates.append("expiry_date = ?")
        values.append(med.expiry_date.isoformat())
    if med.price is not None:
        updates.append("price = ?")
        values.append(med.price)
    if med.doctor_note is not None:
        updates.append("doctor_note = ?")
        values.append(med.doctor_note)
    if not updates:
        return get_by_id(mid)
    values.append(mid)
    query = f"UPDATE medicines SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    return get_by_id(mid)

def delete(mid: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medicines WHERE id = ?", (mid,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

init_db()
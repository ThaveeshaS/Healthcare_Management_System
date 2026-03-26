import sqlite3
from models import Patient, PatientCreate, PatientUpdate

DB_FILE = "patients.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_all():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_by_id(pid: int):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE id = ?", (pid,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def create(patient: PatientCreate):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO patients (name, age, gender, phone, address)
        VALUES (?, ?, ?, ?, ?)
    ''', (patient.name, patient.age, patient.gender, patient.phone, patient.address))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return get_by_id(new_id)

def update(pid: int, patient: PatientUpdate):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Build dynamic update query
    updates = []
    values = []
    if patient.name is not None:
        updates.append("name = ?")
        values.append(patient.name)
    if patient.age is not None:
        updates.append("age = ?")
        values.append(patient.age)
    if patient.gender is not None:
        updates.append("gender = ?")
        values.append(patient.gender)
    if patient.phone is not None:
        updates.append("phone = ?")
        values.append(patient.phone)
    if patient.address is not None:
        updates.append("address = ?")
        values.append(patient.address)
    if not updates:
        return get_by_id(pid)
    values.append(pid)
    query = f"UPDATE patients SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    return get_by_id(pid)

def delete(pid: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE id = ?", (pid,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

init_db()
import sqlite3
from models import DoctorCreate, DoctorUpdate

DB_FILE = "doctors.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_all():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM doctors")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_by_id(did: int):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM doctors WHERE id = ?", (did,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def create(doctor: DoctorCreate):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO doctors (name, specialization, phone, email)
        VALUES (?, ?, ?, ?)
    ''', (doctor.name, doctor.specialization, doctor.phone, doctor.email))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return get_by_id(new_id)

def update(did: int, doctor: DoctorUpdate):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    updates = []
    values = []
    if doctor.name is not None:
        updates.append("name = ?")
        values.append(doctor.name)
    if doctor.specialization is not None:
        updates.append("specialization = ?")
        values.append(doctor.specialization)
    if doctor.phone is not None:
        updates.append("phone = ?")
        values.append(doctor.phone)
    if doctor.email is not None:
        updates.append("email = ?")
        values.append(doctor.email)
    if not updates:
        return get_by_id(did)
    values.append(did)
    query = f"UPDATE doctors SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    return get_by_id(did)

def delete(did: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM doctors WHERE id = ?", (did,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

init_db()
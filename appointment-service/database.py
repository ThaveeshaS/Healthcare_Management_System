import sqlite3
from models import AppointmentCreate, AppointmentUpdate

DB_FILE = "appointments.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_all():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appointments")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_by_id(aid: int):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appointments WHERE id = ?", (aid,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def create(appt: AppointmentCreate):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (appt.patient_id, appt.doctor_id, appt.appointment_date.isoformat(),
          appt.appointment_time.isoformat(), appt.status))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return get_by_id(new_id)

def update(aid: int, appt: AppointmentUpdate):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    updates = []
    values = []
    if appt.patient_id is not None:
        updates.append("patient_id = ?")
        values.append(appt.patient_id)
    if appt.doctor_id is not None:
        updates.append("doctor_id = ?")
        values.append(appt.doctor_id)
    if appt.appointment_date is not None:
        updates.append("appointment_date = ?")
        values.append(appt.appointment_date.isoformat())
    if appt.appointment_time is not None:
        updates.append("appointment_time = ?")
        values.append(appt.appointment_time.isoformat())
    if appt.status is not None:
        updates.append("status = ?")
        values.append(appt.status)
    if not updates:
        return get_by_id(aid)
    values.append(aid)
    query = f"UPDATE appointments SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    return get_by_id(aid)

def delete(aid: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM appointments WHERE id = ?", (aid,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

init_db()
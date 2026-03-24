import sqlite3
from models import MedicineCreate, MedicineUpdate

DB_FILE = "pharmacy.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            stock INTEGER NOT NULL,
            price REAL NOT NULL
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
        INSERT INTO medicines (name, stock, price)
        VALUES (?, ?, ?)
    ''', (med.name, med.stock, med.price))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return get_by_id(new_id)

def update(mid: int, med: MedicineUpdate):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    updates = []
    values = []
    if med.name is not None:
        updates.append("name = ?")
        values.append(med.name)
    if med.stock is not None:
        updates.append("stock = ?")
        values.append(med.stock)
    if med.price is not None:
        updates.append("price = ?")
        values.append(med.price)
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
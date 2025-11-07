from db import get_connection, init_db

init_db()

def add_expense(date, category, description, amount):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO expenses (date, category, description, amount)
        VALUES (?, ?, ?, ?)
    ''', (date, category, description, amount))
    conn.commit()
    conn.close()

def get_all_expenses():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses ORDER BY date DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def search_by_category(category):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses WHERE category LIKE ?", (f"%{category}%",))
    rows = cur.fetchall()
    conn.close()
    return rows

def total_expense():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT SUM(amount) as total FROM expenses")
    row = cur.fetchone()
    conn.close()
    return row["total"] if row["total"] else 0
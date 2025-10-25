import sqlite3

DB_FILE = "husma_foundation.db"

def get_conn():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS donors (
        donor_id TEXT PRIMARY KEY,
        name TEXT,
        nic TEXT UNIQUE,
        phone TEXT,
        email TEXT,
        username TEXT,
        password TEXT
    )''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS children (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        birthday TEXT,
        guardian TEXT,
        phone TEXT,
        milk_type TEXT,
        last_issue TEXT
    )''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS issues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        child_id INTEGER,
        date TEXT,
        milk_type TEXT
    )''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS donations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        donor_id TEXT,
        amount REAL,
        payment_slip TEXT,
        timestamp TEXT
    )''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        product_id INTEGER PRIMARY KEY,
        name TEXT,
        price REAL,
        stock INTEGER,
        image TEXT
    )''')
    conn.commit()

def add_donor(conn, donor_id, name, nic, phone, email, username, password):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO donors VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (donor_id, name, nic, phone, email, username, password))
    conn.commit()

def find_donor_by_id(conn, search_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donors WHERE donor_id = ?", (search_id,))
    donor = cursor.fetchone()
    if donor:
        return {"Donor_ID": donor[0], "Name": donor[1], "NIC": donor[2], "Phone": donor[3],
                "Email": donor[4], "Username": donor[5]}
    return None

def get_donors(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donors")
    return cursor.fetchall()

def add_donation(conn, donor_id, amount, payment_slip, timestamp):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO donations (donor_id, amount, payment_slip, timestamp) VALUES (?, ?, ?, ?)",
                   (donor_id, amount, payment_slip, timestamp))
    conn.commit()

def update_inventory(conn, product_id, qty):
    cursor = conn.cursor()
    cursor.execute("SELECT stock FROM inventory WHERE product_id = ?", (product_id,))
    current_stock = cursor.fetchone()[0]
    new_stock = current_stock - qty
    cursor.execute("UPDATE inventory SET stock = ? WHERE product_id = ?", (new_stock, product_id))
    conn.commit()

def get_donations_by_donor(conn, donor_id):
    cursor = conn.cursor()
    cursor.execute("SELECT amount, timestamp, payment_slip FROM donations WHERE donor_id = ? ORDER BY timestamp DESC",
                   (donor_id,))
    return cursor.fetchall()

def add_child(conn, name, birthday, guardian, phone, milk_type):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO children (name, birthday, guardian, phone, milk_type, last_issue) VALUES (?, ?, ?, ?, ?, ?)",
                   (name, birthday, guardian, phone, milk_type, None))
    conn.commit()

def get_children(conn, search_name=''):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM children WHERE name LIKE ? ORDER BY name", (f"%{search_name}%",))
    return cursor.fetchall()

def update_child(conn, child_id, name, birthday, guardian, phone, milk_type):
    cursor = conn.cursor()
    cursor.execute("UPDATE children SET name=?, birthday=?, guardian=?, phone=?, milk_type=? WHERE id=?",
                   (name, birthday, guardian, phone, milk_type, child_id))
    conn.commit()

def delete_child(conn, child_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM children WHERE id=?", (child_id,))
    cursor.execute("DELETE FROM issues WHERE child_id=?", (child_id,))
    conn.commit()

def get_child_by_id(conn, child_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM children WHERE id = ?", (child_id,))
    return cursor.fetchone()

def add_issue(conn, child_id, date, milk_type):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO issues (child_id, date, milk_type) VALUES (?, ?, ?)",
                   (child_id, date, milk_type))
    conn.commit()

def get_issues_by_child(conn, child_id):
    cursor = conn.cursor()
    cursor.execute("SELECT date, milk_type FROM issues WHERE child_id = ? ORDER BY date DESC", (child_id,))
    return cursor.fetchall()

def update_child_last_issue(conn, child_id, date):
    cursor = conn.cursor()
    cursor.execute("UPDATE children SET last_issue = ? WHERE id = ?", (date, child_id))
    conn.commit()
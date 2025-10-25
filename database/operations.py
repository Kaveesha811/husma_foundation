import sqlite3
import os
from datetime import datetime, timedelta
from config import config


def get_connection():
    """Create database connection"""
    conn = sqlite3.connect(config.DATABASE_URL, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initialize database tables"""
    conn = get_connection()
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS donors
                   (
                       donor_id
                       TEXT
                       PRIMARY
                       KEY,
                       name
                       TEXT
                       NOT
                       NULL,
                       nic
                       TEXT
                       UNIQUE
                       NOT
                       NULL,
                       phone
                       TEXT
                       NOT
                       NULL,
                       email
                       TEXT,
                       username
                       TEXT
                       UNIQUE,
                       password
                       TEXT
                       NOT
                       NULL,
                       is_verified
                       BOOLEAN
                       DEFAULT
                       TRUE,
                       created_at
                       TIMESTAMP
                       DEFAULT
                       CURRENT_TIMESTAMP
                   )
                   ''')

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS children
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       name
                       TEXT
                       NOT
                       NULL,
                       birthday
                       TEXT,
                       guardian
                       TEXT
                       NOT
                       NULL,
                       phone
                       TEXT
                       NOT
                       NULL,
                       milk_type
                       TEXT
                       NOT
                       NULL,
                       last_issue
                       TEXT,
                       created_at
                       TIMESTAMP
                       DEFAULT
                       CURRENT_TIMESTAMP
                   )
                   ''')

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS donations
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       donor_id
                       TEXT,
                       amount
                       REAL
                       NOT
                       NULL,
                       payment_slip
                       TEXT,
                       timestamp
                       TEXT
                       NOT
                       NULL,
                       receipt_generated
                       BOOLEAN
                       DEFAULT
                       FALSE,
                       FOREIGN
                       KEY
                   (
                       donor_id
                   ) REFERENCES donors
                   (
                       donor_id
                   )
                       )
                   ''')

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS inventory
                   (
                       product_id
                       INTEGER
                       PRIMARY
                       KEY,
                       name
                       TEXT
                       NOT
                       NULL,
                       price
                       REAL
                       NOT
                       NULL,
                       stock
                       INTEGER
                       NOT
                       NULL,
                       min_stock_level
                       INTEGER
                       DEFAULT
                       20,
                       image_path
                       TEXT,
                       created_at
                       TIMESTAMP
                       DEFAULT
                       CURRENT_TIMESTAMP
                   )
                   ''')

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS password_reset_tokens
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       donor_id
                       TEXT,
                       token
                       TEXT
                       UNIQUE,
                       expires_at
                       TIMESTAMP,
                       used
                       BOOLEAN
                       DEFAULT
                       FALSE,
                       FOREIGN
                       KEY
                   (
                       donor_id
                   ) REFERENCES donors
                   (
                       donor_id
                   )
                       )
                   ''')

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS issues
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       child_id
                       INTEGER,
                       date
                       TEXT
                       NOT
                       NULL,
                       milk_type
                       TEXT
                       NOT
                       NULL,
                       quantity
                       INTEGER
                       DEFAULT
                       1,
                       FOREIGN
                       KEY
                   (
                       child_id
                   ) REFERENCES children
                   (
                       id
                   )
                       )
                   ''')

    # Initialize inventory if empty
    cursor.execute("SELECT COUNT(*) FROM inventory")
    if cursor.fetchone()[0] == 0:
        products = [
            (1, "Pediasure", 3900.00, 100, 20, "static/images/pediasure.jpg"),
            (2, "Ensure", 3500.00, 80, 15, "static/images/ensure.jpg"),
            (3, "Sustagen", 3200.00, 120, 25, "static/images/sustagen.jpg"),
            (4, "Pediasure Gold", 4100.00, 90, 18, "static/images/pediasure_gold.jpg"),
            (5, "Ensure Complete", 3800.00, 70, 15, "static/images/ensure_complete.jpg"),
            (6, "Sustagen Junior", 3000.00, 110, 22, "static/images/sustagen_junior.jpg"),
        ]
        cursor.executemany("INSERT INTO inventory VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)", products)

    conn.commit()
    conn.close()


def execute_query(query, params=(), fetch=False, fetchall=False):
    """Execute database queries safely"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        if fetchall:
            result = [dict(row) for row in cursor.fetchall()]
        elif fetch:
            row = cursor.fetchone()
            result = dict(row) if row else None
        else:
            result = None
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
    return result


# Donor Operations
def get_next_donor_id():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT donor_id FROM donors ORDER BY donor_id DESC LIMIT 1")
    result = cursor.fetchone()
    conn.close()

    if result:
        num = int(result[0][1:]) + 1
        return f"D{num:03d}"
    return "D001"


def create_donor(donor_data):
    return execute_query(
        """INSERT INTO donors (donor_id, name, nic, phone, email, username, password)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        donor_data
    )


def get_donor_by_username(username):
    return execute_query(
        "SELECT * FROM donors WHERE username = ?",
        (username,),
        fetch=True
    )


def get_donor_by_email(email):
    return execute_query(
        "SELECT * FROM donors WHERE email = ?",
        (email,),
        fetch=True
    )


def get_donor_by_id(donor_id):
    return execute_query(
        "SELECT * FROM donors WHERE donor_id = ?",
        (donor_id,),
        fetch=True
    )


# Inventory Operations
def get_inventory():
    return execute_query("SELECT * FROM inventory", fetchall=True)


def get_low_stock_items():
    return execute_query(
        "SELECT * FROM inventory WHERE stock <= min_stock_level ORDER BY stock ASC",
        fetchall=True
    )


def update_inventory_stock(product_id, quantity):
    return execute_query(
        "UPDATE inventory SET stock = stock - ? WHERE product_id = ?",
        (quantity, product_id)
    )


def update_inventory(product_id, adjustment):
    return execute_query(
        "UPDATE inventory SET stock = stock + ? WHERE product_id = ?",
        (adjustment, product_id)
    )


# Donation Operations
def create_donation(donor_id, amount, payment_slip=None):
    return execute_query(
        "INSERT INTO donations (donor_id, amount, payment_slip, timestamp) VALUES (?, ?, ?, ?)",
        (donor_id, amount, payment_slip, datetime.now().isoformat())
    )


def get_donations_by_donor(donor_id):
    return execute_query(
        "SELECT amount, timestamp, payment_slip FROM donations WHERE donor_id = ? ORDER BY timestamp DESC",
        (donor_id,),
        fetchall=True
    )


def get_all_donations():
    """Get all donations for admin view"""
    return execute_query(
        """SELECT d.*, don.name as donor_name
           FROM donations d
                    LEFT JOIN donors don ON d.donor_id = don.donor_id
           ORDER BY d.timestamp DESC""",
        fetchall=True
    )


# Child Operations
def create_child(child_data):
    return execute_query(
        "INSERT INTO children (name, birthday, guardian, phone, milk_type) VALUES (?, ?, ?, ?, ?)",
        child_data
    )


def get_children(search_name=None):
    if search_name:
        return execute_query(
            "SELECT * FROM children WHERE name LIKE ? ORDER BY name",
            (f"%{search_name}%",),
            fetchall=True
        )
    return execute_query("SELECT * FROM children ORDER BY name", fetchall=True)


def get_child_by_id(child_id):
    return execute_query("SELECT * FROM children WHERE id = ?", (child_id,), fetch=True)


def update_child_last_issue(child_id, date):
    return execute_query(
        "UPDATE children SET last_issue = ? WHERE id = ?",
        (date, child_id)
    )


# Issue Operations
def create_issue(child_id, date, milk_type):
    return execute_query(
        "INSERT INTO issues (child_id, date, milk_type) VALUES (?, ?, ?)",
        (child_id, date, milk_type)
    )


def get_issues_by_child(child_id):
    return execute_query(
        "SELECT date, milk_type FROM issues WHERE child_id = ? ORDER BY date DESC",
        (child_id,),
        fetchall=True
    )


# Analytics Operations
def get_donation_analytics():
    return execute_query('''
                         SELECT COUNT(*)                 as total_donations,
                                COALESCE(SUM(amount), 0) as total_amount,
                                COALESCE(AVG(amount), 0) as average_donation,
                                COUNT(DISTINCT donor_id) as unique_donors,
                                COALESCE(MAX(amount), 0) as largest_donation
                         FROM donations
                         WHERE donor_id != 'anonymous'
                         ''', fetch=True)


def get_monthly_donation_trend():
    return execute_query('''
                         SELECT strftime('%Y-%m', timestamp) as month,
            COALESCE(SUM(amount), 0) as monthly_total,
            COUNT(*) as donation_count
                         FROM donations
                         GROUP BY strftime('%Y-%m', timestamp)
                         ORDER BY month DESC
                             LIMIT 12
                         ''', fetchall=True)


def get_donor_ranking():
    return execute_query('''
                         SELECT d.name,
                                d.donor_id,
                                COUNT(don.id)                as donation_count,
                                COALESCE(SUM(don.amount), 0) as total_donated
                         FROM donors d
                                  LEFT JOIN donations don ON d.donor_id = don.donor_id
                         WHERE d.is_verified = TRUE
                         GROUP BY d.donor_id
                         ORDER BY total_donated DESC LIMIT 10
                         ''', fetchall=True)
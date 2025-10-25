import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(hashed, password):
    return bcrypt.checkpw(password.encode(), hashed)

def check_login(conn, username, password):
    cursor = conn.cursor()
    cursor.execute("SELECT donor_id, phone, email, password FROM donors WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result and check_password(result[3], password):
        return result[0], result[1], result[2]
    return None
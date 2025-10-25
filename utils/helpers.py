def get_next_donor_id(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT donor_id FROM donors ORDER BY donor_id DESC LIMIT 1")
    last_id = cursor.fetchone()
    if last_id:
        num = int(last_id[0][1:]) + 1
        return f"D{num:03d}"
    return "D001"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'pdf'}
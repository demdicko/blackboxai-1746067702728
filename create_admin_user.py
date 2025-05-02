import hashlib
import sqlite3

DB_NAME = "tolo_distribution.db"

def create_admin_user(username, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, ?)
        """, (username, password_hash, "Admin"))
        conn.commit()
        print(f"Admin user '{username}' created successfully.")
    except sqlite3.IntegrityError:
        print(f"User '{username}' already exists.")
    except Exception as e:
        print(f"Error creating user: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Replace these with your desired admin username and password
    admin_username = "admin"
    admin_password = "admin123"
    create_admin_user(admin_username, admin_password)

import sqlite3
from sqlite3 import Error

DB_NAME = "tolo_distribution.db"

def create_connection():
    """ create a database connection to the SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        return conn
    except Error as e:
        print(e)
    return conn

def create_tables():
    """ create tables in the SQLite database """
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()

        # Products table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            reference TEXT UNIQUE NOT NULL,
            purchase_price REAL NOT NULL,
            sale_price REAL NOT NULL,
            stock_quantity INTEGER NOT NULL,
            profit_per_unit REAL NOT NULL
        );
        """)

        # Clients table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact_number TEXT,
            credit_balance REAL DEFAULT 0
        );
        """)

        # Suppliers table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact_info TEXT
        );
        """)

        # Stock entries table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            date TEXT NOT NULL,
            supplier_id INTEGER,
            FOREIGN KEY (product_id) REFERENCES products (id),
            FOREIGN KEY (supplier_id) REFERENCES suppliers (id)
        );
        """)

        # Sales table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            payment_method TEXT NOT NULL,
            client_id INTEGER,
            profit REAL NOT NULL,
            FOREIGN KEY (client_id) REFERENCES clients (id)
        );
        """)

        # Orders table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            order_details TEXT NOT NULL,
            status TEXT NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (client_id) REFERENCES clients (id)
        );
        """)

        # Users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        );
        """)

        conn.commit()
        conn.close()
    else:
        print("Error! cannot create the database connection.")

if __name__ == "__main__":
    create_tables()

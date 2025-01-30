# import sqlite3

# DATABASE_NAME = "hotel.db"

# def get_db_connection():
#     """Establish a connection to the SQLite database."""
#     conn = sqlite3.connect(DATABASE_NAME)
#     conn.row_factory = sqlite3.Row  # Allows access to columns by name
#     return conn

# def execute_query(conn, query, params=()):
#     """Execute a query that modifies the database (INSERT, UPDATE, DELETE)."""
#     try:
#         cursor = conn.cursor()
#         cursor.execute(query, params)
#         conn.commit()
#     except sqlite3.Error as e:
#         print(f"Database error: {e}")
#     finally:
#         cursor.close()

# def fetch_query(conn, query, params=()):
#     """Execute a SELECT query and return results."""
#     cursor = conn.cursor()
#     cursor.execute(query, params)
#     results = cursor.fetchall()
#     cursor.close()
#     return results

# def create_tables():
#     """Create necessary tables if they do not exist."""
#     conn = get_db_connection()
#     queries = [
#         """CREATE TABLE IF NOT EXISTS rooms (
#             room_id INTEGER PRIMARY KEY AUTOINCREMENT,
#             room_number TEXT NOT NULL UNIQUE,
#             room_type TEXT NOT NULL,
#             price REAL NOT NULL,
#             is_available INTEGER DEFAULT 1
#         );""",
#         """CREATE TABLE IF NOT EXISTS users (
#             user_id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT NOT NULL UNIQUE,
#             password TEXT NOT NULL,
#             email TEXT NOT NULL UNIQUE,
#             is_admin INTEGER DEFAULT 0
#         );""",
#         """CREATE TABLE IF NOT EXISTS reservations (
#             reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_id INTEGER NOT NULL,
#             room_id INTEGER NOT NULL,
#             check_in_date TEXT NOT NULL,
#             check_out_date TEXT NOT NULL,
#             status TEXT DEFAULT 'confirmed',
#             FOREIGN KEY (user_id) REFERENCES users (user_id),
#             FOREIGN KEY (room_id) REFERENCES rooms (room_id)
#         );"""
#     ]
    
#     for query in queries:
#         execute_query(conn, query)

#     conn.close()
#     print("Database tables created successfully.")

# # Run table creation when this script is executed
# if __name__ == "__main__":
#     create_tables()
import sqlite3
import os

# Set correct database path (prevents errors when running from different locations)
DATABASE_NAME = os.path.join(os.path.dirname(__file__), "hotel.db")

def get_db_connection():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

def execute_query(conn, query, params=()):
    """Execute a query that modifies the database (INSERT, UPDATE, DELETE)."""
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()

def fetch_query(conn, query, params=()):
    """Execute a SELECT query and return results."""
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()
    return results

def create_tables():
    """Create necessary tables if they do not exist."""
    conn = get_db_connection()
    
    queries = [
        """CREATE TABLE IF NOT EXISTS rooms (
            room_id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_number TEXT NOT NULL UNIQUE,
            room_type TEXT NOT NULL,
            price REAL NOT NULL,
            is_available INTEGER DEFAULT 1
        );""",
        """CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            is_admin INTEGER DEFAULT 0
        );""",
        """CREATE TABLE IF NOT EXISTS reservations (
            reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            room_id INTEGER NOT NULL,
            check_in_date TEXT NOT NULL,
            check_out_date TEXT NOT NULL,
            status TEXT DEFAULT 'confirmed',
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (room_id) REFERENCES rooms (room_id)
        );"""
    ]
    
    for query in queries:
        execute_query(conn, query)

    conn.close()
    print("✅ Database tables ensured.")

# Run table creation when this script is executed
if __name__ == "__main__":
    create_tables()

# utils/authentication.py
from database.db_connection import fetch_query, execute_query

def login(conn):
    """Login system."""
    username = input("Enter username: ")
    password = input("Enter password: ")

    query = "SELECT * FROM users WHERE username = ? AND password = ?;"
    user = fetch_query(conn, query, (username, password))

    if user:
        print("✅ Login successful!")
        return user[0]  # Returns the user record
    else:
        print("❌ Invalid username or password.")
        return None

def register_user(conn):
    """Register a new user."""
    username = input("Enter username: ")
    password = input("Enter password: ")
    email = input("Enter email: ")

    query = "INSERT INTO users (username, password, email) VALUES (?, ?, ?);"
    execute_query(conn, query, (username, password, email))

    print("✅ Registration successful!")

def is_admin(user):
    """Check if user is an admin."""
    return user[4] == 1  # Column index 4 is `is_admin`

def main():
    """Main function to test the authentication system."""
    print("Welcome to the Authentication System!")

    # You can simulate a connection here by replacing with an actual connection object
    # Assuming you have a function to get the DB connection
    conn = None  # Replace with your actual connection fetching function

    # For example purposes, you can call login or register functions
    print("\n--- Login ---")
    user = login(conn)

    if user:
        print(f"User {user[1]} logged in successfully.")

    print("\n--- Register User ---")
    register_user(conn)

if __name__ == "__main__":
    main()  # Calls the main function when the module is run

# from database.db_connection import get_db_connection, execute_query, fetch_query

# def view_my_reservations(conn, user_id):
#     """View reservations for a logged-in user."""
#     query = """
#         SELECT r.reservation_id, rm.room_number, rm.room_type, r.check_in_date, r.check_out_date, r.status
#         FROM reservations r
#         JOIN rooms rm ON r.room_id = rm.room_id
#         WHERE r.user_id = ?;
#     """
#     reservations = fetch_query(conn, query, (user_id,))

#     if reservations:
#         print("\n📋 Your Reservations:")
#         for res in reservations:
#             print(f"Reservation ID: {res[0]}, Room: {res[1]} ({res[2]}), Check-in: {res[3]}, Check-out: {res[4]}, Status: {res[5]}")
#     else:
#         print("❌ You have no reservations.")

# def book_room(conn, user_id):
#     """Allow registered users to book a room."""
#     check_in_date = input("Enter check-in date (YYYY-MM-DD): ")
#     check_out_date = input("Enter check-out date (YYYY-MM-DD): ")

#     # Fetch available rooms
#     query = """
#         SELECT room_id, room_number, room_type, price
#         FROM rooms
#         WHERE is_available = 1;
#     """
#     available_rooms = fetch_query(conn, query)

#     if available_rooms:
#         print("\n🏨 Available Rooms:")
#         for room in available_rooms:
#             print(f"Room ID: {room[0]}, Number: {room[1]}, Type: {room[2]}, Price: ${room[3]}")

#         room_id = input("Enter Room ID to book: ")

#         # Insert reservation
#         query = """
#             INSERT INTO reservations (user_id, room_id, check_in_date, check_out_date, status)
#             VALUES (?, ?, ?, ?, 'confirmed');
#         """
#         execute_query(conn, query, (user_id, room_id, check_in_date, check_out_date))
#         print("✅ Booking successful!")
#     else:
#         print("❌ No available rooms at the moment.")

# def registered_user_menu(conn, user_id):
#     """Menu for registered users."""
#     while True:
#         print("\n👤 Registered User Menu:")
#         print("1. View My Reservations")
#         print("2. Book a Room")
#         print("3. Logout")

#         choice = input("Enter your choice: ")

#         if choice == "1":
#             view_my_reservations(conn, user_id)
#         elif choice == "2":
#             book_room(conn, user_id)
#         elif choice == "3":
#             print("Logging out...")
#             break
#         else:
#             print("Invalid choice. Please try again.")

# if __name__ == "__main__":
#     conn = get_db_connection()
#     user_id = int(input("Enter your user ID to log in: "))  # Dummy authentication for now
#     registered_user_menu(conn, user_id)
import sqlite3
from database.db_connection import get_db_connection, execute_query, fetch_query
import hashlib

def hash_password(password):
    """Hash the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(conn):
    """Register a new user and log them in automatically."""
    print("\n🔹 Register a New Account")
    username = input("Enter your username: ")
    email = input("Enter your email: ")
    password = input("Enter a password: ")

    hashed_password = hash_password(password)

    # Insert user into database
    query = "INSERT INTO users (username, email, password) VALUES (?, ?, ?);"
    execute_query(conn, query, (username, email, hashed_password))

    # Fetch the newly registered user ID
    user_id = fetch_query(conn, "SELECT user_id FROM users WHERE email = ?;", (email,))
    
    if user_id:
        user_id = user_id[0][0]
        print(f"✅ User '{username}' registered successfully!\n")
        print(f"🎉 Welcome, {username}! You are now logged in.")
        registered_user_menu(conn, user_id)  # Redirect to user menu
    else:
        print("❌ Registration failed. Please try again.")

def login_user(conn):
    """Allow users to log in."""
    print("\n🔐 Login to Your Account")
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    hashed_password = hash_password(password)

    # Verify user credentials
    query = "SELECT user_id, username FROM users WHERE email = ? AND password = ?;"
    user = fetch_query(conn, query, (email, hashed_password))

    if user:
        user_id, username = user[0]
        print(f"✅ Welcome back, {username}!")
        registered_user_menu(conn, user_id)  # Redirect to user menu
    else:
        print("❌ Invalid email or password.")

def view_my_reservations(conn, user_id):
    """View reservations for a logged-in user."""
    query = """
        SELECT r.reservation_id, rm.room_number, rm.room_type, r.check_in_date, r.check_out_date, r.status
        FROM reservations r
        JOIN rooms rm ON r.room_id = rm.room_id
        WHERE r.user_id = ?;
    """
    reservations = fetch_query(conn, query, (user_id,))

    if reservations:
        print("\n📋 Your Reservations:")
        for res in reservations:
            print(f"Reservation ID: {res[0]}, Room: {res[1]} ({res[2]}), Check-in: {res[3]}, Check-out: {res[4]}, Status: {res[5]}")
    else:
        print("❌ You have no reservations.")

def book_room(conn, user_id):
    """Allow registered users to book a room."""
    check_in_date = input("Enter check-in date (YYYY-MM-DD): ")
    check_out_date = input("Enter check-out date (YYYY-MM-DD): ")

    # Fetch available rooms
    query = """
        SELECT room_id, room_number, room_type, price
        FROM rooms
        WHERE is_available = 1;
    """
    available_rooms = fetch_query(conn, query)

    if available_rooms:
        print("\n🏨 Available Rooms:")
        for room in available_rooms:
            print(f"Room ID: {room[0]}, Number: {room[1]}, Type: {room[2]}, Price: ${room[3]}")

        room_id = input("Enter Room ID to book: ")

        # Insert reservation
        query = """
            INSERT INTO reservations (user_id, room_id, check_in_date, check_out_date, status)
            VALUES (?, ?, ?, ?, 'confirmed');
        """
        execute_query(conn, query, (user_id, room_id, check_in_date, check_out_date))
        print("✅ Booking successful!")
    else:
        print("❌ No available rooms at the moment.")

def registered_user_menu(conn, user_id):
    """Menu for registered users."""
    while True:
        print("\n👤 Registered User Menu:")
        print("1. View My Reservations")
        print("2. Book a Room")
        print("3. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_my_reservations(conn, user_id)
        elif choice == "2":
            book_room(conn, user_id)
        elif choice == "3":
            print("Logging out...\n")
            return  # Exit to main menu
        else:
            print("Invalid choice. Please try again.")

def main():
    conn = get_db_connection()

    while True:
        print("\n🔑 Welcome to the Hotel Booking System")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            register_user(conn)
        elif choice == "2":
            login_user(conn)
        elif choice == "3":
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

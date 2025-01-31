
import sqlite3
import hashlib
from database.db_connection import get_db_connection, execute_query, fetch_query
from utils.email_notifications import send_booking_email, send_welcome_email  # Assuming email functions are in utils
from datetime import datetime

# Function to hash passwords securely
def hash_password(password):
    """Hash the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(conn):
    """Register a new user and send a confirmation email."""
    print("\n🔹 Register a New Account")
    username = input("Enter your username: ").strip()
    email = input("Enter your email: ").strip()
    password = input("Enter a password: ").strip()

    hashed_password = hash_password(password)

    # Check if email already exists
    existing_user = fetch_query(conn, "SELECT user_id FROM users WHERE email = ?;", (email,))
    if existing_user:
        print("❌ This email is already registered. Try logging in.")
        return

    # Insert user into the database
    query = "INSERT INTO users (username, email, password) VALUES (?, ?, ?);"
    execute_query(conn, query, (username, email, hashed_password))

    # Fetch the newly registered user ID
    user = fetch_query(conn, "SELECT user_id FROM users WHERE email = ?;", (email,))
    
    if user:
        user_id = user[0]["user_id"]
        print(f"✅ User '{username}' registered successfully!\n")
        print(f"🎉 Welcome, {username}! You are now logged in.")

        # ✅ Send welcome email
        send_welcome_email(email, username)

        registered_user_menu(conn, user_id)  # Redirect to user menu
    else:
        print("❌ Registration failed. Please try again.")

def login_user(conn):
    """Allow users to log in."""
    print("\n🔐 Login to Your Account")
    email = input("Enter your email: ").strip()
    password = input("Enter your password: ").strip()
    hashed_password = hash_password(password)

    # Verify user credentials
    query = "SELECT user_id, username FROM users WHERE email = ? AND password = ?;"
    user = fetch_query(conn, query, (email, hashed_password))

    if user:
        user_id, username = user[0]["user_id"], user[0]["username"]
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
            print(f"Reservation ID: {res['reservation_id']}, Room: {res['room_number']} ({res['room_type']}), Check-in: {res['check_in_date']}, Check-out: {res['check_out_date']}, Status: {res['status']}")
    else:
        print("❌ You have no reservations.")

def book_room(conn, user_id):
    """Allow registered users to book a room and send a confirmation email."""
    try:
        check_in_date = input("Enter check-in date (YYYY-MM-DD): ").strip()
        check_out_date = input("Enter check-out date (YYYY-MM-DD): ").strip()

        # Convert to datetime for validation
        try:
            check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d')
            check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d')
        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD.")
            return

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
                print(f"Room ID: {room['room_id']}, Number: {room['room_number']}, Type: {room['room_type']}, Price: ${room['price']}")

            try:
                room_id = int(input("Enter Room ID to book: ").strip())

                # Check if the selected room exists and is available
                room_check = fetch_query(conn, "SELECT room_number, room_type FROM rooms WHERE room_id = ? AND is_available = 1;", (room_id,))
                if not room_check:
                    print("❌ Invalid Room ID or Room is not available.")
                    return

                room_info = f"Room {room_check[0]['room_number']} ({room_check[0]['room_type']})"

                # Insert reservation
                query = """
                    INSERT INTO reservations (user_id, room_id, check_in_date, check_out_date, status)
                    VALUES (?, ?, ?, ?, 'confirmed');
                """
                reservation_id = execute_query(conn, query, (user_id, room_id, check_in_date.strftime('%Y-%m-%d'), check_out_date.strftime('%Y-%m-%d')))

                if reservation_id:
                    # Update room availability
                    execute_query(conn, "UPDATE rooms SET is_available = 0 WHERE room_id = ?;", (room_id,))

                    # Get user email and username
                    user = fetch_query(conn, "SELECT email, username FROM users WHERE user_id = ?;", (user_id,))
                    
                    if user:
                        user_email, username = user[0]["email"], user[0]["username"]
                        send_booking_email(user_email, username, room_info, check_in_date.strftime('%Y-%m-%d'), check_out_date.strftime('%Y-%m-%d'))
                        print("✅ Booking successful! Check your email for confirmation.")  # ✅ Message appears only after success.
                    else:
                        print("❌ User not found. Unable to send email confirmation.")
                else:
                    print("❌ Booking failed. Please try again.")

            except ValueError:
                print("❌ Invalid input. Please enter a numerical Room ID.")
        else:
            print("❌ No available rooms at the moment.")

    except Exception as e:
        print(f"❌ Error: {e}")

def registered_user_menu(conn, user_id):
    """Menu for registered users."""
    while True:
        print("\n👤 Registered User Menu:")
        print("1. View My Reservations")
        print("2. Book a Room")
        print("3. Logout")

        choice = input("Enter your choice: ").strip()

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

        choice = input("Enter your choice: ").strip()

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

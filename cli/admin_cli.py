import logging
from database.db_connection import execute_query, fetch_query, get_db_connection

# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("admin_cli.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def add_room(conn):
    """Allow admin to add a new room."""
    room_number = input("Enter room number: ")
    room_type = input("Enter room type (e.g., Deluxe, Standard, Suite): ")

    try:
        price = float(input("Enter room price: "))
        query = "INSERT INTO rooms (room_number, room_type, price, is_available) VALUES (?, ?, ?, 1);"
        execute_query(conn, query, (room_number, room_type, price))
        print(f"✅ Room {room_number} added successfully!")
        logger.info(f"Room added: {room_number}, Type: {room_type}, Price: {price}")
    except ValueError:
        print("⚠️ Invalid price format. Please enter a number.")
        logger.warning("Invalid price entered.")
    except Exception as e:
        print(f"⚠️ Error: {e}")
        logger.error(f"Failed to add room: {e}")

def view_rooms(conn):
    """Display all available rooms."""
    rooms = fetch_query(conn, "SELECT * FROM rooms;")
    if rooms:
        print("\nAvailable Rooms:")
        for room in rooms:
            print(f"Room ID: {room[0]}, Number: {room[1]}, Type: {room[2]}, Price: ${room[3]}, Available: {'Yes' if room[4] else 'No'}")
        logger.info("Rooms displayed successfully.")
    else:
        print("⚠️ No rooms found.")
        logger.warning("No rooms found in database.")

def view_reservations(conn):
    """Display all reservations."""
    reservations = fetch_query(conn, "SELECT * FROM reservations;")
    if reservations:
        print("\nAll Reservations:")
        for res in reservations:
            print(f"Reservation ID: {res[0]}, Guest: {res[1]}, Room: {res[2]}, Check-in: {res[3]}, Check-out: {res[4]}")
        logger.info("Reservations displayed successfully.")
    else:
        print("⚠️ No reservations found.")
        logger.warning("No reservations found in database.")

def delete_room(conn):
    """Allow admin to delete a room."""
    room_number = input("Enter room number to delete: ")
    query = "DELETE FROM rooms WHERE room_number = ?;"
    execute_query(conn, query, (room_number,))
    print(f"✅ Room {room_number} deleted successfully!")
    logger.info(f"Room deleted: {room_number}")

def admin_cli():
    """Admin panel CLI."""
    conn = get_db_connection()

    while True:
        print("\n--- Admin CLI Panel ---")
        print("1. Add Room")
        print("2. View Rooms")
        print("3. View Reservations")
        print("4. Delete Room")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_room(conn)
        elif choice == "2":
            view_rooms(conn)
        elif choice == "3":
            view_reservations(conn)
        elif choice == "4":
            delete_room(conn)
        elif choice == "5":
            print("Exiting Admin CLI.")
            logger.info("Admin exited the CLI panel.")
            break
        else:
            print("❌ Invalid choice. Please try again.")
            logger.warning("Invalid menu choice entered.")

    conn.close()

if __name__ == "__main__":
    admin_cli()

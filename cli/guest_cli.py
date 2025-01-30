from database.db_connection import fetch_query

def check_room_availability(conn, check_in_date, check_out_date):
    """Check available rooms for a given date range."""
    query = """
        SELECT room_number, room_type, price
        FROM rooms
        WHERE is_available = 1 AND room_id NOT IN (
            SELECT room_id FROM reservations
            WHERE NOT (check_out_date <= ? OR check_in_date >= ?)
        );
    """
    return fetch_query(conn, query, (check_in_date, check_out_date))

def guest_menu(conn):
    """Guest user menu."""
    while True:
        print("\nGuest Menu:")
        print("1. Check Room Availability")
        print("2. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            check_in_date = input("Enter check-in date (YYYY-MM-DD): ")
            check_out_date = input("Enter check-out date (YYYY-MM-DD): ")
            
            rooms = check_room_availability(conn, check_in_date, check_out_date)
            
            if rooms:
                print("\nAvailable Rooms:")
                for room in rooms:
                    print(f"Room: {room[0]}, Type: {room[1]}, Price: ${room[2]}")
            else:
                print("No rooms available for the selected dates.")
        elif choice == "2":
            print("Returning to main menu...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    from database.db_connection import get_db_connection

    conn = get_db_connection()
    guest_menu(conn)

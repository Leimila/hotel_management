# # from database.db_connection import fetch_query
# # from cli.registered_cli import register_user, book_room

# # def check_room_availability(conn, check_in_date, check_out_date):
# #     """Check available rooms for a given date range."""
# #     query = """
# #         SELECT room_number, room_type, price
# #         FROM rooms
# #         WHERE is_available = 1 AND room_id NOT IN (
# #             SELECT room_id FROM reservations
# #             WHERE NOT (check_out_date <= ? OR check_in_date >= ?)
# #         );
# #     """
# #     return fetch_query(conn, query, (check_in_date, check_out_date))

# # def guest_menu(conn):
# #     """Guest user menu."""
# #     while True:
# #         print("\n🛎️ Guest Menu:")
# #         print("1. Check Room Availability")
# #         print("2. Register")
# #         print("3. Book a Room")
# #         print("4. Logout (Return to Main Menu)")
# #         print("5. Exit (Close Application)")

# #         choice = input("Enter your choice: ")

# #         if choice == "1":
# #             check_in_date = input("Enter check-in date (YYYY-MM-DD): ")
# #             check_out_date = input("Enter check-out date (YYYY-MM-DD): ")
            
# #             rooms = check_room_availability(conn, check_in_date, check_out_date)
            
# #             if rooms:
# #                 print("\nAvailable Rooms:")
# #                 for room in rooms:
# #                     print(f"Room: {room[0]}, Type: {room[1]}, Price: ${room[2]}")
# #             else:
# #                 print("No rooms available for the selected dates.")

# #         elif choice == "2":
# #             register_user(conn)  # Calls the function to register a new user.

# #         elif choice == "3":
# #             book_room(conn)  # Calls the function to book a room.

# #         elif choice == "4":
# #             print("Logging out... Returning to the main menu.")
# #             return  # Returns to the main menu.

# #         elif choice == "5":
# #             print("Exiting the system... Goodbye!")
# #             exit()  # Closes the application.

# #         else:
# #             print("Invalid choice. Please try again.")

# # if __name__ == "__main__":
# #     from database.db_connection import get_db_connection

# #     conn = get_db_connection()
# #     guest_menu(conn)



# from database.db_connection import fetch_query
# from cli.registered_cli import register_user, book_room

# # To track whether the user is registered or not
# is_registered = False  

# def check_room_availability(conn, check_in_date, check_out_date):
#     """Check available rooms for a given date range."""
#     query = """
#         SELECT room_number, room_type, price
#         FROM rooms
#         WHERE is_available = 1 AND room_id NOT IN (
#             SELECT room_id FROM reservations
#             WHERE NOT (check_out_date <= ? OR check_in_date >= ?)
#         );
#     """
#     return fetch_query(conn, query, (check_in_date, check_out_date))

# def guest_menu(conn):
#     """Guest user menu."""
#     global is_registered  # Track registration status

#     while True:
#         print("\n🛎️ Guest Menu:")
#         print("1. Check Room Availability")
#         print("2. Register")
#         print("3. Book a Room")
#         print("4. Logout (Return to Main Menu)")
#         print("5. Exit (Close Application)")

#         choice = input("Enter your choice: ")

#         if choice == "1":
#             check_in_date = input("Enter check-in date (YYYY-MM-DD): ")
#             check_out_date = input("Enter check-out date (YYYY-MM-DD): ")
            
#             rooms = check_room_availability(conn, check_in_date, check_out_date)
            
#             if rooms:
#                 print("\nAvailable Rooms:")
#                 for room in rooms:
#                     print(f"Room: {room[0]}, Type: {room[1]}, Price: ${room[2]}")
#             else:
#                 print("No rooms available for the selected dates.")

#         elif choice == "2":
#             register_user(conn)  # Calls the function to register a new user.
#             is_registered = True  # Mark user as registered after successful registration.

#         elif choice == "3":
#             if not is_registered:
#                 print("\n⚠️ Warning: You need to register before booking a room.")
#                 print("Please select option 2 to register first.\n")
#             else:
#                 book_room(conn)  # Calls the function to book a room.

#         elif choice == "4":
#             print("Logging out... Returning to the main menu.")
#             return  # Returns to the main menu.

#         elif choice == "5":
#             print("Exiting the system... Goodbye!")
#             exit()  # Closes the application.

#         else:
#             print("Invalid choice. Please try again.")

# if __name__ == "__main__":
#     from database.db_connection import get_db_connection

#     conn = get_db_connection()
#     guest_menu(conn)
import re
from datetime import datetime
from database.db_connection import fetch_query
from cli.registered_cli import register_user, book_room, view_my_reservations

def is_valid_date(date_str):
    """Check if the input is a valid date format (YYYY-MM-DD)."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False  

def check_room_availability(conn):
    """Check available rooms for a given date range."""
    while True:
        check_in_date = input("Enter check-in date (YYYY-MM-DD): ").strip()
        if check_in_date == '6':  
            exit()  # Exit application
        if check_in_date == '0':  
            return  # Return to the main menu
        if not is_valid_date(check_in_date):
            print("❌ Invalid date format. Please enter in YYYY-MM-DD format.")
            continue  

        check_out_date = input("Enter check-out date (YYYY-MM-DD): ").strip()
        if check_out_date == '6':  
            exit()  
        if check_out_date == '0':  
            return  
        if not is_valid_date(check_out_date):
            print("❌ Invalid date format. Please enter in YYYY-MM-DD format.")
            continue  

        query = """
            SELECT room_number, room_type, price
            FROM rooms
            WHERE is_available = 1 AND room_id NOT IN (
                SELECT room_id FROM reservations
                WHERE NOT (check_out_date <= ? OR check_in_date >= ?)
            );
        """
        rooms = fetch_query(conn, query, (check_in_date, check_out_date))

        if rooms:
            print("\n✅ Available Rooms:")
            for room in rooms:
                print(f"Room: {room[0]}, Type: {room[1]}, Price: ${room[2]}")
        else:
            print("❌ No rooms available for the selected dates.")
        return  

def guest_menu(conn):
    """Guest user menu."""
    while True:
        print("\n🌟 Welcome to the Hotel Booking System 🌟")
        print("1. Check Room Availability")
        print("2. Register")
        print("3. Logout")
        print("4. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            check_room_availability(conn)

        elif choice == "2":
            username = register_user(conn)  # Function should return username
            # print(f"\n🔹 {username} registration successful! Press 0 to return to the main menu.")
            # while True:
            #     back_choice = input().strip()
            #     if back_choice == '0':
            #         break  
          

        elif choice == "3":
            print("Logging out...\n")
            return  

        elif choice == "4":
            print("Exiting... Goodbye!")
            exit()  

        else:
            print("❌ Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    from database.db_connection import get_db_connection

    conn = get_db_connection()
    guest_menu(conn)

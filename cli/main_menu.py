# import sys
# from database.db_connection import get_db_connection
# from cli.guest_cli import guest_menu
# from cli.admin_cli import manage_rooms  # Ensure this function is correctly implemented in `admin_cli.py`

# def main_menu():
#     """Main menu for the hotel reservation system."""
#     conn = get_db_connection()  # Establish database connection
    
#     while True:
#         print("\n🏨 Welcome to the Hotel Reservation System")
#         print("1. Guest")
#         print("2. Admin")
#         print("3. Exit")

#         choice = input("Enter your choice: ")

#         if choice == "1":
#             guest_menu(conn)
#         elif choice == "2":
#             print("\n🔑 Admin Login Required")
#             username = input("Enter admin username: ")
#             password = input("Enter admin password: ")
            
#             # Dummy authentication for now
#             if username == "admin" and password == "password":
#                 manage_rooms(conn)
#             else:
#                 print("❌ Invalid credentials. Access denied.")
#         elif choice == "3":
#             print("Exiting system. Goodbye!")
#             sys.exit(0)
#         else:
#             print("Invalid choice. Please try again.")

# if __name__ == "__main__":
#     main_menu()
import logging
from database.db_connection import get_db_connection
from cli.admin_cli import admin_cli
from cli.registered_cli import registered_user_menu  # ✅ Fixed import

# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("main_menu.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def main_menu():
    """Main CLI menu for the hotel reservation system."""
    conn = get_db_connection()

    while True:
        print("\n🏨 Welcome to the Hotel Management System")
        print("1. Admin Login")
        print("2. Registered User Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            admin_cli()  # ✅ Calls the admin panel
        elif choice == "2":
            try:
                user_id = int(input("Enter your User ID: "))
                registered_user_menu(conn, user_id)  # ✅ Fixed function call
            except ValueError:
                print("❌ Invalid User ID. Please enter a number.")
                logger.warning("Invalid User ID entered.")
        elif choice == "3":
            print("👋 Exiting the system. Goodbye!")
            logger.info("System exited by user.")
            break
        else:
            print("❌ Invalid choice. Please try again.")
            logger.warning("Invalid menu choice entered.")

    conn.close()

if __name__ == "__main__":
    main_menu()

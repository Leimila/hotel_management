# import logging
# from database.db_connection import get_db_connection
# from cli.admin_cli import admin_cli
# from cli.registered_cli import registered_user_menu  # ✅ Fixed import

# # ANSI Color Codes for CLI Output
# GREEN = "\033[92m"
# RED = "\033[91m"
# BLUE = "\033[94m"
# YELLOW = "\033[93m"
# RESET = "\033[0m"

# # Logger setup
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# file_handler = logging.FileHandler("main_menu.log")
# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)

# def main_menu():
#     """Main CLI menu for the hotel reservation system."""
#     conn = get_db_connection()

#     while True:
#         print("\n🏨 Welcome to the Hotel Management System")
#         print("1. Admin Login")
#         print("2. Registered User Login")
#         print("3. Exit")

#         choice = input("Enter your choice: ")

#         if choice == "1":
#             admin_cli()  # ✅ Calls the admin panel
#         elif choice == "2":
#             try:
#                 user_id = int(input("Enter your User ID: "))
#                 registered_user_menu(conn, user_id)  # ✅ Fixed function call
#             except ValueError:
#                 print("❌ Invalid User ID. Please enter a number.")
#                 logger.warning("Invalid User ID entered.")
#         elif choice == "3":
#             print("👋 Exiting the system. Goodbye!")
#             logger.info("System exited by user.")
#             break
#         else:
#             print("❌ Invalid choice. Please try again.")
#             logger.warning("Invalid menu choice entered.")

#     conn.close()

# if __name__ == "__main__":
#     main_menu()
import logging
from database.db_connection import get_db_connection
from cli.admin_cli import admin_cli
from cli.registered_cli import registered_user_menu

# ANSI Color Codes for CLI Output
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RESET = "\033[0m"

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
        print(f"\n{BLUE}🏨 Welcome to the Hotel Management System{RESET}")
        print(f"{YELLOW}1.{RESET} Admin Login")
        print(f"{YELLOW}2.{RESET} Registered User Login")
        print(f"{YELLOW}3.{RESET} Exit")

        choice = input(f"{BLUE}Enter your choice: {RESET}").strip()

        if choice == "1":
            admin_cli()  # ✅ Calls the admin panel
        elif choice == "2":
            try:
                user_id = int(input(f"{BLUE}Enter your User ID: {RESET}"))
                registered_user_menu(conn, user_id)  # ✅ Calls user menu
            except ValueError:
                print(f"{RED}❌ Invalid User ID. Please enter a number.{RESET}")
                logger.warning("Invalid User ID entered.")
        elif choice == "3":
            print(f"{RED}👋 Exiting the system. Goodbye!{RESET}")
            logger.info("System exited by user.")
            break
        else:
            print(f"{RED}❌ Invalid choice. Please try again.{RESET}")
            logger.warning("Invalid menu choice entered.")

    conn.close()

if __name__ == "__main__":
    main_menu()

import requests

from data_base.data_base_service import DatabaseService
from menu.main_menu import MainMenu
from utils.config import RESET_ALL, YELLOW, RED


def main() -> None:
    """
    The main function to execute the Hunter Check Mail application.

    Returns:
        None
    """
    # Initialize the DatabaseService instance
    database_service: DatabaseService = DatabaseService()

    # Initialize the MainMenu instance with the DatabaseService instance
    main_menu: MainMenu = MainMenu(database_service)

    # Display the main menu
    main_menu.display_main_menu()


# Check if the script is executed directly
if __name__ == "__main__":
    try:
        # Execute the main function within a try block
        main()
    except KeyboardInterrupt:
        # Handle keyboard interruption by printing a message
        print(f"{YELLOW}Программа прервана пользователем{RESET_ALL}")
    except requests.exceptions.RequestException as req_error:
        # Handle requests exceptions by printing an error message
        print(f"{RED}Произошла ошибка во время запроса: {req_error}{RESET_ALL}")
    except Exception as e:
        # Handle other exceptions by printing an error message
        print(f"{RED}Произошла непредвиденная ошибка: {e}{RESET_ALL}")

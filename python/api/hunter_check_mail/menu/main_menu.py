# hunter_check_mail/menu/main_menu.py
from typing import Any

from api_clients.hunter_client_factory import HunterClientFactory
from menu.request_menu import RequestMenu
from utils.config import GREEN, CYAN, RESET_ALL, RED, BLUE
from utils.logger import logger


class MainMenu:
    """
    MainMenu class for handling the main menu interactions.

    Attributes:
        m_hunter_client_factory (HunterClientFactory): Factory for creating Hunter API clients.
        m_database_service (Any): Service for interacting with the database.
        m_logger (Logger): Logger instance for logging messages.
    """

    def __init__(self, database_service: Any):
        """
        Initializes a new MainMenu instance.

        Args:
            database_service (Any): Service for interacting with the database.
        """
        # Instantiate a HunterClientFactory to create instances of Hunter API clients
        self.m_hunter_client_factory = HunterClientFactory()

        # Assign the provided 'database_service' parameter to the 'm_database_service' attribute
        self.m_database_service = database_service  # Добавлено (Added)

        # Assign the logger instance to the 'm_logger' attribute for logging messages
        self.m_logger = logger

    def display_main_menu(self) -> None:
        """
        Displays the main menu and processes user input until the user chooses to exit.
        """
        while True:
            self.print_main_menu_options()
            choice = input(f"{GREEN}Choice: {RESET_ALL}")
            # Process the user's choice by calling the 'process_main_menu_choice' method
            self.process_main_menu_choice(choice)

    @staticmethod
    def print_main_menu_options() -> None:
        """
        Prints the main menu options.
        """
        print(f"{GREEN}---------- MAIN MENU ------------{RESET_ALL}")
        print(f"{CYAN}1. Make request{RESET_ALL}")
        print(f"{CYAN}2. Show result by Email{RESET_ALL}")
        print(f"{CYAN}3. Show all results{RESET_ALL}")
        print(f"{CYAN}4. Delete by email{RESET_ALL}")
        print(f"{CYAN}5. Exit{RESET_ALL}")

    def process_main_menu_choice(self, choice: str) -> None:
        """
        Processes the user's choice from the main menu.

        Args:
            choice (str): The user's input choice.
        """
        menu_actions = {
            "1": self.make_request_menu,
            "2": self.show_result_by_email,
            "3": self.show_all_results,
            "4": self.delete_by_email,
            "5": self.exit_program,
        }

        # Retrieve the action associated with the user's choice from the 'menu_actions' dictionary
        action = menu_actions.get(choice)

        # Check if the retrieved action is not None (i.e., a valid action exists for the choice)
        if action:
            # Execute the retrieved action (call the corresponding method)
            action()
        else:
            # If the action is None, the user input is invalid, so call the 'invalid_input' method
            self.invalid_input()

    def invalid_input(self) -> None:
        """
        Handles invalid user input by logging a warning and printing an error message.
        """
        self.m_logger.warning("Invalid input. Please choose an option from 1 to 5.")
        print(f"{RED}Invalid input. Please choose an option from 1 to 5.{RESET_ALL}")

    def make_request_menu(self) -> None:
        """
        Initiates the process to make a request by creating a RequestMenu instance.
        """
        # Create an instance of the RequestMenu class, passing the current MainMenu instance,
        # the HunterClientFactory, and the DatabaseService as parameters
        request_menu = RequestMenu(self, self.m_hunter_client_factory, self.m_database_service)

        # Display the request menu by calling the 'display_request_menu' method on the created RequestMenu instance
        request_menu.display_request_menu()

    def show_result_by_email(self) -> None:
        """
        Displays the result for a specified email by querying the database.
        """
        email = input(f"{CYAN}Enter email: {RESET_ALL}")
        # Retrieve the result for the specified email from the database service
        result = self.m_database_service.get_result_by_email(email)
        print(result)

    def show_all_results(self) -> None:
        """
        Displays all results in the database.
        """
        # Retrieve all results from the database service and store them in the 'results' variable
        results = self.m_database_service.get_all_results()
        print(results)

    def delete_by_email(self) -> None:
        """
        Deletes a record in the database based on the specified email.
        """
        email = input(f"{CYAN}Enter email to delete: {RESET_ALL}")
        # Delete the record in the database associated with the specified email using the database service
        self.m_database_service.delete_by_email(email)

    @staticmethod
    def exit_program() -> None:
        """
        Exits the program gracefully.
        """
        print(f"\n{BLUE}Goodbye!{RESET_ALL}")
        # Exit the program
        exit()

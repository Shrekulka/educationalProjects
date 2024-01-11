# hunter_check_mail/menu/request_menu.py

import json
from typing import Any, Dict, Optional

import requests

from utils.config import RED, RESET_ALL, CYAN, YELLOW, GREEN, MAGENTA
from utils.logger import logger


class RequestMenu:
    """
    RequestMenu class for handling various API requests in the menu.

    Attributes:
        m_main_menu (MainMenu): The instance of the main menu.
        m_hunter_client_factory (HunterClientFactory): Factory for creating Hunter API clients.
        m_database_service (Any): Service for interacting with the database.
        m_logger (Logger): Logger instance for logging messages.
    """

    def __init__(self, main_menu: Any, hunter_client_factory: Any, database_service: Any):
        """
        Initializes a new RequestMenu instance.

        Args:
            main_menu (Any): The instance of the main menu.
            hunter_client_factory (Any): Factory for creating Hunter API clients.
            database_service (Any): Service for interacting with the database.
        """
        # Assigning the main menu instance to the 'm_main_menu' attribute of the current object.
        self.m_main_menu = main_menu

        # Assigning the HunterClientFactory instance to the 'm_hunter_client_factory' attribute of the current object.
        self.m_hunter_client_factory = hunter_client_factory

        # Assigning the database service instance to the 'm_database_service' attribute of the current object.
        self.m_database_service = database_service

        # Assigning the logger instance to the 'm_logger' attribute of the current object.
        self.m_logger = logger

    def display_request_menu(self) -> None:
        """
        Displays the request menu and processes user input until the user chooses to go back.
        """
        # Infinite loop for displaying the main menu options and processing user input.
        while True:
            # Print the available menu options.
            self.print_menu_options()
            choice = input(f"{GREEN}Select an option (1-6): {RESET_ALL}")
            # Process the user's choice based on the menu actions.
            self.process_menu_choice(choice)

    @staticmethod
    def print_menu_options() -> None:
        """
        Prints the options available in the request menu.
        """
        print(f"{GREEN}---------- REQUEST MENU ------------{RESET_ALL}")
        print(f"{CYAN}1. Domain Search{RESET_ALL}")
        print(f"{CYAN}2. Email Finder{RESET_ALL}")
        print(f"{CYAN}3. Email Verification{RESET_ALL}")
        print(f"{CYAN}4. Email Count{RESET_ALL}")
        print(f"{CYAN}5. Account Information{RESET_ALL}")
        print(f"{CYAN}6. Back{RESET_ALL}")

    def process_menu_choice(self, choice: str) -> None:
        """
        Processes the user's choice from the request menu.

        Args:
            choice (str): The user's input choice.
        """
        menu_actions = {
            "1": self.domain_search_request_menu,
            "2": self.email_finder_request_menu,
            "3": self.email_verification_request_menu,
            "4": self.email_count_request_menu,
            "5": self.account_information_request_menu,
            "6": self.back_to_main_menu,
        }

        # Get the corresponding action function based on the user's choice.
        action = menu_actions.get(choice)

        # Check if a valid action function is found.
        if action:
            # Execute the chosen action function.
            action()
        else:
            # Handle the case when the user input is invalid.
            self.invalid_input()

    def invalid_input(self) -> None:
        """
        Handles invalid user input by logging a warning and printing an error message.
        """
        self.m_logger.warning("Invalid input. Please choose an option from 1 to 6.")
        print(f"{RED}Invalid input. Please choose an option from 1 to 6.{RESET_ALL}")

    def back_to_main_menu(self) -> None:
        """
        Returns to the main menu.
        """
        # Call the display_main_menu method of the MainMenu instance.
        self.m_main_menu.display_main_menu()

    def save_and_show_result(self, result_type: str, result_data: Dict[str, Any]) -> None:
        """
        Saves the API result to the database and displays it.

        Args:
            result_type (str): The type of the API result.
            result_data (Dict[str, Any]): The data of the API result.
        """
        # Save verification result in the database.
        self.m_database_service.save_verification(result_type, result_data)

        # Display the result using the database service.
        self.m_database_service.display_result(result_type, result_data)

    def domain_search_request_menu(self) -> None:
        """
        Initiates the domain search request process.
        """
        print(f"\n{MAGENTA}You must provide the domain name or the company name!{RESET_ALL}")
        domain_to_search = input(f"{CYAN}Enter the domain to search: {RESET_ALL}")
        company_name = input(f"{YELLOW}Enter the company name (optional): {RESET_ALL}")
        # Validate that the provided domain and company fields are not empty.
        self.validate_non_empty_fields(domain_to_search, company_name)

        # Create a domain search client using the Hunter client factory.
        client = self.m_hunter_client_factory.create_domain_search()

        # Try making a domain search request and handle any potential errors.
        try:
            result = self.handle_request_error(
                client.domain_search,
                domain=domain_to_search,
                company=company_name,
                raw=True
            )

            # Process the API response using the generic method.
            self.process_api_response(result, "Domain Search")

            # Handle any exceptions that may occur during the request.
        except Exception as error:
            self.log_and_print_error(str(error))

    def email_finder_request_menu(self) -> None:
        """
        Initiates the email finder request process.
        """
        print(f"\n{MAGENTA}You must provide a domain name or company name, and you "
              "must also provide a first and last name or full name.!")
        domain_value = input(f"{CYAN}Enter the domain to search for Email: {RESET_ALL}")
        company_value = input(f"{YELLOW}Enter the company name (optional): {RESET_ALL}")
        first_name_value = input(f"{CYAN}Enter the first name: {RESET_ALL}")
        last_name_value = input(f"{CYAN}Enter the last name: {RESET_ALL}")
        full_name_value = input(f"{YELLOW}Enter the full name (optional): {RESET_ALL}")
        # Validate that required fields are provided (domain, company, first name, last name, and full name).
        self.validate_required_fields(domain_value, company_value, first_name_value, last_name_value, full_name_value)
        max_duration_value = input(
            f"{YELLOW}Enter the maximum duration of the request (3 to 20 seconds, optional): {RESET_ALL}")
        # Validate the entered maximum duration.
        self.validate_max_duration(max_duration_value)

        # Create an email finder client using the Hunter client factory.
        client = self.m_hunter_client_factory.create_email_finder()

        # Try making an email finder request and handle any potential errors.
        try:
            result = self.handle_request_error(
                client.email_finder,
                domain=domain_value,
                company=company_value,
                first_name=first_name_value,
                last_name=last_name_value,
                full_name=full_name_value,
                max_duration=max_duration_value,
                raw=True
            )

            # Process the API response for the 'Email Finder' result type.
            self.process_api_response(result, 'Email Finder')

        # Handle any exceptions that may occur during the request.
        except Exception as error:
            self.log_and_print_error(str(error))

    def email_verification_request_menu(self) -> None:
        """
        Initiates the email verification request process.
        """
        print(f"\n{MAGENTA}You must provide an email address for verification!")
        email_to_verify = input(f"{CYAN}Enter the Email to verify: {RESET_ALL}")
        # Create an email verifier client using the Hunter client factory.
        client = self.m_hunter_client_factory.create_email_verifier()

        # Try making an email verification request and handle any potential errors.
        try:
            result = self.handle_request_error(
                client.email_verifier,
                email_to_verify,
                raw=True
            )

            # Process the API response using the generic method.
            self.process_api_response(result, "Email Verification")

            # Handle JSON decoding error separately.
        except json.JSONDecodeError as error:
            self.log_and_print_error(f"JSON decoding error: {error}")

            # Handle any other exceptions that may occur during the request.
        except Exception as error:
            self.log_and_print_error(str(error))

    def email_count_request_menu(self) -> None:
        """
        Initiates the email count request process.
        """
        print(f"\n{MAGENTA}You must provide the domain name or the company name for email count!")
        domain_to_count = input(f"{CYAN}Enter the domain to count Email: {RESET_ALL}")
        company_to_count = input(f"{YELLOW}Enter the company name (optional): {RESET_ALL}")
        # Validate that required fields 'domain_to_count' and 'company_to_count' are non-empty.
        self.validate_non_empty_fields(domain_to_count, company_to_count)

        # Create an email count client using the Hunter client factory.
        client = self.m_hunter_client_factory.create_email_count()

        # Try making an email count request and handle potential errors.
        try:
            result = self.handle_request_error(
                client.email_count,
                domain=domain_to_count,
                company=company_to_count,
                raw=True
            )

            # Process the API response for the 'Email Count' result type.
            self.process_api_response(result, "Email Count")

        # Handle a specific ValueError related to the email_count method.
        except ValueError as error:
            self.log_and_print_error(f"Method email_count_menu:\nError: {error}")

        # Handle any other exceptions that may occur during the request.
        except Exception as error:
            self.log_and_print_error(str(error))

    def account_information_request_menu(self) -> None:
        """
        Initiates the account information request process.
        """
        # Create an account information client using the Hunter client factory.
        client = self.m_hunter_client_factory.create_account_information()

        # Try making an account information request and handle potential errors.
        try:
            result = self.handle_request_error(
                client.account_information,
                raw=True
            )

            # Convert the JSON response data to a dictionary.
            result_data = result.json()

            # If the 'requests' key is present in the data, rename it to 'calls'.
            if 'requests' in result_data['data']:
                result_data['data']['calls'] = result_data['data'].pop('requests')

            # Save and show the result for the 'Account Info' result type.
            self.save_and_show_result("Account Info", result_data)

            # or instead of strings (points) 269 - 277
            # self.process_api_response(result, "Account Info")

        # Handle any exceptions that may occur during the request.
        except Exception as error:
            self.log_and_print_error(str(error))

    def handle_request_error(self, func: Any, *args: Any, **kwargs: Any) -> Any:
        """
        Handles errors that may occur during an API request.

        Args:
            func (Any): The function representing the API request.
            *args (Any): Additional positional arguments for the API request.
            **kwargs (Any): Additional keyword arguments for the API request.

        Returns:
            Any: The result of the API request or an error message.
        """
        # Define a dictionary to map exception types to error messages.
        error_messages = {
            requests.exceptions.HTTPError: "HTTP Error",
            ValueError: "Invalid input",
            Exception: "Unexpected error"
        }

        try:
            # Attempt to execute the provided function with the given arguments and keyword arguments.
            return func(*args, **kwargs)

        except tuple(error_messages.keys()) as error_type:
            # Handle specific exception types defined in the error_messages dictionary.
            error_message = f"{error_type.__name__}: {error_type}"
            status_code = None
            error_response_data = None

            if isinstance(error_type, requests.exceptions.HTTPError):
                # Extract HTTP status code and attempt to decode error response as JSON.
                status_code = error_type.response.status_code
                try:
                    error_response_data = error_type.response.json()
                except json.JSONDecodeError:
                    error_response_data = "Failed to decode error response as JSON"

            # Log and print the error details.
            self.log_and_print_error(error_message, status_code, error_response_data)

        except Exception as unexpected_err:
            # Handle unexpected errors and log/print the error message.
            error_message = f"Unexpected error: {unexpected_err}"
            self.log_and_print_error(error_message)

    def log_and_print_error(self, error_message: str, status_code: Optional[int] = None,
                            error_response_data: Optional[Dict[str, Any]] = None) -> None:
        """
        Logs and prints an error message along with optional status code and response data.

        Args:
            error_message (str): The error message.
            status_code (Optional[int]): The HTTP status code (if applicable).
            error_response_data (Optional[Dict[str, Any]]): Additional error response data (if available).
        """
        # Create a formatted message with color-coded error message.
        formatted_message = f"{RED}{error_message}{RESET_ALL}"

        # Append status code information if available.
        if status_code is not None:
            formatted_message += f" - Status Code: {status_code}"

        # Append error response details if available.
        if error_response_data is not None:
            formatted_message += f" - Error Details: {error_response_data}"

        # Log the formatted message with color coding.
        self.m_logger.warning(formatted_message)

        # Print the formatted message.
        print(formatted_message)

    @staticmethod
    def get_error_message(error: Any) -> str:
        """
        Gets the appropriate error message based on the error type.

        Args:
            error (Any): The error instance.

        Returns:
            str: The error message.
        """
        # Define a dictionary mapping error types to corresponding error messages.
        error_messages = {
            requests.exceptions.HTTPError: "HTTP Error",
            ValueError: "Invalid input",
            Exception: "Unexpected error"
        }

        # Get the error message based on the type of the provided error.
        return error_messages.get(type(error), 'Unknown error')

    @staticmethod
    def validate_non_empty_fields(*values: str) -> None:
        """
        Validates that at least one of the provided fields is non-empty.

        Args:
            *values (str): The values to validate.

        Raises:
            ValueError: If all provided fields are empty.
        """
        # Check if any of the provided values are empty.
        if not any(values):
            # If all values are empty, create a message indicating which fields are required.
            field_names = " or the ".join(map(str, values))
            raise ValueError(f"{RED}You must provide at least the {field_names}{RESET_ALL}")

    @staticmethod
    def validate_required_fields(domain_value: str, company_value: str, first_name_value: str,
                                 last_name_value: str, full_name_value: str) -> None:
        """
        Validates that required fields for email finder are provided.

        Args:
            domain_value (str): The domain value.
            company_value (str): The company value.
            first_name_value (str): The first name value.
            last_name_value (str): The last name value.
            full_name_value (str): The full name value.

        Raises:
            ValueError: If required fields are missing.
        """
        # Check if either the domain or the company name is provided.
        if not any([domain_value, company_value]):
            raise ValueError(f"{RED}You must provide at least the domain or the company name.{RESET_ALL}")

        # Check if either the combination of first name and last name or the full name is provided.
        if not any([first_name_value and last_name_value, full_name_value]):
            raise ValueError(f"{RED}You must provide either the first name and last name, or the full name.{RESET_ALL}")

    @staticmethod
    def validate_max_duration(max_duration_value: str) -> None:
        """
        Validates the maximum duration value for the request.

        Args:
            max_duration_value (str): The maximum duration value.

        Raises:
            ValueError: If the maximum duration value is invalid.
        """
        # Check if max_duration_value is provided and is a digit.
        if max_duration_value and not max_duration_value.isdigit():
            raise ValueError(f"{RED}Maximum duration of the request must be a number.{RESET_ALL}")

        # If max_duration_value is provided, convert it to an integer and check if it falls within the specified range.
        if max_duration_value:
            max_duration_value = int(max_duration_value)
            if not (3 <= max_duration_value <= 20):
                raise ValueError(f"{RED}Maximum duration of the request must be from 3 to 20 seconds.{RESET_ALL}")

    def process_api_response(self, result: Any, result_type: str) -> None:
        """
        Processes the API response and saves/shows the result.

        Args:
            result (Any): The API response.
            result_type (str): The type of the API result.
        """
        # Check if the result is a dictionary containing an "error" key.
        if isinstance(result, dict) and "error" in result:
            print(f"{RED}Error: {result['error']}{RESET_ALL}")
            return

        # Check if the result is not an instance of requests.Response or if its status code is not 200.
        if not isinstance(result, requests.Response) or result.status_code != 200:
            print(f"{RED}Result.status_code != 200: {result.status_code}{RESET_ALL}")
            return

        # Extract the JSON data from the result.
        result_data = result.json()

        # Check if 'data' key is present in the result_data dictionary.
        if 'data' in result_data:
            # Save and show the result if 'data' is present.
            self.save_and_show_result(result_type, result_data['data'])
        else:
            print(f"{RED}Invalid response format{RESET_ALL}")

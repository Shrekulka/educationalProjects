# hunter_check_mail/data_base_service.py

import json
import os
import sqlite3
from typing import Dict, Any, Union

from prettytable import PrettyTable

from utils.config import Config
from utils.config import RED, RESET_ALL, MAGENTA, CYAN, YELLOW


class DatabaseService:
    """
      DatabaseService class for managing SQLite database operations.

      Attributes:
          db_path (str): The path to the SQLite database file.

      Methods:
          __init__(): Initializes a new DatabaseService instance.
          create_database(): Checks if the database file exists and creates it if not.
          save_verification(result_type: str, result_data: Dict[str, Any]) -> None:
              Saves verification data to the database.
          _recursive_save_dynamic_data(conn: sqlite3.Connection, result_type: str, type_name: str,
                                       data: Dict[str, Any], parent_key: str = '') -> None:
              Helper method for recursively saving dynamic data to the database.
          display_result(result_type: str, result_data: Union[str, Dict[str, Any]]) -> None:
              Displays the verification result.
          get_verification(key: str) -> Union[Dict[str, Union[str, Dict[str, str]]], None]:
              Retrieves verification data from the database based on the key.
          get_result_by_email(email: str) -> Union[PrettyTable, None]:
              Retrieves verification results from the database based on the email.
          get_all_results() -> None:
              Retrieves and displays all verification results from the database.
          delete_by_email(email: str) -> None:
              Deletes verification data from the database based on the email.
      """

    def __init__(self) -> None:
        """
        Initializes a new DatabaseService instance.

        Sets the database file path and creates the database if it doesn't exist.
        """
        # Get the database file path from the Config
        self.db_path: str = Config.DB_PATH
        # Create the database if it doesn't exist
        self.create_database()

    def create_database(self) -> None:
        """
        Checks if the database file exists and creates it if not.

        If the file doesn't exist, creates a new SQLite database file and defines the 'verifications' table.
        """
        # Check if the database file exists
        if not os.path.exists(self.db_path):
            # If the file doesn't exist, create it and define the schema
            print(f"Creating a new database file at: {self.db_path}")
            with sqlite3.connect(self.db_path) as conn:
                # Create 'verifications' table with necessary columns
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS verifications (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        type TEXT,
                        type_name TEXT, 
                        key TEXT UNIQUE,
                        value TEXT
                    )
                ''')

    def save_verification(self, result_type: str, result_data: Dict[str, Any]) -> None:
        """
        Saves verification data to the database.

        Args:
            result_type (str): The type of the verification result.
            result_data (Dict[str, Any]): The verification result data.
        """
        with sqlite3.connect(self.db_path) as conn:
            # Call the recursive helper method to handle nested data
            self._recursive_save_dynamic_data(conn, result_type, "TEXT", result_data)

    def _recursive_save_dynamic_data(self, conn: sqlite3.Connection, result_type: str, type_name: str,
                                     data: Dict[str, Any], parent_key: str = '') -> None:
        """
        Helper method for recursively saving dynamic data to the database.

        Args:
            conn (sqlite3.Connection): The SQLite database connection.
            result_type (str): The type of the verification result.
            type_name (str): The type name for the current data.
            data (Dict[str, Any]): The data to be saved.
            parent_key (str): The parent key for recursive calls.
        """
        for key, value in data.items():
            if isinstance(value, dict):
                # Recursively call the helper method for nested dictionaries
                self._recursive_save_dynamic_data(
                    conn, result_type, type_name, value,
                    f'{parent_key}.{key}' if parent_key else key
                )
            else:
                key_path = f'{parent_key}.{key}' if parent_key else key
                clean_key = key_path.replace('data.', '').replace('meta.', '')  # Exclude "data." and "meta."

                current_type = "meta" if "meta" in key_path else "data"
                current_key = clean_key

                try:
                    # Insert or update data in the 'verifications' table
                    conn.execute("""
                        INSERT INTO verifications (type, type_name, key, value) VALUES (?, ?, ?, ?)
                        ON CONFLICT(key) DO UPDATE SET value=excluded.value
                    """, (result_type, current_type, current_key, str(value)))
                except Exception as e:
                    print(f"Error saving data to the database: {e}")

    @staticmethod
    def display_result(result_type: str, result_data: Union[str, Dict[str, Any]]) -> None:
        """
        Displays the verification result.

        Args:
            result_type (str): The type of the verification result.
            result_data (Union[str, Dict[str, Any]]): The verification result data.
        """
        # Convert the result_data from JSON string to dictionary if it's a string
        if isinstance(result_data, str):
            result_data = json.loads(result_data)

        print(f"\nResult Type: {result_type}\n")

        # Check for errors in the response
        if 'error' in result_data:
            print(f"{RED}Request error: {result_data['error']}{RESET_ALL}")
            return

        # Check if there is data in the response
        if 'data' not in result_data:
            print(f"{RED}No data in the response{RESET_ALL}")
            return

        data = result_data["data"]

        # Display parameters and their values (excluding specific keys)
        for key, value in data.items():
            if key not in ["calls", "technologies", "emails", "linked_domains"]:
                if not isinstance(value, (list, dict)):
                    table = PrettyTable([f"{MAGENTA}Parameter{RESET_ALL}", f"{MAGENTA}Value{RESET_ALL}"])
                    table.add_row([f"{CYAN}{key}{RESET_ALL}", f"{CYAN}{value}{RESET_ALL}"])
                    print(table)

        # Display information about API calls
        if 'calls' in data:
            calls_table = PrettyTable([f"{MAGENTA}Request Type{RESET_ALL}", f"{MAGENTA}Used{RESET_ALL}",
                                       f"{MAGENTA}Available{RESET_ALL}"])
            for request_type, call_data in data['calls'].items():
                calls_table.add_row([
                    f"{YELLOW}{request_type}{RESET_ALL}",
                    f"{YELLOW}{call_data.get('used', '')}{RESET_ALL}",
                    f"{YELLOW}{call_data.get('available', '')}{RESET_ALL}"
                ])
            print(calls_table)

        # Display technologies information
        if 'technologies' in data:
            technologies_table = PrettyTable([f"{MAGENTA}Technologies{RESET_ALL}"])
            for technology in data['technologies']:
                technologies_table.add_row([f"{CYAN}{technology}{RESET_ALL}"])
            print(technologies_table)

        # Display emails information
        if 'emails' in data:
            emails_table = PrettyTable([
                f"{MAGENTA}Email{RESET_ALL}",
                f"{MAGENTA}First Name{RESET_ALL}",
                f"{MAGENTA}Last Name{RESET_ALL}"
            ])
            for email_info in data['emails']:
                email_value = email_info.get('value', '')
                first_name = email_info.get('first_name', '')
                last_name = email_info.get('last_name', '')
                emails_table.add_row([
                    f"{CYAN}{email_value}{RESET_ALL}",
                    f"{CYAN}{first_name}{RESET_ALL}",
                    f"{CYAN}{last_name}{RESET_ALL}"
                ])
            print(emails_table)

        # Display linked domains information
        if 'linked_domains' in data:
            linked_domains_table = PrettyTable([f"{MAGENTA}Linked Domains{RESET_ALL}"])
            for linked_domain in data['linked_domains']:
                linked_domains_table.add_row([f"{YELLOW}{linked_domain}{RESET_ALL}"])
            print(linked_domains_table)

        # Display verification information
        if 'verification' in data:
            verification_data = data['verification']
            verification_table = PrettyTable([f"{MAGENTA}Parameter{RESET_ALL}", f"{MAGENTA}Value{RESET_ALL}"])
            verification_table.add_row([
                f"{YELLOW}Verification Status{RESET_ALL}",
                f"{YELLOW}{verification_data.get('status', '')}{RESET_ALL}"
            ])
            verification_table.add_row([
                f"{YELLOW}Verification Date{RESET_ALL}",
                f"{YELLOW}{verification_data.get('date', '')}{RESET_ALL}"
            ])
            print(verification_table)

        # Display information about sources
        if 'sources' in data:
            sources = data['sources']
            if sources:
                sources_table = PrettyTable([
                    f"{MAGENTA}Domain{RESET_ALL}",
                    f"{MAGENTA}URI{RESET_ALL}",
                    f"{MAGENTA}Extracted On{RESET_ALL}",
                    f"{MAGENTA}Last Seen On{RESET_ALL}",
                    f"{MAGENTA}Still On Page{RESET_ALL}"
                ])
                for source in sources:
                    domain = source.get('domain', '')
                    uri = source.get('uri', '')
                    extracted_on = source.get('extracted_on', '')
                    last_seen_on = source.get('last_seen_on', '')
                    still_on_page = source.get('still_on_page', False)

                    sources_table.add_row([
                        f"{YELLOW}{domain}{RESET_ALL}",
                        f"{YELLOW}{uri}{RESET_ALL}",
                        f"{YELLOW}{extracted_on}{RESET_ALL}",
                        f"{YELLOW}{last_seen_on}{RESET_ALL}",
                        f"{YELLOW}{still_on_page}{RESET_ALL}"
                    ])
                print(sources_table)
            else:
                print(f"{YELLOW}Sources not found.{RESET_ALL}")

    def get_verification(self, key: str) -> Union[Dict[str, Union[str, Dict[str, str]]], None]:
        """
        Retrieves verification data from the database based on the key.

        Args:
            key (str): The key used for retrieval.

        Returns:
            Union[Dict[str, Union[str, Dict[str, str]]], None]: The retrieved data or None if not found.
        """
        # Establish a connection to the database
        with sqlite3.connect(self.db_path) as conn:
            # Execute SQL query to select verification data based on the key
            cursor = conn.execute("SELECT type, type_name, key, value FROM verifications WHERE key = ?", (key,))
            result = cursor.fetchone()
            # Return the retrieved data as a dictionary or None if not found
            return {'type': result[0], 'data': {result[1]: result[3]}} if result else None

    def get_result_by_email(self, email: str) -> Union[PrettyTable, None]:
        """
        Retrieves verification results from the database based on the email.

        Args:
            email (str): The email used for retrieval.

        Returns:
            Union[PrettyTable, None]: The retrieved results or None if not found.
        """
        # Establish a connection to the database
        with sqlite3.connect(self.db_path) as conn:
            # Execute SQL query to select all verification results
            cursor = conn.execute("SELECT type, type_name, key, value FROM verifications")

            # Fetch all results
            results = cursor.fetchall()

            # Create a PrettyTable for displaying results
            table = PrettyTable()
            table.field_names = [f"{MAGENTA}Type{RESET_ALL}", f"{MAGENTA}Type Name{RESET_ALL}",
                                 f"{MAGENTA}Key{RESET_ALL}", f"{MAGENTA}Value{RESET_ALL}"]

            # Iterate through results
            for result in results:
                try:
                    # Convert result data to string
                    data = str(result[3])
                    # Check if the email is in the data
                    if email in data:
                        table.add_row([result[0], result[1], result[2], result[3]])
                except Exception as e:
                    print(f"Error processing data: {e}")

            # Display results if any, else print a message
            if len(table.field_names) > 0:
                print(f"{CYAN}Results for email: {email}{RESET_ALL}")
                print(table)
                return table
            else:
                print(f"{CYAN}No results found for email: {email}{RESET_ALL}")
                return None

    def get_all_results(self) -> None:
        """
        Retrieves and displays all verification results from the database.
        """
        # Establish a connection to the database
        with sqlite3.connect(self.db_path) as conn:
            # Execute SQL query to select all verification results
            cursor = conn.execute("SELECT type, key, value FROM verifications")
            results = cursor.fetchall()

        # Display results if any, else print a message
        if not results:
            print(f"{RED}No results found.{RESET_ALL}")
            return

        # Create a PrettyTable for displaying results
        table = PrettyTable([f"{MAGENTA}Type{RESET_ALL}", f"{MAGENTA}Key{RESET_ALL}", f"{MAGENTA}Value{RESET_ALL}"])
        # Add results to the table
        for result in results:
            table.add_row(result)

        # Print the table
        print(table)

    def delete_by_email(self, email: str) -> None:
        """
        Deletes verification data from the database based on the email.

        Args:
            email (str): The email used for deletion.
        """
        # Establish a connection to the database
        with sqlite3.connect(self.db_path) as conn:
            # Execute SQL query to select IDs of verification data to be deleted
            cursor = conn.execute("SELECT id FROM verifications WHERE value LIKE ?", (f"%{email}%",))
            # Extract IDs to be deleted
            ids_to_delete = [row[0] for row in cursor.fetchall()]

            # Check if there are IDs to be deleted
            if ids_to_delete:
                # Convert IDs to a comma-separated string
                ids_str = ",".join(map(str, ids_to_delete))
                # Build and execute the delete query
                delete_query = f"DELETE FROM verifications WHERE id IN ({ids_str})"
                conn.execute(delete_query)
                print(f"{YELLOW}Data for email {email} was successfully deleted.{RESET_ALL}")
            else:
                print(f"{YELLOW}No data found for email: {email}{RESET_ALL}")

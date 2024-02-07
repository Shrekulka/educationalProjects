# numbers_api_explorer/numbers_menu.py

from datetime import datetime

import requests
from colorama import Fore, Style

from config import API_BASE_URL, RANDOM_CATEGORIES
from logger import logger


class NumbersMenu:
    """
        NumbersMenu - a class for user interaction in the Numbers API Explorer program.

        Methods:
            - __init__: Initializes an instance of the NumbersMenu class.
            - print_menu: Displays the main menu of the program on the screen.
            - get_user_choice: Retrieves the user's choice from standard input.
            - process_user_choice: Processes the user's choice.
            - make_request: Sends a request to the API with the specified parameters and returns the result.
            - build_url: Builds a URL for the request based on the specified parameters.
            - show_result: Displays the result of the request on the screen.
            - is_date_category: Checks if the request category is "date".
            - handle_error: Handles an error, prints an error message, and returns error details.
    """
    EXIT_OPTION = "0"   # Константа для выхода из меню
    MIN_MENU_INDEX = 1  # Минимальный индекс в меню

    def __init__(self):
        """
            Initializes an instance of the NumbersMenu class.

            Attributes:
                - self.api_base_url (str): Base URL for the Numbers API.
                - self.random_categories (list): List of random categories for requests.
        """

        self.api_base_url = API_BASE_URL
        self.random_categories = RANDOM_CATEGORIES

    @staticmethod
    def print_menu() -> None:
        """
            Displays the main menu of the program on the screen.

            Returns:
                None
        """
        print(f"\n{Fore.CYAN}Welcome to the Numbers Comedy Club!{Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}1. {Fore.GREEN}🧮 Magic of Mathematics (not for the faint-hearted){Style.RESET_ALL}")
        print(f"{Fore.YELLOW}2. {Fore.GREEN}🤓 Interesting Facts (get ready to be amazed){Style.RESET_ALL}")
        print(f"{Fore.YELLOW}3. {Fore.GREEN}🗓️ Time Travel (or at least to yesterday){Style.RESET_ALL}")
        print(f"{Fore.YELLOW}4. {Fore.GREEN}🎲 Random Number (or how I decided what to cook for dinner)"
              f"{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}0. {Fore.GREEN}🚪 Exit (but exit with a smile){Style.RESET_ALL}")

    @staticmethod
    def get_user_choice() -> str:
        """
            Retrieves the user's choice from standard input.

            Returns:
                str: The user-entered choice.
        """

        return input(f"\n{Fore.BLUE}🤔 Choose a category and get ready for some fun "
                     f"(or enter 0 to exit): {Style.RESET_ALL}")

    def process_user_choice(self, choice: str) -> None:
        """
            Processes the user's choice.

            Args:
                choice (str): The user's choice.

            Returns:
                None
        """
        if choice == self.EXIT_OPTION:
            print(f"{Fore.MAGENTA}It was fun, hope you leave with a smile! 🤣{Style.RESET_ALL}")
            return

        try:
            index = int(choice)
            # Получение категории на основе выбора пользователя
            if self.MIN_MENU_INDEX <= index <= len(self.random_categories):
                category = self.random_categories[index - 1]
                # Если категория - дата, запрашиваем у пользователя ввод даты
                if self.is_date_category(category):
                    date_input = input(
                        f"\n{Fore.MAGENTA}Enter the day of the year in the format month/day "
                        f"(e.g., 2/28, 1/09, 04/1): {Style.RESET_ALL}")
                    try:
                        # Попытка преобразования введенной даты в объект datetime
                        date_object = datetime.strptime(date_input, "%m/%d")
                        # Отправка запроса к API с указанной датой
                        result = self.make_request(category.lower(), date_object.month, date_object.day)
                    # Обработка ошибки в случае некорректного формата ввода даты
                    except ValueError as error:
                        self.handle_error(error, f"Input format error. Please enter a "
                                                 f"valid date in the format month/day: {str(error)}")
                        return
                # Если категория содержит "RANDOM", отправляем запрос на случайное число
                elif "RANDOM" in category:
                    result = self.make_request(category.replace("RANDOM ", "").lower())
                # Если категория не "date" и не содержит "RANDOM", запрашиваем у пользователя ввод числа
                else:
                    number = int(input(f"\n{Fore.MAGENTA}Enter a number (if unsure, enter, for example, "
                                       f"the number of penguins in your bathtub): {Style.RESET_ALL}"))
                    # Отправка запроса к API с указанным числом
                    result = self.make_request(category.lower(), number)
                # Вывод результата запроса на экран
                self.show_result(result)
            # Вывод сообщения об ошибке при некорректном выборе пользователя
            else:
                print(f"{Fore.RED}Oops! Looks like we have a little hiccup... Incorrect choice! 😅 "
                      f"Please choose an existing category and give it another shot.{Style.RESET_ALL}")
        # Вывод сообщения об ошибке при некорректном вводе числа
        except ValueError:
            print(f"{Fore.RED}Oops! Incorrect input. Please enter a number from 0 to"
                  f" {len(self.random_categories)}. 😅{Style.RESET_ALL}")

    def make_request(self, category: str, *numbers: int) -> str:
        """
            Sends a request to the API with the specified parameters and returns the result.

            Args:
                category (str): The category of the request.
                numbers (int): The parameters of the request.

            Returns:
                str: The result of the request.
        """
        logger.debug(f"Making request for category: {category}, numbers: {numbers}")
        # Формирование URL для запроса
        url = self.build_url(category, *numbers)
        try:
            # Отправка GET-запроса к API
            response = requests.get(url)
            response.raise_for_status()
            # Возвращение текстового ответа от API
            return response.text
        # Обработка ошибки запроса и возврат сообщения об ошибке
        except requests.exceptions.RequestException as e:
            return self.handle_error(e, "Error while sending a request to the API")

    def build_url(self, category: str, number1: int = None, number2: int = None) -> str:
        """
            Builds a URL for the request based on the specified parameters.

            Args:
                category (str): The category of the request.
                number1 (int): The first parameter.
                number2 (int): The second parameter.

            Returns:
                str: The constructed URL.
        """
        # Формирование базовой части URL с учетом наличия/отсутствия первого числа
        base_url = f"{self.api_base_url}/" if number1 is None else f"{self.api_base_url}/"
        # Добавление чисел и категории к URL в формате "number1/number2/category"
        if number1 is not None and number2 is not None:
            base_url += f"{number1:02d}/{number2:02d}/{category}"
        # Добавление первого числа и категории к URL в формате "number1/category"
        elif number1 is not None:
            base_url += f"{number1:02d}/{category}"
        # Добавление только категории в нижнем регистре к URL
        else:
            base_url += f"{category.lower()}"

        logger.debug(f"Api_base_url: {base_url}")
        return base_url

    @staticmethod
    def show_result(result: str) -> None:
        """
            Displays the result of the request on the screen.

            Args:
                result (str): The result of the request.

            Returns:
                None
        """
        print(f"\n{Fore.RED}🎉 Here's your long-awaited result:\n"
              f"{Style.RESET_ALL}{Fore.GREEN}{result}{Style.RESET_ALL}\n")

    @staticmethod
    def is_date_category(category: str) -> bool:
        """
            Checks if the request category is "date".

            Args:
                category (str): The category of the request.

            Returns:
                bool: True if the category is "date", otherwise False.
        """
        return category.lower() == "date"

    @staticmethod
    def handle_error(error: Exception, error_message: str) -> str:
        """
            Handles an error, prints an error message, and returns error details.

            Args:
                error (Exception): The error object.
                error_message (str): The error message.

            Returns:
                str: Error details.
        """
        logger.error(error_message, exc_info=True)
        print(f"{Fore.RED}Don't worry, I'm always ready for unexpected situations! 😅{Style.RESET_ALL}")
        return f"Errors like this can happen: {str(error)}"

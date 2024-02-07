# numbers_api_explorer/main.py
import traceback

from logger import logger
from numbers_menu import NumbersMenu


def main() -> None:
    """
        The main function of the program.

        Creates an instance of the NumbersMenu class and initiates an infinite loop for interacting with the user.

        Returns:
            None
    """
    # Создание экземпляра класса NumbersMenu
    numbers_menu = NumbersMenu()

    # Бесконечный цикл для взаимодействия с пользователем
    while True:
        # Вывод меню на экран
        numbers_menu.print_menu()

        # Получение выбора пользователя
        choice = numbers_menu.get_user_choice()

        # Обработка выбора пользователя
        numbers_menu.process_user_choice(choice)


# Запуск основной функции, если скрипт запущен как отдельный файл
if __name__ == "__main__":
    try:
        # Вызов функции main() при запуске программы
        main()
    except KeyboardInterrupt:
        # Обработка прерывания программы пользователем
        logger.info("Program interrupted by user")
    except Exception as e:
        # Обработка неожиданных ошибок и логирование
        detailed_error_traceback = traceback.format_exc()
        logger.error(f"An unexpected error occurred: {e}\n{detailed_error_traceback}")

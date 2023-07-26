import sys
from menu import Menu


def main():
    """
    Основная функция программы.
    Создает экземпляр класса Menu и запускает его метод run().
    """
    # Создаем экземпляр класса Menu и передаем ему аргумент database=None
    menu = Menu(database=None)
    menu.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")
        sys.exit()

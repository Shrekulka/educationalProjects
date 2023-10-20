class Command:
    """
    Класс, представляющий команду в оболочке FAT32.
    """

    def __init__(self, func: callable, description: str):
        """
        Инициализирует объект команды.

        Args:
            func (callable): Функция, которую должна выполнить команда. Ожидается объект callable (функция).
            description (str): Описание команды. Ожидается строка (str).
        """
        self.func = func  # Присваивание функции команде
        self.description = description  # Присваивание описания команде

    def execute(self, args: list) -> None:
        """
        Выполняет команду, вызывая соответствующую функцию с аргументами.

        Args:
            args (list): Список аргументов, передаваемых в функцию команды. Ожидается список (list).

        Returns:
            None: Этот метод не возвращает значения.
        """
        self.func(*args)

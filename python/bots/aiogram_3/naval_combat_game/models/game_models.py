# naval_combat_game/models/game_models.py

from random import randint

from config_data.game_config_data import FIELD_SIZE
from logger_config import logger

# Словарь, определяющий количество кораблей различных размеров
SHIPS_COUNT = {
    3: 2,  # Два трехпалубных корабля
    2: 3,  # Три двухпалубных корабля
    1: 4   # Четыре однопалубных корабля
}


def generate_ships(is_user: bool = True) -> list[list[int]]:
    """
       Generates a game field with ships placed randomly.

       This function generates a game field with ships placed according to predefined rules.
       It ensures that ships do not overlap or touch each other diagonally.

       Returns:
           list[list[int]]: A 2D list representing the game field with ships placed.
    """
    # Создаем пустое игровое поле размером FIELD_SIZE x FIELD_SIZE
    field = [[0 for _ in range(FIELD_SIZE)] for _ in range(FIELD_SIZE)]

    # Для каждого размера корабля из словаря SHIPS_COUNT
    for ship_size, ship_count in SHIPS_COUNT.items():
        # Создаем указанное количество кораблей заданного размера
        for _ in range(ship_count):
            # Бесконечный цикл для размещения кораблей
            while True:
                # Случайно определяем, будет ли корабль вертикальным (1) или горизонтальным (0)
                is_vertical = randint(0, 1)
                # Случайно выбираем начальные координаты для корабля
                x = randint(0, FIELD_SIZE - 1)
                y = randint(0, FIELD_SIZE - 1)

                # Если корабль вертикальный
                if is_vertical:
                    # Проверяем, влезет ли корабль в игровое поле по вертикали
                    if x + ship_size > FIELD_SIZE:
                        continue

                    # Проверяем, можно ли разместить корабль в выбранной позиции, проверяя соприкосновения
                    can_place = True
                    for i in range(ship_size):
                        # Проверка соприкосновений по вертикали и диагонали
                        if (x + i < FIELD_SIZE and field[x + i][y] == 1) or \
                                (x > 0 and field[x - 1][y] == 1) or \
                                (x + i < FIELD_SIZE - 1 and field[x + i + 1][y] == 1) or \
                                (y > 0 and field[x + i][y - 1] == 1) or \
                                (y < FIELD_SIZE - 1 and field[x + i][y + 1] == 1) or \
                                (x > 0 and y > 0 and field[x - 1][y - 1] == 1) or \
                                (x + i < FIELD_SIZE - 1 and y > 0 and field[x + i + 1][y - 1] == 1) or \
                                (x > 0 and y < FIELD_SIZE - 1 and field[x - 1][y + 1] == 1) or \
                                (x + i < FIELD_SIZE - 1 and y < FIELD_SIZE - 1 and field[x + i + 1][y + 1] == 1):
                            can_place = False
                            break

                # Если корабль горизонтальный
                else:
                    # Проверяем, влезет ли корабль в игровое поле по горизонтали
                    if y + ship_size > FIELD_SIZE:
                        continue

                    # Проверяем, можно ли разместить корабль в выбранной позиции, проверяя соприкосновения
                    can_place = True
                    for i in range(ship_size):
                        # Проверка соприкосновений по горизонтали и диагонали
                        if (y + i < FIELD_SIZE and field[x][y + i] == 1) or \
                                (y > 0 and field[x][y + i - 1] == 1) or \
                                (y + i < FIELD_SIZE - 1 and field[x][y + i + 1] == 1) or \
                                (x > 0 and field[x - 1][y + i] == 1) or \
                                (x < FIELD_SIZE - 1 and field[x + 1][y + i] == 1) or \
                                (x > 0 and y > 0 and field[x - 1][y - 1] == 1) or \
                                (y + i < FIELD_SIZE - 1 and x > 0 and field[x - 1][y + i + 1] == 1) or \
                                (x < FIELD_SIZE - 1 and y > 0 and field[x + 1][y - 1] == 1) or \
                                (x < FIELD_SIZE - 1 and y + i < FIELD_SIZE - 1 and field[x + 1][y + i + 1] == 1):
                            can_place = False
                            break

                # Если можно разместить корабль, размещаем его и завершаем цикл
                if can_place:
                    if is_vertical:
                        for i in range(ship_size):
                            field[x + i][y] = 1
                    else:
                        for i in range(ship_size):
                            field[x][y + i] = 1
                    break

    # Выводим игровое поле для отладки
    print_field(field)
    # Возвращаем сгенерированное игровое поле
    return field


def print_field(field: list[list[int]]) -> None:
    """
        Prints the game field with ship positions.

        This function prints the current state of the game field with ship positions represented by 1s.

        Args:
            field (list[list[int]]): A 2D list representing the game field.
    """
    # Создаем заголовок поля, указывающий на буквенные метки столбцов
    field_str = "  A B C D E F G H\n"

    # Перебираем строки игрового поля с помощью enumerate, начиная с 1
    for i, row in enumerate(field, start=1):
        # Создаем строку для текущей строки поля, включая числовую метку строки
        row_str = f"{i} " + " ".join(map(str, row)) + "\n"
        # Добавляем строку текущей строки поля к строке field_str
        field_str += row_str

    # Отправляем сформированное игровое поле в лог, используя логгер, и включаем его в сообщение с отступом
    logger.info(f"\n{field_str}")

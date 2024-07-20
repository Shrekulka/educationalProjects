# zodiac_portal/horoscope/models.py

from datetime import datetime


class ZodiacSign:
    """
        Представляет знак зодиака с его именем, описанием и соответствующим временным диапазоном.

        Attributes:
            name (str): Имя знака зодиака.
            description (str): Описание или характеристики знака зодиака.
            start_date (tuple): Начальная дата периода знака зодиака в формате (месяц, день).
            end_date (tuple): Конечная дата периода знака зодиака в формате (месяц, день).
    """

    def __init__(self, name: str, description: str, start_date: tuple, end_date: tuple):
        """
            Инициализирует объект ZodiacSign.

            Args:
                name (str): Имя знака зодиака.
                description (str): Описание или характеристики знака зодиака.
                start_date (tuple): Начальная дата периода знака зодиака в формате (месяц, день).
                end_date (tuple): Конечная дата периода знака зодиака в формате (месяц, день).
        """
        self.name = name                # Присваиваем переданное имя знака зодиака.
        self.description = description  # Присваиваем  переданное описание знака зодиака.
        self.start_date = start_date    # Присваиваем переданный кортеж начальной даты знака зодиака.
        self.end_date = end_date        # Присваиваем переданный кортеж конечной даты знака зодиака.

    def __str__(self) -> str:
        """
            Возвращает строковое представление объекта ZodiacSign.

            Returns:
                str: Строка, содержащая имя и описание знака зодиака.
        """
        # Возвращаем строку, содержащую имя знака зодиака (с заглавной буквы) и его описание.
        return f"{self.name.title()} - {self.description}"


class ZodiacSigns:
    """
        Представляет коллекцию всех знаков зодиака с методами для получения знаков по различным критериям.

        Attributes:
            signs (list): Список объектов ZodiacSign, представляющих все знаки зодиака.
            signs_dict (dict): Словарь, отображающий имена знаков зодиака на объекты ZodiacSign.
            types (dict): Словарь, отображающий типы элементов ('fire', 'earth', 'air', 'water')
                          на списки имен знаков зодиака, принадлежащих каждому элементу.
    """

    def __init__(self):
        """
           Инициализирует объект ZodiacSigns, заполняя список знаков зодиака.
        """
        # Инициализируем список знаков зодиака с их именами, описаниями и периодами.
        self.signs = [
            ZodiacSign('aries', 'Овен - первый знак зодиака, планета Марс (с 21 марта по 20 апреля).',
                       (3, 21), (4, 20)),
            ZodiacSign('taurus', 'Телец - второй знак зодиака, планета Венера (с 21 апреля по 21 мая).',
                       (4, 21), (5, 21)),
            ZodiacSign('gemini', 'Близнецы - третий знак зодиака, планета Меркурий (с 22 мая по 21 июня).',
                       (5, 22), (6, 21)),
            ZodiacSign('cancer', 'Рак - четвёртый знак зодиака, Луна (с 22 июня по 22 июля).',
                       (6, 22), (7, 22)),
            ZodiacSign('leo', 'Лев - пятый знак зодиака, солнце (с 23 июля по 21 августа).',
                       (7, 23), (8, 21)),
            ZodiacSign('virgo', 'Дева - шестой знак зодиака, планета Меркурий (с 22 августа по 23 сентября).',
                       (8, 22), (9, 23)),
            ZodiacSign('libra', 'Весы - седьмой знак зодиака, планета Венера (с 24 сентября по 23 октября).',
                       (9, 24), (10, 23)),
            ZodiacSign('scorpio', 'Скорпион - восьмой знак зодиака, планета Марс (с 24 октября по 22 ноября).',
                       (10, 24), (11, 22)),
            ZodiacSign('sagittarius', 'Стрелец - девятый знак зодиака, планета Юпитер (с 23 ноября по 22 декабря).',
                       (11, 23), (12, 22)),
            ZodiacSign('capricorn', 'Козерог - десятый знак зодиака, планета Сатурн (с 23 декабря по 20 января).',
                       (12, 23), (1, 20)),
            ZodiacSign('aquarius',
                       'Водолей - одиннадцатый знак зодиака, планеты Уран и Сатурн (с 21 января по 19 февраля).',
                       (1, 21), (2, 19)),
            ZodiacSign('pisces', 'Рыбы - двенадцатый знак зодиака, планеты Юпитер (с 20 февраля по 20 марта).',
                       (2, 20), (3, 20))
        ]
        # Создаем словарь знаков зодиака, где ключом является имя знака, а значением - объект знака зодиака.
        self.signs_dict = {sign.name: sign for sign in self.signs}
        # Инициализируем словарь, где ключами являются элементы (огонь, земля, воздух, вода), а значениями - списки
        # знаков зодиака, принадлежащих каждому элементу.
        self.types = {
            'fire': ['aries', 'leo', 'sagittarius'],
            'earth': ['taurus', 'virgo', 'capricorn'],
            'air': ['gemini', 'libra', 'aquarius'],
            'water': ['cancer', 'scorpio', 'pisces'],
        }

    def get_sign(self, sign_name: str) -> ZodiacSign:
        """
            Возвращает объект ZodiacSign по его имени.

            Args:
                sign_name (str): Имя знака зодиака для поиска.

            Returns:
                ZodiacSign: Объект ZodiacSign, соответствующий указанному имени,
                            или None, если знак не найден.
        """
        # Возвращаем объект знака зодиака из словаря по имени знака, приведенному к нижнему регистру. Если знак не
        # найден, возвращаем None.
        return self.signs_dict.get(sign_name.lower())

    def get_sign_by_number(self, number: int) -> ZodiacSign | None:
        """
            Возвращает объект ZodiacSign по его порядковому номеру.

            Args:
                number (int): Порядковый номер знака зодиака (от 1 до 12).

            Returns:
                ZodiacSign: Объект ZodiacSign на указанной позиции,
                            или None, если номер вне диапазона.
        """
        # Проверяем, находится ли переданный номер в пределах допустимого диапазона (от 1 до количества знаков зодиака).
        if 1 <= number <= len(self.signs):
            # Возвращаем знак зодиака из списка по индексу (номер - 1, так как индексация списка начинается с 0).
            return self.signs[number - 1]
        # Если номер вне допустимого диапазона, возвращаем None.
        return None

    def get_all_types(self) -> list:
        """
            Возвращает список всех типов элементов зодиака.

            Returns:
                list: Список строк, представляющих типы элементов зодиака ('fire', 'earth', 'air', 'water').
        """
        # Возвращаем список всех элементов (ключей) из словаря типов знаков зодиака.
        return list(self.types.keys())

    def get_signs_by_element(self, element: str) -> list:
        """
            Возвращает список объектов ZodiacSign, принадлежащих определенному типу элемента зодиака.

            Args:
                element (str): Тип элемента зодиака ('fire', 'earth', 'air', 'water').

            Returns:
                list: Список объектов ZodiacSign, принадлежащих указанному типу элемента.
        """
        # Берем из словаря типов (self.types) список знаков, относящихся к элементу (ключ элемент приводим к нижнему
        # регистру).
        # Если элемент не найден в словаре, возвращаем пустой список.
        # Затем получаем объекты знаков зодиака из словаря знаков (self.signs_dict) по именам из полученного списка.
        return [self.signs_dict[sign] for sign in self.types.get(element.lower(), [])]

    def get_all_signs(self) -> list:
        """
            Возвращает список всех объектов ZodiacSign.

            Returns:
                list: Список всех объектов ZodiacSign.
        """
        # Возвращаем список всех знаков зодиака.
        return self.signs

    def get_sign_by_date(self, month: int, day: int) -> ZodiacSign | None:
        """
            Возвращает объект ZodiacSign, соответствующий заданной дате.

            Args:
                month (int): Месяц (от 1 до 12) даты.
                day (int): День (от 1 до 31) даты.

            Returns:
                ZodiacSign: Объект ZodiacSign, соответствующий указанной дате,
                            или None, если ни один знак не соответствует дате.
        """
        # Создаем объект даты для указанного месяца и дня, используя невисокосный год (2000) для упрощения.
        date = datetime(2000, month, day)
        # Проходим по всем знакам зодиака.
        for sign in self.signs:
            # Создаем объект даты для начала периода знака, используя год 2000.
            start = datetime(2000, sign.start_date[0], sign.start_date[1])
            # Создаем объект даты для конца периода знака, используя год 2000.
            end = datetime(2000, sign.end_date[0], sign.end_date[1])
            # Проверяем, находится ли указанная дата в пределах периода знака.
            if start <= date <= end:
                # Если да, возвращаем текущий знак зодиака.
                return sign
            # Особый случай для Козерога, так как его период включает переход через Новый год.
            if sign.name == 'capricorn':
                # Проверяем, находится ли дата либо в начале периода Козерога (в декабре), либо в конце (в январе).
                if date >= start or date <= end:
                    # Если да, возвращаем знак Козерога.
                    return sign
        # Если дата не попадает в период ни одного знака зодиака, возвращаем None.
        return None


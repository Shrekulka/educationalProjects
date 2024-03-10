# edit_messages/services/services.py

from random import randint

from lexicon.lexicon import jokes


# Функция, генерирующая случайное число в диапазоне от 1 до длины словаря jokes
def random_joke() -> int:
    """
        Generates a random number in the range from 1 to the length of the 'jokes' dictionary and returns it.
    
        Returns:
            int: A random number in the range from 1 to the length of the 'jokes' dictionary.
    """
    # Возвращение случайного числа в диапазоне от 1 до длины словаря jokes
    return randint(1, len(jokes))

"""Описание игры: "Угадай карту"

Цель игры - угадать различные характеристики случайно выбранной карты из колоды. Игрок должен угадать цвет карты
(красный или черный), масть (пики, червы, бубны или трефы), значение карты (2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, A)
или и значение, и масть карты одновременно. В каждом раунде генерируется случайная карта и игроку предлагается сделать
свою ставку. Всего игроку дается 6 попыток на каждый тип вопроса. В конце игры игрок получает свой результат в виде
количества правильных и неправильных ответов.

Перед игрой необходимо импортировать sys и модуль random. Определены следующие константы: список мастей, список
значений, список мастей в виде словаря.

Функция generate_random_card() генерирует случайную карту из колоды и возвращает кортеж со значением и мастью карты.

Функция response_to_the_player(right_answers, wrong_answers) принимает количество правильных и неправильных ответов и
выводит сообщение об итогах игры.

Функция handle_invalid_input() выводит сообщение об ошибке ввода данных.

Функция guess_color() отвечает за угадывание цвета карты. В каждом раунде генерируется случайная карта и игроку
предлагается угадать цвет (красный или черный). После каждой попытки выводится сообщение с результатом. В конце игры
вызывается функция response_to_the_player().

Функция guess_suit() отвечает за угадывание масти карты. В каждом раунде генерируется случайная карта и игроку
предлагается угадать масть (пики, червы, бубны или трефы). После каждой попытки выводится сообщение с результатом.
В конце игры вызывается функция response_to_the_player().

Функция guess_card_value() отвечает за угадывание значения карты. В каждом раунде генерируется случайная карта и
игроку предлагается угадать значение (2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, A). После каждой попытки выводится
сообщение с результатом. В конце игры вызывается функция response_to_the_player().

Функция guess_card_value_and_suit() отвечает за угадывание значения и масти карты. В каждом раунде генерируется
случайная карта и игроку предлагается угадать значение и масть одновременно. После каждой попытки выводится сообщение
с результатом. В конце игры вызывается функция response_to_the_player()."""

import sys
from random import choice

# список мастей карт
CARD_SUIT = ['clubs', 'spades', 'diamonds', 'hearts']
# список значений карт
CARD_VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
# словарь, сопоставляющий первую букву масти с названием масти
CARD_SUIT_LIST = {'c': 'clubs', 'd': 'diamonds', 'h': 'hearts', 's': 'spades'}


# функция генерации случайной карты
def generate_random_card():
    # выбираем случайное значение карты из списка CARD_VALUES и случайную масть карты из списка CARD_SUIT
    return choice(CARD_VALUES), choice(CARD_SUIT)


# функция для вывода ответа игроку
def response_to_the_player(right_answers, wrong_answers):
    response = f"Out of five rounds you answered correctly {right_answers} times and answered incorrectly " \
               f"{wrong_answers} times."
    if right_answers == 5:
        print(response, "Vanga may envy you.")
    elif right_answers in range(2, 5):
        print(response, "You are well done.")
    else:
        print(response, "You need a little more practice.")


# функция для обработки некорректного ввода
def handle_invalid_input():
    print("Invalid input! Please enter clubs (c) or spades (s) or diamonds (d) or hearts (h), "
          "a card value (2-10, J, Q, K, A), or a card color (red(r) or black(b)).")


# игра "угадай цвет карты"
def guess_color():
    # создаем переменные для правильных и неправильных ответов
    right_answers = 0
    wrong_answers = 0
    # цикл на 6 итераций для 6 карт
    for _ in range(6):
        card = generate_random_card()  # генерируем случайную карту
        card_suit = card[1]  # получаем масть карты
        player_answer = input(f"Select card color (red(r) or black(b)): ").lower()
        try:
            # если ответ игрока - r или b, то проверяем, совпадает ли цвет карты
            if player_answer in ['r', 'b']:
                # если цвет угадан верно, увеличиваем счетчик правильных ответов
                if player_answer == 'r' and card_suit in ['diamonds', 'hearts']:
                    print(
                        f"Congratulations, you guessed the color of the card!!! The card was", *card)
                    right_answers += 1
                elif player_answer == 'b' and card_suit in ['clubs', 'spades']:
                    print(
                        f"Congratulations, you guessed the color of the card!!! The card was", *card)
                    right_answers += 1
                # если цвет неверен, увеличиваем счетчик неправильных ответов
                else:
                    print(f"You didn't guess the color. The card was", *card)
                    wrong_answers += 1
            # если ответ пользователя некорректен, обрабатываем исключение
            else:
                handle_invalid_input()
                continue
        except ValueError:
            handle_invalid_input()
            continue
    # выводим результаты игры
    response_to_the_player(right_answers, wrong_answers)


# игра "угадай масть карты"
def guess_suit():
    # создаем переменные для правильных и неправильных ответов
    right_answers = 0
    wrong_answers = 0
    # цикл на 6 итераций для 6 карт
    for _ in range(6):
        card = generate_random_card()  # генерация случайной карты
        card_suit = card[1]  # определение масти текущей карты
        player_answer = input(f"Choose a card suit (clubs (c), spades (s), diamonds (d), hearts (h)): ").lower()
        try:
            # если пользователь ввел допустимую масть карты
            if player_answer in CARD_SUIT_LIST:
                # если пользователь угадал масть карты, увеличиваем счетчик правильных ответов
                if CARD_SUIT_LIST[player_answer] == card_suit:
                    print(f"Congratulations, you guessed the suit of the card! The card was", *card)
                    right_answers += 1
                # если масть неверна, увеличиваем счетчик неправильных ответов
                else:
                    print(f"You didn't guess the suit. The card was", *card)
                    wrong_answers += 1
            # если ответ пользователя некорректен, обрабатываем исключение
            else:
                handle_invalid_input()
                continue
        except ValueError:
            handle_invalid_input()
            continue
    # выводим результаты игры
    response_to_the_player(right_answers, wrong_answers)


# игра "угадай значение карты"
def guess_card_value():
    # создаем переменные для правильных и неправильных ответов
    right_answers = 0
    wrong_answers = 0
    for _ in range(6):
        card = generate_random_card()  # генерация случайной карты
        card_value = card[0]  # определение значение текущей карты
        player_answer = input("Choose a card value (2-10, J, Q, K, A): ").lower()
        try:
            # проверяем, что пользователь ввел корректное значение карты
            if player_answer in CARD_VALUES:
                # если пользователь угадал значение карты
                if player_answer == card_value:
                    print("Congratulations, you guessed the card value!!! The card was", *card)
                    right_answers += 1
                # если значение карты неверно, увеличиваем счетчик неправильных ответов
                else:
                    print("You didn't guess the card value. The card was", *card)
                    wrong_answers += 1
            # если ответ пользователя некорректен, обрабатываем исключение
            else:
                raise ValueError
        except ValueError:
            print("Invalid input! Please enter a card value (2-10, J, Q, K, A).")
    # выводим результаты игры
    response_to_the_player(right_answers, wrong_answers)


# игра "угадай значение карты и масть карты"
def guess_card_value_and_suit():
    # создаем переменные для правильных и неправильных ответов
    right_answers = 0
    wrong_answers = 0
    # цикл на 6 итераций для 6 карт
    for _ in range(6):
        card = generate_random_card()  # генерация случайной карты
        player_answer = input("Choose a card value and suit (for example: 2d, 10h, Qs): ").lower()
        # Проверяется корректность введенного значения: длина ответа должна быть 2 или 3 символа, первый символ -
        # значение карты (2-10, j, q, k, a), второй или второй и третий символы - масть карты (c, s, d, h).
        if len(player_answer) != 2 and len(player_answer) != 3:
            # Если введенное значение некорректно, вызывается функция handle_invalid_input() и цикл продолжается со
            # следующей итерации.
            handle_invalid_input()
            continue
        value = player_answer[0]
        suit = player_answer[1:]
        try:
            # Если введенное значение корректно, проверяется, совпадает ли введенное значение с значением и мастью
            # случайно сгенерированной карты. Если да, то выводится сообщение о правильном ответе, иначе - сообщение о
            # неправильном ответе и увеличивается количество неправильных ответов (wrong_answers).
            if value not in CARD_VALUES and value not in ['j', 'q', 'k', 'a'] or suit[0] not in ['c', 's', 'd', 'h']:
                raise ValueError
            suit_name = CARD_SUIT_LIST[suit[0]]
            if value.upper() == card[0].upper() and suit_name == card[1]:
                print("Congratulations, you guessed both the value and the suit of the card!!!")
                right_answers += 1
            else:
                print("You didn't guess the value and/or the suit. The card was", *card)
                wrong_answers += 1
        except ValueError:
            handle_invalid_input()
    # выводим результаты игры
    response_to_the_player(right_answers, wrong_answers)


def game_selection():
    # Бесконечный цикл для выбора игры, пока пользователь не выберет или не выйдет из игры
    while True:
        # вывод на экран информации о выборе игры
        player_choice = input("""                       ******************** Hello player!!! ******************** 

    The game consists of five rounds where you have to guess the cards.

    Choose what game you want to play:

    1) Guess the color of the card (red(r) or black(b)):

    2) Guess the suit of the card (clubs(c), spades(s), diamonds(d), hearts(h)):

    3) Guess the card value (2, 3, 4, 5, 6, 7, 8, 9, 10, jack(j), queen(q), king(k), ace(a)):

    4) Guess the card value and suit (2, 3, 4, 5, 6, 7, 8, 9, 10, jack(j), queen(q), king(k), ace(a) 
       and through the space suit clubs(c), spades(s), diamonds(d), hearts(h)):

    to exit press key Q(q)

    -> """).lower()
        # проверка выбора игрока
        if player_choice.lower() == 'q':
            # выход из программы
            sys.exit()
        # вызов соответствующей игры в зависимости от выбора
        if player_choice in ['1', '2', '3', '4']:
            if player_choice == '1':
                guess_color()
            elif player_choice == '2':
                guess_suit()
            elif player_choice == '3':
                guess_card_value()
            elif player_choice == '4':
                guess_card_value_and_suit()
        # вывод сообщения о некорректном выборе игры
        else:
            print("You made a mistake in the choice, repeat the choice again!!!\n")
            continue


########################################################################################################################

# вызов функции для выбора игры
game_selection()

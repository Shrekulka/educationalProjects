Description of the game: "Guess the card"

The goal of the game is to guess the various characteristics of a randomly selected card from the deck. The player must
guess the color of the card (red or black), suit (spades, hearts, diamonds or clubs), card value (2, 3, 4, 5, 6, 7, 8, 
9, 10, J, Q, K, A) or both the value and suit of the card at the same time. In each round, a random card is generated 
and the player is asked to make your bet. In total, the player is given 6 attempts for each type of question. At the end
of the game, the player receives his result in the form the number of correct and incorrect answers.

Before playing, you need to import sys and the random module. The following constants are defined: suit list, list 
values, a list of suits in the form of a dictionary.

The generate_random_card() function generates a random card from the deck and returns a tuple with the card's value and 
suit.

The function response_to_the_player(right_answers, wrong_answers) takes the number of correct and incorrect answers and
displays a message about the results of the game.

The handle_invalid_input() function prints an input error message.

The guess_color() function is responsible for guessing the color of the map. In each round, a random card is generated 
and the player you are asked to guess the color (red or black). After each attempt, a message is displayed with the 
result. At the end of the game the function response_to_the_player() is called.

The guess_suit() function is responsible for guessing the suit of the card. In each round, a random card is generated 
and the player it is proposed to guess the suit (spades, hearts, diamonds or clubs). After each attempt, a message is 
displayed with the result. At the end of the game, the response_to_the_player() function is called.

The guess_card_value() function is responsible for guessing the value of the card. Each round a random card is generated
and the player is asked to guess the value (2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, A). After each attempt, it displays
result message. At the end of the game, the response_to_the_player() function is called.

The guess_card_value_and_suit() function is responsible for guessing the value and suit of the card. Each round generates
random card and the player is asked to guess the value and suit at the same time. A message is displayed after each attempt.
with the result. At the end of the game, the response_to_the_player() function is called.




Описание игры: "Угадай карту"

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
с результатом. В конце игры вызывается функция response_to_the_player().

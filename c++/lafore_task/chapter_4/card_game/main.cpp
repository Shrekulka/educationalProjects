#include <iostream>

using namespace std;

// Эта программа имитирует действия уличного игрока. Игрок показывает вам три карты, перемешивает их и раскладывает. Если
// вам удастся угадать, в какой последовательности разложены карты, то вы выиграли. Все происходит у вас на виду, но игрок
// мешает карты настолько быстро и умело, что вы путаетесь в расположении карт и, как правило, проигрываете свою ставку.
// Структура, хранящая информацию об игральной карте, выглядит так:
//
//struct card
//{
// int number;
// int suit;
//};
// Эта структура содержит два поля, number и suit, предназначенных для хранения соответственно достоинства карты и ее масти.
// Достоинство карты определяется числом от 2 до 14, где числа 11, 12, 13 и 14 означают соответственно валета, даму,
// короля и туза. Масть карты — число от 0 до 3, где 0 означает трефовую масть, 1 — бубновую, 2 — червовую, 3 — пиковую.
// Листинг программы CARDS выглядит следующим образом:

// Масти
const int clubs = 0;
const int diamonds = 1;
const int hearts = 2;
const int spades = 3;
// Достоинства карт
const int jack = 11;
const int queen = 12;
const int king = 13;
const int ace = 14;
struct card
{
	// достоинство
	int number;
	// масть
	int suit;
};

int main()
{
// три карты
	card temp, chosen, prize;
	int position = 0;
// инициализация карты 1
	card card1 = { 7, clubs };
	cout << "Карта 1: 7 треф\n";
	// инициализация карты 2
	card card2 = { jack, hearts };
	cout << "Карта 2: валет червей\n";
// инициализация карты 3
	card card3 = { ace, spades };
	cout << "Карта 3: туз пик\n ";
// запоминание карты 3
	prize = card3;
	cout << "Меняем местами карту 1 и карту 3...\n";
	temp = card3;
	card3 = card1;
	card1 = temp;
	cout << "Меняем местами карту 2 и карту 3...\n";
	temp = card3;
	card3 = card2;
	card2 = temp;
	cout << "Меняем местами карту 1 и карту 2...\n";
	temp = card2;
	card2 = card1;
	card1 = temp;
	cout << "На какой позиции (1, 2 или 3) теперь туз пик? ";
	cin >> position;
	switch (position)
	{
	case 1:
		chosen = card1;
		break;
	case 2:
		chosen = card2;
		break;
	case 3:
		chosen = card3;
		break;
	}
// сравнение карт
	if (chosen.number == prize.number && chosen.suit == prize.suit)
	{
		cout << "Правильно! Вы выиграли!\n";
	}
	else
	{
		cout << "Неверно. Вы проиграли.\n";
	}
	return 0;
}

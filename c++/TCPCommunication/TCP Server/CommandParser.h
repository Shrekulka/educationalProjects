//
// Created by Shrekulka on 27.06.2023.
//
#pragma once

#include "pch.h"

#ifndef TCP_SERVER_COMMANDPARSER_H
#define TCP_SERVER_COMMANDPARSER_H

/*
Класс CommandParser служит для обработки и управления командами в контексте сетевого соединения или приложения, которое
обрабатывает команды. Он предоставляет набор функций для работы с буфером команд, связанным с определенными сокетами.

Класс CommandParser, который имеет несколько функций для работы с буфером команд для указанного сокета. Он использует
std::map для хранения команд в буфере, где каждая команда связана с определенным сокетом.

1) getCommand(int socketid) - этот метод позволяет получить команду из буфера для указанного сокета. Возвращаемое
   значение является строкой (std::string).
2) addData(int socketid, const char* data, int length) - этот метод используется для добавления полученных данных в
   буфер для указанного сокета. Он принимает идентификатор сокета (socketid), указатель на массив символов (data) и
   длину данных (length).
3) clear(int socketid) - этот метод используется для очистки буфера для указанного сокета. Он принимает идентификатор
   сокета (socketid).
*/

class CommandParser
{
protected:
	// Создание защищенного члена класса - карты (map) с целочисленными ключами (int) и строковыми значениями (string).
	// Этот член будет использоваться для хранения команд в буфере.
	std::map<int, std::string> commandBuff = {};

public:
	// Функция будет использоваться для получения команды из буфера для указанного сокета.
	std::string getCommand(int socketid);

	// Функция будет использоваться для добавления полученных данных в буфер для указанного сокета, которая принимает
	// три аргумента:
	// 1. socketid - тип int, идентификатор сокета;
	// 2. data - тип const char*, указатель на массив символов (строку) для добавления в буфер;
	// 3. length - тип int, длина данных.
	void addData(int socketid, const char* data, int length);

	// Функция будет использоваться для очистки буфера для указанного сокета.
	void clear(int socketid);
};

#endif //TCP_SERVER_COMMANDPARSER_H
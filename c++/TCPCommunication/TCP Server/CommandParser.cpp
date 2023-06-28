//
// Created by Shrekulka on 27.06.2023.
//

#include "pch.h"

void CommandParser::addData(int socketid, const char* data, int length)
{
	// commandBuff[socketid] - обращение к элементу с ключом socketid в commandBuff (карте команд).
	// append(data, length) - добавление length символов из массива data в значение, связанное с ключом socketid в
	// commandBuff.
	commandBuff[socketid].append(data, length);
}

std::string CommandParser::getCommand(int socketid)
{
	// Получаем ссылку на значение, связанное с ключом `socketid` в `commandBuff`.
	std::string& buffer = commandBuff[socketid];

	// Ищем первое вхождение символа '\n' в `buffer`.
	std::size_t pos = buffer.find('\n');

	// Если символ '\n' не найден, возвращаем пустую строку.
	if (pos == std::string::npos)
	{
		return "";
	}

	// Получаем подстроку из `buffer`, начиная с индекса 0 и длиной `pos`.
	std::string fetchedCommand = buffer.substr(0, pos);

	// Обновляем `buffer`, отбрасывая полученную команду и символ '\n'.
	buffer = buffer.substr(pos + 1);

	// Возвращаем полученную команду.
	return fetchedCommand;
}

void CommandParser::clear(int socketid)
{
	// commandBuff[socketid].clear() - очищаем значение, связанное с ключом socketid в commandBuff, удаляя все символы
	// из строки.
	commandBuff[socketid].clear();
}

//
// Created by Shrekulka on 17.10.2023.
//
#pragma once

#include "common.h"

#ifndef TCP_CLIENT_FOR_DETERMINING_TIME_AND_DATE_CONFIG_H
#define TCP_CLIENT_FOR_DETERMINING_TIME_AND_DATE_CONFIG_H

#define BUFFER_SIZE 4096                         // Определяем максимальный размер буфера.
#define ADDRESS_SIZE sizeof(struct sockaddr_in)  // Определяем размер структуры sockaddr_in.

#define MAX_HOURS 24       // Определяем максимальное количество часов в сутках.
#define MONTHS_IN_YEAR 12  // Определяем количество месяцев в году.

#define IP_PROTOCOL 0       // Определяем протокол IP.
#define DAYTIME_PORT 13     // Определяем номер порта для дневного времени.
#define SA struct sockaddr  // Псевдоним для структуры sockaddr.

#define DATE_FORMAT "%d-%02d-%02d"    // Определяем формат даты.
#define TIME_FORMAT "%02d:%02d:%02d"  // Определяем формат времени.

#define TM_YEAR_OFFSET 1900  // Смещение для года в структуре tm.

enum Months  // Перечисление месяцев.
{
	JAN = 0, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC
};

struct TimeZoneInfo  // Структура с информацией о часовом поясе.
{
	int offset;                // Смещение времени.
	enum Months startMonth;    // Месяц начала часового пояса.
	int startDay;              // День начала часового пояса.
	enum Months endMonth;      // Месяц окончания часового пояса.
	int endDay;                // День окончания часового пояса.
	int daylightSavingOffset;  // Смещение летнего времени.
};

#endif //TCP_CLIENT_FOR_DETERMINING_TIME_AND_DATE_CONFIG_H

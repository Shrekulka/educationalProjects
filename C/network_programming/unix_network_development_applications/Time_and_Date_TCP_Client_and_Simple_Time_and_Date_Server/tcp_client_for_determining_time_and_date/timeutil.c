//
// Created by Shrekulka on 17.10.2023.
//
#include "timeutil.h"

// Функция для коррекции времени в соответствии с часовым поясом.
void correctTimezone(struct tm* localTime, const struct TimeZoneInfo* timezoneInfo)
{
	int month = localTime->tm_mon;  // Получение номера месяца из структуры tm.
	int day = localTime->tm_mday;   // Получение дня месяца из структуры tm.

	int offset = timezoneInfo->offset;                        // Получение смещения часового пояса.
	int daylightOffset = timezoneInfo->daylightSavingOffset;  // Получение смещения летнего времени.

	// Если месяц больше начального месяца или совпадает и день больше или равен начальному дню.
	// Или месяц равен конечному месяцу и день меньше конечного дня.
	if ((month > timezoneInfo->startMonth || (month == timezoneInfo->startMonth && day >= timezoneInfo->startDay)) ||
		(month == timezoneInfo->endMonth && day < timezoneInfo->endDay))
	{
		// Летнее время
		localTime->tm_hour += daylightOffset;  // Прибавляем смещение летнего времени.
	}
	else
	{
		// Зимнее время
		localTime->tm_hour += offset;  // Прибавляем смещение часового пояса.
	}

	// Если часы превышают 24.
	if (localTime->tm_hour >= MAX_HOURS)
	{
		localTime->tm_hour -= MAX_HOURS;  // Уменьшаем часы на 24.
		incrementDate(localTime);  // Инкрементируем дату.
	}
}

// Функция для инкрементирования даты.
void incrementDate(struct tm* date)
{
	// Массив смещений для месяцев.
	const int monthOffsets[] = {
			0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334
	};

	// Получение текущего смещения для месяца.
	const int currentMonthOffset = monthOffsets[date->tm_mon];

	// Получение смещения для следующего месяца.
	const int nextMonthOffset = monthOffsets[(date->tm_mon + 1) % MONTHS_IN_YEAR];

	// Если день больше или равен разнице смещений.
	if (date->tm_mday >= (nextMonthOffset - currentMonthOffset))
	{
		date->tm_mon = (date->tm_mon + 1) % MONTHS_IN_YEAR;  // Увеличиваем месяц на 1, переходя на следующий месяц.
		date->tm_mday = 1;                                   // Устанавливаем первое число месяца.
	}
	else
	{
		date->tm_mday++;  // Увеличиваем день на 1.
	}
}
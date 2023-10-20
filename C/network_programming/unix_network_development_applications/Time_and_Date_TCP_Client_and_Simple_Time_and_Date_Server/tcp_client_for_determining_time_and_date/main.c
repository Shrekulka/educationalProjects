#include "common.h"

int main(int argc, char** argv)  // Главная функция программы.
{
	int sockfd, n;                // Объявление переменных для сокета и количества байт.
	char recline[BUFFER_SIZE];    // Объявление буфера для чтения.

	struct sockaddr_in servaddr;  // Объявление структуры sockaddr_in для сервера.

	// Если количество аргументов командной строки не равно 2.
	if (argc != 2)
	{
		err_quit("usage: a.out <IPaddress", NULL);  // Выход из программы с сообщением об использовании.
	}

	// Создание сокета и проверка на ошибку.
	if ((sockfd = socket(AF_INET, SOCK_STREAM, IP_PROTOCOL)) < 0)
	{
		err_sys("socket error");  // Обработка ошибки сокета.
	}

	bzero(&servaddr, ADDRESS_SIZE);  // Обнуление структуры servaddr.

	servaddr.sin_family = AF_INET;  // Установка семейства адресов в AF_INET.

	servaddr.sin_port = htons(DAYTIME_PORT);  // Установка порта для сервера.

	// Преобразование IP-адреса из текстового в сетевой формат и проверка на ошибку.
	if (inet_pton(AF_INET, argv[1], &servaddr.sin_addr) <= 0)
	{
		err_quit("inet_pton error for %s", argv[1]);  // Обработка ошибки преобразования адреса.
	}

	// Установление соединения с сервером и проверка на ошибку.
	if (connect(sockfd, (SA*)&servaddr, ADDRESS_SIZE) < 0)
	{
		err_sys("connect error");  // Обработка ошибки соединения.
	}

	// Инициализация структуры TimeZoneInfo для Киевского времени.
	struct TimeZoneInfo kievTimeZone = {
			.offset = 2,
			.startMonth = MAR,
			.startDay = 31,
			.endMonth = OCT,
			.endDay = 31,
			.daylightSavingOffset = 3
	};

	// Чтение данных из сокета.
	while ((n = read(sockfd, recline, BUFFER_SIZE)) > 0)
	{
		recline[n] = 0;  // Завершение строки нулевым символом.

		// Вывод полученных данных на экран и проверка на ошибку.
		if (fputs(recline, stdout) == EOF)
		{
			err_sys("fputs error");  // Обработка ошибки вывода.
		}

		int year, month, day, hour, minute, second;  // Объявление переменных для компонентов времени.

		// Извлечение компонентов времени из строки.
		sscanf(recline, "%*d "DATE_FORMAT" "TIME_FORMAT, &year, &month, &day, &hour, &minute, &second);

		// Инициализация структуры tm для локального времени.
		struct tm localTime = {
				.tm_year = year - TM_YEAR_OFFSET,
				.tm_mon = month - 1,
				.tm_mday = day,
				.tm_hour = hour,
				.tm_min = minute,
				.tm_sec = second
		};

		// Коррекция времени в соответствии с часовым поясом Киева.
		correctTimezone(&localTime, &kievTimeZone);

		// Вывод времени на экран.
		printf("Year: %d\nMonth: %d\nDay: %d\nHour: %d\nMinute: %d\nSecond: %d\n",
				localTime.tm_year + TM_YEAR_OFFSET,
				localTime.tm_mon + 1,
				localTime.tm_mday,
				localTime.tm_hour,
				localTime.tm_min,
				localTime.tm_sec);
	}

	// Если чтение завершилось с ошибкой.
	if (n < 0)
	{
		err_sys("read error");  // Обработка ошибки чтения.
	}

	exit(0);  // Выход из программы без ошибок.
}




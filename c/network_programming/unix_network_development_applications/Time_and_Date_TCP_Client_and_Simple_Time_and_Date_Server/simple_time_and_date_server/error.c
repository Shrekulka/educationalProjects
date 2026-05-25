//
// Created by Shrekulka on 19.10.2023.
//

#include "error.h"

// Функция для выхода из программы с сообщением об ошибке.
void err_quit(const char* format, const char* arg)
{
	fprintf(stderr, format, arg);
	exit(1);
}

// Функция для обработки системных ошибок.
void err_sys(const char* msg)
{
	perror(msg);
	exit(1);
}
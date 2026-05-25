//
// Created by Shrekulka on 17.10.2023.
//
#pragma once

#include "common.h"

#ifndef TCP_CLIENT_FOR_DETERMINING_TIME_AND_DATE_ERROR_H
#define TCP_CLIENT_FOR_DETERMINING_TIME_AND_DATE_ERROR_H

// Прототип функции для выхода из программы с сообщением об ошибке.
void err_quit(const char* format, const char* arg);

// Прототип функции для обработки системных ошибок.
void err_sys(const char* msg);

#endif //TCP_CLIENT_FOR_DETERMINING_TIME_AND_DATE_ERROR_H

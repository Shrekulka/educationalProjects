//
// Created by Shrekulka on 19.10.2023.
//

#pragma once

#include "common.h"

#ifndef SIMPLE_TIME_AND_DATE_SERVER_ERROR_H
#define SIMPLE_TIME_AND_DATE_SERVER_ERROR_H

// Прототип функции для выхода из программы с сообщением об ошибке.
void err_quit(const char* format, const char* arg);

// Прототип функции для обработки системных ошибок.
void err_sys(const char* msg);


#endif //SIMPLE_TIME_AND_DATE_SERVER_ERROR_H

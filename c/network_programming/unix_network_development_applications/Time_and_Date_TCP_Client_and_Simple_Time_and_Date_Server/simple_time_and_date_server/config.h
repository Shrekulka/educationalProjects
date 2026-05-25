//
// Created by Shrekulka on 19.10.2023.
//
#pragma once

#include "common.h"

#ifndef SIMPLE_TIME_AND_DATE_SERVER_CONFIG_H
#define SIMPLE_TIME_AND_DATE_SERVER_CONFIG_H

// Mаксимальный размер буфера MAXLINE для хранения данных.
#define MAXLINE 4096

// Максимальная очередь ожидающих соединений.
#define LISTENQ 1024

// Порт для daytime сервера
#define PORT 13

#endif //SIMPLE_TIME_AND_DATE_SERVER_CONFIG_H

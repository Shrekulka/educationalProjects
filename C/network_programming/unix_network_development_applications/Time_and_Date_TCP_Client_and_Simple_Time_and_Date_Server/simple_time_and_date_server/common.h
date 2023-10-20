//
// Created by Shrekulka on 19.10.2023.
//

#pragma once

#ifndef SIMPLE_TIME_AND_DATE_SERVER_COMMON_H
#define SIMPLE_TIME_AND_DATE_SERVER_COMMON_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netinet/tcp.h>
#include <sys/socket.h>
#include <time.h>
#include "config.h"
#include "error.h"
#include "utils.h"

typedef struct sockaddr SA;
/* struct sockaddr - это структура данных, которая используется для хранения информации об адресе сокета в сетевом
 * программировании.
Она определена в заголовочных файлах сетевого API (например, sys/socket.h) и имеет следующую типичную структуру:

struct sockaddr
{
  sa_family_t sin_family; // семейство адресов (AF_INET, AF_INET6 и т.д.)
  char        sa_data[14]; // 14 байт для адреса и номера порта
};

Основные поля:
sin_family - семейство адресов, например AF_INET для IPv4.
sa_data - буфер фиксированного размера для хранения адреса и порта. Размер зависит от семейства адресов.

Для IPv4 адреса используется производная структура sockaddr_in:

struct sockaddr_in
{
  short int          sin_family; // AF_INET
  unsigned short int sin_port;   // порт
  struct in_addr     sin_addr;   // IP-адрес
};

А для IPv6 используется sockaddr_in6.
Таким образом, структура sockaddr предоставляет общий способ хранения сетевых адресов и параметров сокета, независимо от
 их типа и семейства. Она широко используется в сетевых вызовах, таких как bind(), connect(), sendto() и других.*/

#endif //SIMPLE_TIME_AND_DATE_SERVER_COMMON_H

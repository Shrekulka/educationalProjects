//
// Created by Shrekulka on 26.10.2023.
//
#pragma once

#include "common.h"

#ifndef FUNCTION_FOR_CONVERTING_IP_ADDRESSES_SOCKET_ADDRESS_UTILITY_H
#define FUNCTION_FOR_CONVERTING_IP_ADDRESSES_SOCKET_ADDRESS_UTILITY_H

char *sock_ntop(const struct sockaddr* sa, socklen_t salen);

// Функция sock bind wild связывает универсальный адрес идинамически на- значаемый порт ссокетом.
int sock_bind_wild(int sockfd, int family);

// Функция sock mcp_ addr сравнивает адресные части двух структур адреса сокета.
int sock_cmp_addr(const struct sockaddr* sockaddr1, const struct sockaddr* sockaddr2, socklen_t addrlen);

// Функция sock cmp_port сравнивает номера портов.
int sock_cmp_port(const struct sockaddr* sockaddr1, const struct sockaddr* sockaddr2, socklen_t addrlen);

// Функция sock _get _port возвращает только номер порта.
int sock_get_port(const struct sockaddr* sockaddr, socklen_t addrlen);

// Функция sock ntop_host преобразует к формату представления только ту часть структуры адреса сокета, которая относится
// к узлу (все, кроме порта, то есть IP-адрес узла).
char* sock_ntop_host(const struct sockaddr* sockaddr, socklen_t addrlen);

// Функция sock_set_addr присваивает адресной части структуры значение, указанное аргументом ptr
void sock_set_addr(struct sockaddr* sa, socklen_t salen, const void* addr);

// Функция sock set port задает вструктуре адреса сокета только номер порта.
void sock_set_port(struct sockaddr* sa, socklen_t salen, int port);

// Функция sock_se_t_wild задает адресную часть структуры через символы подстановки.
void sock_set_wild(struct sockaddr* sockaddr, socklen_t addrlen);

#endif //FUNCTION_FOR_CONVERTING_IP_ADDRESSES_SOCKET_ADDRESS_UTILITY_H

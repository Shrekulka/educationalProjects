//
// Created by Shrekulka on 26.10.2023.
//
#pragma once

#include "common.h"

#ifndef FUNCTION_FOR_CONVERTING_IP_ADDRESSES_CONFIG_H
#define FUNCTION_FOR_CONVERTING_IP_ADDRESSES_CONFIG_H

/* Following shortens all the typecasts of pointer arguments: */
#define    SA    struct sockaddr
const int INFO_SIZE = 256;  // Константа для размера буфера информации.
const int VENDOR_ID_SIZE = 13;  // Константа для размера буфера идентификатора прои
struct sockaddr_un
{
	sa_family_t sun_family;               /* AF_UNIX */
	char sun_path[108];            /* имя пути */
};
#endif //FUNCTION_FOR_CONVERTING_IP_ADDRESSES_CONFIG_H

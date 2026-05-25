//
// Created by Shrekulka on 25.10.2023.
//

#pragma once

#include "common.h"

#ifndef BYTE_ORDER_DETECTION_FUNCTIONS_H
#define BYTE_ORDER_DETECTION_FUNCTIONS_H

// Функция для получения информации о операционной системе и процессоре.
const char* get_os_and_cpu_info();

// Функция для получения идентификатора производителя процессора.
const char* get_cpu_vendor_id();

#endif //BYTE_ORDER_DETECTION_FUNCTIONS_H

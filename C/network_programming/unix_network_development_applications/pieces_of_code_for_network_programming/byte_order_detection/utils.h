//
// Created by Shrekulka on 25.10.2023.
//
#pragma once

#include "common.h"

#ifndef BYTE_ORDER_DETECTION_UTILS_H
#define BYTE_ORDER_DETECTION_UTILS_H

// Макрос для проверки ошибок. Макросы обычно используются для более удобного обнаружения и обработки ошибок.
#define CHECK_ERR(expr, msg) { \
   int result = (expr); \
   if (result != 0) { \
      fprintf(stderr, "Error in %s: %s (Error Code: %d)\n", #expr, msg, result); \
      exit(EXIT_FAILURE); \
   } \
}

#endif //BYTE_ORDER_DETECTION_UTILS_H

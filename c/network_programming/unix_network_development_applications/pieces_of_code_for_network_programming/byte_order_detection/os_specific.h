//
// Created by Shrekulka on 25.10.2023.
//
#pragma once

#include "common.h"

#ifndef BYTE_ORDER_DETECTION_OS_SPECIFIC_H
#define BYTE_ORDER_DETECTION_OS_SPECIFIC_H


// Условная компиляция: этот блок будет включен только при компиляции кода на macOS.
#ifdef __APPLE__

#include <sys/sysctl.h>

#endif

// Условная компиляция: этот блок будет включен только при компиляции кода на системах Linux.
#ifdef __linux__
#include <sys/utsname.h>
#include <cpuid.h>
#endif

// Условная компиляция: этот блок будет включен только при компиляции кода на платформе Windows.
#ifdef _WIN32
#include <windows.h>
#endif


#endif //BYTE_ORDER_DETECTION_OS_SPECIFIC_H

//
// Created by Shrekulka on 17.10.2023.
//
#pragma once

#include "common.h"

#ifndef TCP_CLIENT_FOR_DETERMINING_TIME_AND_DATE_TIMEUTIL_H
#define TCP_CLIENT_FOR_DETERMINING_TIME_AND_DATE_TIMEUTIL_H

// Прототип функции для коррекции времени в соответствии с часовым поясом.
void correctTimezone(struct tm* localTime, const struct TimeZoneInfo* timezoneInfo);

// Прототип функции для инкрементирования даты.
void incrementDate(struct tm* date);

#endif //TCP_CLIENT_FOR_DETERMINING_TIME_AND_DATE_TIMEUTIL_H

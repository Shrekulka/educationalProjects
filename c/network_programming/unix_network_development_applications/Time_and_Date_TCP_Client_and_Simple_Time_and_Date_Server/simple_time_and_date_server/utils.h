//
// Created by Shrekulka on 19.10.2023.
//

#pragma once

#include "common.h"

#ifndef SIMPLE_TIME_AND_DATE_SERVER_UTILS_H
#define SIMPLE_TIME_AND_DATE_SERVER_UTILS_H

int Socket(int family, int type, int protocol);

int Bind(int sockfd, const struct sockaddr* myaddr, socklen_t addrlen);

int Listen(int sockfd, int backlog);

int Accept(int sockfd, struct sockaddr* cliaddr, socklen_t* addrlen);

int Close(int fd);

ssize_t Write(int fd, const void* buff, size_t nbytes);

#endif //SIMPLE_TIME_AND_DATE_SERVER_UTILS_H

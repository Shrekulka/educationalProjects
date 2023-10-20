//
// Created by Shrekulka on 19.10.2023.
//

#include "utils.h"

int Socket(int family, int type, int protocol)
{
	int n;
	if ((n = socket(family, type, protocol)) < 0)
	{
		perror("socket error");
		exit(1);
	}
	return n;
}

int Bind(int sockfd, const SA* myaddr, socklen_t addrlen)
{
	if (bind(sockfd, myaddr, addrlen) < 0)
	{
		perror("bind error");
		exit(1);
	}
	return 0;
}

int Listen(int sockfd, int backlog)
{
	if (listen(sockfd, backlog) < 0)
	{
		perror("listen error");
		exit(1);
	}
	return 0;
}

int Accept(int sockfd, SA* cliaddr, socklen_t* addrlen)
{
	int connfd;
	if ((connfd = accept(sockfd, cliaddr, addrlen)) < 0)
	{
		perror("accept error");
		exit(1);
	}
	return connfd;
}

int Close(int fd)
{
	if (close(fd) < 0)
	{
		perror("close error");
		exit(1);
	}
	return 0;
}

ssize_t Write(int fd, const void* buff, size_t nbytes)
{
	ssize_t n;
	if ((n = write(fd, buff, nbytes)) < 0)
	{
		perror("write error");
		exit(1);
	}
	return n;
}

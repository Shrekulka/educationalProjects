#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netdb.h>
#include <arpa/inet.h>

// Функция для получения и вывода IP-адресов заданного хоста.
void printIPAddresses(const char* host)
{
	struct addrinfo hints, * result, * rp; // Объявляем структуры для работы с информацией о сетевых адресах и итерации по ним.

	int status; // Переменная для хранения статуса выполнения функций.

	char ipstr[INET6_ADDRSTRLEN]; // Буфер для хранения текстового представления IP-адреса.

	// Инициализация структуры hints для указания параметров поиска сетевых адресов.
	memset(&hints, 0, sizeof(struct addrinfo));
	hints.ai_family = AF_UNSPEC;    // Указываем, что хотим получить адреса IPv4 и IPv6.
	hints.ai_socktype = SOCK_STREAM; // Указываем, что хотим сокс с потоковым TCP-соединением.

	// Вызываем функцию getaddrinfo() для получения информации о сетевых адресах хоста.
	status = getaddrinfo(host, NULL, &hints, &result);
	if (status != 0)
	{
		fprintf(stderr, "getaddrinfo error: %s\n",
				gai_strerror(status)); // Выводим ошибку, если getaddrinfo завершилась с ошибкой.
		exit(1); // Завершаем программу с кодом ошибки.
	}

	printf("IP addresses for %s:\n\n", host); // Выводим заголовок с именем хоста.

	// Перебираем список адресов, полученных от getaddrinfo().
	for (rp = result; rp != NULL; rp = rp->ai_next)
	{
		void* addr; // Указатель на бинарный адрес (IPv4 или IPv6).
		char* ipver; // Указатель на строку с версией IP (IPv4 или IPv6).

		// Если семейство адресов IPv4.
		if (rp->ai_family == AF_INET)
		{
			struct sockaddr_in* ipv4 = (struct sockaddr_in*)rp->ai_addr;
			addr = &(ipv4->sin_addr); // Получаем указатель на IPv4-адрес.
			ipver = "IPv4"; // Устанавливаем метку для IPv4.
		}
		// Иначе (семейство адресов IPv6).
		else
		{
			struct sockaddr_in6* ipv6 = (struct sockaddr_in6*)rp->ai_addr;
			addr = &(ipv6->sin6_addr); // Получаем указатель на IPv6-адрес.
			ipver = "IPv6"; // Устанавливаем метку для IPv6.
		}

		// Преобразование бинарного адреса в текстовое представление.
		inet_ntop(rp->ai_family, addr, ipstr, sizeof(ipstr));
		printf(" %s: %s\n", ipver, ipstr); // Выводим IP-адрес и его версию (IPv4 или IPv6).
	}

	freeaddrinfo(result); // Освобождаем память, выделенную getaddrinfo().

}

int main(int argc, char* argv[])
{
	if (argc != 2)
	{
		fprintf(stderr, "usage: %s hostname\n", argv[0]); // Выводим сообщение об использовании, если не указан хост.
		return 1;
	}

	const char* host = argv[1]; // Получаем имя хоста из аргументов командной строки.

	printIPAddresses(host); // Вызываем функцию для вывода IP-адресов заданного хоста.

	return 0; // Возвращаем ноль, чтобы указать успешное завершение программы.
}

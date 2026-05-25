#include <stdio.h>
#include <arpa/inet.h>


#define IPV4_ADDR_SIZE 4        // Определяем константу для размера IPv4 адреса в байтах
#define IPV6_ADDR_SIZE 16       // Определяем константу для размера IPv6 адреса в байтах

int main()
{
	struct in_addr ipv4Addr;   // Создаем структуру для хранения IPv4 адреса
	struct in6_addr ipv6Addr;  // Создаем структуру для хранения IPv6 адреса

	// Задаем IPv4 и IPv6 адреса (в хост-порядке)

	// Преобразуем текстовый IPv4 адрес в бинарный формат
	inet_pton(AF_INET, "192.168.1.1", &ipv4Addr);

	// Преобразуем текстовый IPv6 адрес в бинарный формат
	inet_pton(AF_INET6, "2001:0db8:85a3:0000:0000:8a2e:0370:7334", &ipv6Addr);

	// Преобразуем IPv4 адрес в сетевой порядок байт с использованием функции htonl
	uint32_t networkIPv4 = htonl(ipv4Addr.s_addr);

	// Создаем структуру для хранения IPv6 адреса в сетевом порядке
	struct in6_addr networkIPv6;

	// Преобразуем каждый блок IPv6 адреса в сетевой порядок байт
	for (int i = 0; i < IPV6_ADDR_SIZE; i += IPV4_ADDR_SIZE)
	{
		*(uint32_t*)(networkIPv6.s6_addr + i) = htonl(*(uint32_t*)(ipv6Addr.s6_addr + i));
	}

	// Выводим исходные и данные в сетевом порядке байт
	printf("\nИсходный IPv4 адрес (порядок хоста): %s\n", inet_ntoa(ipv4Addr));
	printf("IPv4 адрес в сетевом порядке байт: %s\n\n", inet_ntoa(*(struct in_addr*)&networkIPv4));

	// Создаем буфер для хранения текстового IPv6 адреса
	char ipv6Str[INET6_ADDRSTRLEN];

	// Преобразуем IPv6 адрес в текстовый формат
	inet_ntop(AF_INET6, &ipv6Addr, ipv6Str, INET6_ADDRSTRLEN);

	// Выводим исходный IPv6 адрес
	printf("Исходный IPv6 адрес (порядок хоста): %s\n", ipv6Str);

	// Преобразуем IPv6 адрес в сетевом порядке в текстовый формат
	inet_ntop(AF_INET6, &networkIPv6, ipv6Str, INET6_ADDRSTRLEN);

	// Выводим IPv6 адрес в сетевом порядке
	printf("IPv6 адрес в сетевом порядке байт: %s\n\n", ipv6Str);

	// Преобразуем IPv4 адрес из сетевого порядка в порядок хоста
	uint32_t hostIPv4FromNetwork = ntohl(networkIPv4);

	// Создаем структуру для хранения IPv6 адреса в порядке хоста
	struct in6_addr hostIPv6FromNetwork;

	// Преобразуем каждый блок IPv6 адреса из сетевого порядка в порядок хоста
	for (int i = 0; i < IPV6_ADDR_SIZE; i += IPV4_ADDR_SIZE)
	{
		*(uint32_t*)(hostIPv6FromNetwork.s6_addr + i) = ntohl(*(uint32_t*)(networkIPv6.s6_addr + i));
	}

	// Выводим IPv4 адрес в порядке хоста
	printf("IPv4 адрес, преобразованный обратно в порядок хоста: %s\n",
			inet_ntoa(*(struct in_addr*)&hostIPv4FromNetwork));

	// Преобразуем IPv6 адрес из порядка хоста в текстовый формат
	inet_ntop(AF_INET6, &hostIPv6FromNetwork, ipv6Str, INET6_ADDRSTRLEN);

	// Выводим IPv6 адрес в порядке хоста
	printf("IPv6 адрес, преобразованный обратно в порядок байтов хоста: %s\n", ipv6Str);

	return 0;
}

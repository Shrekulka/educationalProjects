#include "common.h"

int main() {
	// Создаем структуру адреса IPv4
	struct sockaddr_in ipv4_addr;
	memset(&ipv4_addr, 0, sizeof(ipv4_addr));
	ipv4_addr.sin_family = AF_INET;
	ipv4_addr.sin_port = htons(80); // Пример порта 80
	inet_pton(AF_INET, "192.168.1.1", &ipv4_addr.sin_addr); // Пример IPv4-адреса

	// Продемонстрируем функцию sock_ntop для IPv4
	printf("sock_ntop for IPv4: %s\n", sock_ntop((struct sockaddr*)&ipv4_addr, sizeof(ipv4_addr)));

	// Создаем структуру адреса IPv6
	struct sockaddr_in6 ipv6_addr;
	memset(&ipv6_addr, 0, sizeof(ipv6_addr));
	ipv6_addr.sin6_family = AF_INET6;
	ipv6_addr.sin6_port = htons(443); // Пример порта 443
	inet_pton(AF_INET6, "2001:0db8:85a3:0000:0000:8a2e:0370:7334", &ipv6_addr.sin6_addr); // Пример IPv6-адреса

	// Продемонстрируем функцию sock_ntop для IPv6
	printf("sock_ntop for IPv6: %s\n", sock_ntop((struct sockaddr*)&ipv6_addr, sizeof(ipv6_addr)));

	// Продемонстрируем функцию sock_bind_wild для IPv4
	int ipv4_socket = socket(AF_INET, SOCK_STREAM, 0);
	int ipv4_port = sock_bind_wild(ipv4_socket, AF_INET);
	printf("Bound IPv4 port: %d\n", ipv4_port);

	// Продемонстрируем функцию sock_cmp_addr для сравнения IPv4-адресов
	struct sockaddr_in ipv4_addr1, ipv4_addr2;
	inet_pton(AF_INET, "192.168.1.1", &ipv4_addr1.sin_addr);
	inet_pton(AF_INET, "192.168.1.2", &ipv4_addr2.sin_addr);
	int addr_cmp_result = sock_cmp_addr((struct sockaddr*)&ipv4_addr1, (struct sockaddr*)&ipv4_addr2, sizeof(ipv4_addr1));
	printf("Comparison result for IPv4 addresses: %d\n", addr_cmp_result);

	// Продемонстрируем функцию sock_cmp_port для сравнения портов
	struct sockaddr_in ipv4_addr3, ipv4_addr4;
	ipv4_addr3.sin_port = htons(80);
	ipv4_addr4.sin_port = htons(8080);
	int port_cmp_result = sock_cmp_port((struct sockaddr*)&ipv4_addr3, (struct sockaddr*)&ipv4_addr4, sizeof(ipv4_addr3));
	printf("Comparison result for IPv4 ports: %d\n", port_cmp_result);

	// Продемонстрируем функцию sock_get_port для получения порта
	int retrieved_port = sock_get_port((struct sockaddr*)&ipv4_addr3, sizeof(ipv4_addr3));
	printf("Retrieved IPv4 port: %d\n", ntohs(retrieved_port));

	// Продемонстрируем функцию sock_ntop_host для IPv4
	printf("sock_ntop_host for IPv4: %s\n", sock_ntop_host((struct sockaddr*)&ipv4_addr, sizeof(ipv4_addr)));

	// Создаем структуру адреса IPv6
	struct sockaddr_in6 ipv6_addr;
	memset(&ipv6_addr, 0, sizeof(ipv6_addr));
	ipv6_addr.sin6_family = AF_INET6;
	ipv6_addr.sin6_port = htons(443); // Пример порта 443
	inet_pton(AF_INET6, "2001:0db8:85a3:0000:0000:8a2e:0370:7334", &ipv6_addr.sin6_addr); // Пример IPv6-адреса

	// Продемонстрируем функцию sock_ntop для IPv6
	printf("sock_ntop for IPv6: %s\n", sock_ntop((struct sockaddr*)&ipv6_addr, sizeof(ipv6_addr)));

	// Продемонстрируем функцию sock_bind_wild для IPv6
	int ipv6_socket = socket(AF_INET6, SOCK_STREAM, 0);
	int ipv6_port = sock_bind_wild(ipv6_socket, AF_INET6);
	printf("Bound IPv6 port: %d\n", ipv6_port);

	// Продемонстрируем функцию sock_cmp_addr для сравнения IPv6-адресов
	struct sockaddr_in6 ipv6_addr1, ipv6_addr2;
	inet_pton(AF_INET6, "2001:0db8:85a3:0000:0000:8a2e:0370:7334", &ipv6_addr1.sin6_addr);
	inet_pton(AF_INET6, "2001:0db8:85a3:0000:0000:8a2e:0370:7335", &ipv6_addr2.sin6_addr);
	int addr_cmp_result6 = sock_cmp_addr((struct sockaddr*)&ipv6_addr1, (struct sockaddr*)&ipv6_addr2, sizeof(ipv6_addr1));
	printf("Comparison result for IPv6 addresses: %d\n", addr_cmp_result6);

	// Продемонстрируем функцию sock_cmp_port для сравнения портов
	struct sockaddr_in6 ipv6_addr3, ipv6_addr4;
	ipv6_addr3.sin6_port = htons(443);
	ipv6_addr4.sin6_port = htons(80);
	int port_cmp_result6 = sock_cmp_port((struct sockaddr*)&ipv6_addr3, (struct sockaddr*)&ipv6_addr4, sizeof(ipv6_addr3));
	printf("Comparison result for IPv6 ports: %d\n", port_cmp_result6);

	// Продемонстрируем функцию sock_get_port для получения порта
	int retrieved_port6 = sock_get_port((struct sockaddr*)&ipv6_addr3, sizeof(ipv6_addr3));
	printf("Retrieved IPv6 port: %d\n", ntohs(retrieved_port6));

	// Продемонстрируем функцию sock_ntop_host для IPv6
	printf("sock_ntop_host for IPv6: %s\n", sock_ntop_host((struct sockaddr*)&ipv6_addr, sizeof(ipv6_addr)));

	return 0;
}

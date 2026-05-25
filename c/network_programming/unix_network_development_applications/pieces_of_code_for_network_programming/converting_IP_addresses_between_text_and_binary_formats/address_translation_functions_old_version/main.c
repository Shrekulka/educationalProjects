#include <arpa/inet.h>
#include <stdio.h>

// Именованные константы для IP-адреса
#define IP_ADDRESS_STR "192.168.1.1"
#define IP_ADDRESS_NUM 0xC0A80101

int main()
{
	// Объявляем переменные addr, которая будет использоваться для хранения IP-адреса в бинарном формате (структура
	// in_addr), и ip_str, которая будет использоваться для хранения IP-адреса в виде строки.
	struct in_addr addr;
	char* ip_str;

	// 1) inet_aton - преобразование строки в бинарный вид

	// С помощью функции inet_aton преобразуем строку IP_ADDRESS_STR в бинарное представление и сохраняем ее в addr.
	// Проверяем, успешно ли прошло преобразование. Если преобразование прошло успешно, выводим бинарное представление
	// IP-адреса в шестнадцатеричном формате.
	if (inet_aton(IP_ADDRESS_STR, &addr))
	{
		// Преобразуем в сетевой порядок для вывода
		uint32_t net_addr = htonl(addr.s_addr);
		printf("IP address in binary format: 0x%08X\n", net_addr);
	}
	else
	{
		printf("Error converting string to binary format.\n");
	}

	// 2) inet_addr - преобразование строки в 32-битное число

	// Преобразуем строковое представление IP-адреса (IP_ADDRESS_NUM) в 32-битное число, сохраняем его в переменной
	// ip_num. Проверяем, было ли преобразование успешным, и если да, выводим число в шестнадцатеричном формате.
	in_addr_t ip_num = IP_ADDRESS_NUM;

	// Преобразуем в сетевой порядок байтов
	ip_num = htonl(ip_num);

	if (ip_num != INADDR_NONE)
	{
		printf("IP address as a 32-bit number: 0x%08X\n", ip_num);
	}
	else
	{
		printf("Error converting string to number.\n");
	}

	// 3) inet_ntoa - преобразование бинарного представления обратно в строку

	// Преобразуем 32-битное число ip_num обратно в строковое представление с использованием функции inet_ntoa. Затем
	// выводим строковое представление IP-адреса.
	addr.s_addr = ip_num;
	ip_str = inet_ntoa(addr);
	printf("IP address in string format: %s\n", ip_str);

	return 0;
}

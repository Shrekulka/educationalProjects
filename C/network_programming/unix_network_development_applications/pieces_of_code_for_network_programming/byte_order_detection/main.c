#include "common.h"


int main(int argc, char** argv)
{
	// Определение объединения (union) un, которое используется для интерпретации двухбайтового числа (short) как
	// массива из двух байтов (char).
	union
	{
		short s;                // Двухбайтовое число
		char c[sizeof(short)];  // Массив из двух байтов
	} un;

	// Присвоение значению s в объединении un шестнадцатеричного значения 0x0102.
	un.s = 0x0102;

	// Вызов функции get_os_and_cpu_info для получения информации о системе и процессоре, результат сохраняется в
	// переменной CPU_VENDOR_OS.
	const char* CPU_VENDOR_OS = get_os_and_cpu_info();

	printf("CPU_VENDOR_OS: %s\n", CPU_VENDOR_OS);

	// Проверка размера short, чтобы определить порядок байтов (endianness) на данной платформе.
	if (sizeof(short) == 2)
	{
		// Если размер short равен 2 байта, выполняется проверка порядка байтов.

		// Порядок байтов, при котором старший байт хранится первым.
		if (un.c[0] == 1 && un.c[1] == 2) printf("big-endian\n");

			// Порядок байтов, при котором младший байт хранится первым.
		else if (un.c[0] == 2 && un.c[1] == 1) printf("little-endian\n");

			// Неизвестный порядок байтов.
		else printf("unknown\n");
	}
		// Если размер short не равен 2 байта, выводится сообщение о размере short.
	else printf("sizeof(short) = %lu\n", sizeof(short));

	// Проверка, не является ли указатель CPU_VENDOR_OS нулевым, и если нет, освобождение памяти, выделенной для
	// CPU_VENDOR_OS.
	if (CPU_VENDOR_OS != NULL) free((char*)CPU_VENDOR_OS);

	return 0;
}


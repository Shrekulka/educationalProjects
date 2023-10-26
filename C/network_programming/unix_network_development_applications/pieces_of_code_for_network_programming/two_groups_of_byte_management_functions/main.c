#include <stdio.h>
#include <strings.h>
#include <string.h>

// Определение макроса, который выбирает первую или вторую группу функций
#define USE_FIRST_GROUP 0

/*
Первая группа функций, названия которых начинаются с 'b' (от слова "byte" - "байт"), происходит из реализации 4.2BSD
и по-прежнему поддерживается практически всеми системами, поддерживающими функции соксетов.


1. Функция bzero устанавливает указанное количество байтов в области памяти в нулевые значения. Эту функцию часто
   используют для инициализации структуры адреса соксета нулевыми значениями.
* void bzero(void *dest, size_t nbytes);

2. Функция bcopy копирует указанное количество байтов из источника в место назначения.
* void bcopy(const void *src, void *dest, size_t nbytes);

3. Функция bcmp сравнивает две произвольные последовательности байтов и возвращает ноль, если две байтовые строки
   идентичны, или ненулевое значение в противном случае.
* int bcmp(const void *ptr1, const void *ptr2, size_t nbytes);


Вторая группа функций, названия которых начинаются с 'mem' (от слова "memory" - "память"), происходит из стандарта
ANSI C и доступна в любой системе, поддерживающей библиотеку ANSI C.

1. Функция memset назначает значение указанному числу байтов.
* void *memset(void *dest, int c, size_t len);

2. Функция memcpy аналогична bcopy, но имеет другой порядок аргументов.
* void *memcpy(void *dest, const void *src, size_t nbytes);

3. Функция memcmp сравнивает две произвольные последовательности байтов и возвращает ноль, если они идентичны. В случае
   различия, знак возвращаемого значения определяется разницей между первыми отличающимися байтами, на которые указывают
   ptr1 и ptr2. Предполагается, что сравниваемые байты принадлежат к типу unsigned char.
* int memcmp(const void *ptr1, const void *ptr2, size_t nbytes);
*/

int main()
{
	char buffer1[10] = "Hello";  // Создаем массив buffer1 и инициализируем его строкой "Hello"
	char buffer2[10];            // Создаем второй массив buffer2

// Используем макрос для выбора группы функций
#if USE_FIRST_GROUP

	bzero(buffer2, sizeof(buffer2));  // Используем функцию bzero для установки значений в buffer2

	bcopy(buffer1, buffer2, sizeof(buffer1));  // Используем функцию bcopy для копирования данных из buffer1 в buffer2

	// Если буферы идентичны, выводим сообщение
	if (bcmp(buffer1, buffer2, sizeof(buffer1)) == 0) printf("Buffers are identical (first group)\n");

	// В противном случае выводим другое сообщение
	else printf("Buffers are different (first group)\n");

#else
	memset(buffer2, 0, sizeof(buffer2));  // Используем функцию memset для установки значений в buffer2

    memcpy(buffer2, buffer1, sizeof(buffer1));  // Используем функцию memcpy для копирования данных из buffer1 в buffer2

	// Если буферы идентичны, выводим сообщение
    if (memcmp(buffer1, buffer2, sizeof(buffer1)) == 0) printf("Buffers are identical (second group)\n");

	// В противном случае выводим другое сообщение
    else printf("Buffers are different (second group)\n");

#endif

	return 0;
}

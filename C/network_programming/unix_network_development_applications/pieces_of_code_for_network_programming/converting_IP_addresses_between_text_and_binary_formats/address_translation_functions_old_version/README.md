**Title: Demonstrating IP Address Handling Using <arpa/inet.h> Functions**

This code showcases the use of functions from the <arpa/inet.h> library for working with IPv4 addresses. It also provides
information about some properties and nuances of these functions.

1. **'inet_aton' and the Undocumented Feature:**
   The 'inet_aton' function is used to convert an IP address string into its binary representation (in_addr structure).
   Undocumented Feature: If 'addrptr' is a null pointer, the function still performs address validity checks in the input
   string but does not save the conversion result.
2. **'inet_addr' and Its Limitations:**
   The 'inet_addr' function performs the same conversion, returning a 32-bit binary number in network byte order. 
   Problem: In case of an error, the function returns the INADDR_NONE constant, which is represented as a 32-bit binary 
   number with all bits set to one. This can be confusing, as this value indicates an error, and the dotted-decimal 
   representation "255.255.255.255" cannot be processed by this function.
3. **Note on 'inet_addr':**
   Issue with 'inet_addr': There is an inconsistency in that some guides may claim that 'inet_addr' returns -1 in case 
   of an error instead of 'INADDR_NONE'. This can cause problems when comparing the function's return value (an unsigned
   value) with a negative constant.
4. **Recommendation for Usage:**
   Today, 'inet_addr' is considered a deprecated function, and it is recommended to use 'inet_aton'. It's even better to
   use newer functions that work with both IPv4 and IPv6.
5. **'inet_ntoa' and Its Features:**
   The 'inet_ntoa' function converts a 32-bit binary IPv4 address, stored in network byte order, into a dotted-decimal 
   string. It's essential to note that the string pointed to by the function's return pointer is in static memory, 
   meaning the function is not reentrant and does not support multiple invocations.

**Usage of the Code:**

This code demonstrates how to work with IP address conversion functions and highlights some of their features. It can be
used as an example and for understanding how to use 'inet_aton', 'inet_addr', and 'inet_ntoa' functions in network 
programming.

**Sample program output:**
``` 
IP address in binary format: 0xC0A80101
IP address as a 32-bit number: 0x0101A8C0
IP address in string format: 192.168.1.1

Process finished with exit code 0
```




Этот код демонстрирует использование функций из библиотеки <arpa/inet.h> для работы с IP-адресами в формате IPv4. Он 
также содержит информацию о некоторых свойствах и нюансах этих функций.

1. **'inet_aton' и недокументированное свойство:**
   Функция 'inet_aton' используется для преобразования строки IP-адреса в его бинарное представление (структура in_addr).
   Недокументированное свойство: Если 'addrptr' - пустой указатель (null pointer), функция все равно выполняет проверку
   допустимости адреса во входной строке, но не сохраняет результат преобразования.
2. **'inet_addr' и его ограничения:**
   Функция 'inet_addr' выполняет то же преобразование, возвращая в качестве значения 32-разрядное двоичное число в 
   сетевом порядке байтов.
   Проблема: В случае ошибки, функция возвращает константу INADDR_NONE, которая представлена как двоичное число, 
   состоящее из 32 бит, установленных в единицу. Это может вызвать путаницу, поскольку это значение означает ошибку, и 
   точечно-десятичная запись "255.255.255.255" не может быть обработана этой функцией.
3. **Примечание о 'inet_addr':**
   Проблема с 'inet_addr': Существует несоответствие в том, что некоторые руководства могут утверждать, что в случае 
   ошибки 'inet_addr' возвращает значение -1 вместо 'INADDR_NONE'. Это может вызвать проблемы при сравнении возвращаемого
   значения функции (значение без знака) с отрицательной константой.
4. **Рекомендация по использованию:**
   На сегодняшний день 'inet_addr' считается устаревшей функцией, и рекомендуется использовать 'inet_aton'.
   Еще лучше использовать более новые функции, работающие как с IPv4, так и с IPv6.
5. **'inet_ntoa' и его особенности:**
   Функция 'inet_ntoa' преобразует 32-разрядный двоичный адрес IPv4, хранящийся в сетевом порядке байтов, в точечно-
   десятичную строку.
   Важно отметить, что строка, на которую указывает возвращаемый указатель, находится в статической памяти, что означает,
   что функция не является повторно входимой (reentrant) и не поддерживает многократное вызовы.

**Использование кода:**

Этот код демонстрирует как работу функций преобразования IP-адресов, так и особенности некоторых из них. Он может быть 
использован для примера и понимания, как использовать функции 'inet_aton', 'inet_addr', и 'inet_ntoa' для работы с IP-
адресами в сетевом программировании.

**Sample program output:**
``` 
IP address in binary format: 0xC0A80101
IP address as a 32-bit number: 0x0101A8C0
IP address in string format: 192.168.1.1

Process finished with exit code 0
``` 
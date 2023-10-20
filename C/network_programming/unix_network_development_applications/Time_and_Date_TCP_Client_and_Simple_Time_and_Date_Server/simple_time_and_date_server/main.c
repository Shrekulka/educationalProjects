#include "common.h"

int main(int argc, char** argv)
{
	int listenfd;  // Дескриптор соксета для прослушивания входящих соединений.

	int connfd;  // Дескриптор соксета для установленного соединения с клиентом.

	struct sockaddr_in servaddr;  // Структура, описывающая адрес сервера.

	char buff[MAXLINE];  // Буфер для хранения данных.

	time_t ticks;  // Переменная для хранения времени.

	// Создаем соксет для прослушивания входящих соединений на порту 13 (daytime).
	listenfd = Socket(AF_INET, SOCK_STREAM, 0);

	// Заполняем структуру servaddr нулями и устанавливаем семейство адресов и порт.
	bzero(&servaddr, sizeof(servaddr));

	// Устанавливаем член структуры servaddr с именем sin_family равным AF_INET. Это указывает, что мы используем
	// семейство адресов IPv4.
	servaddr.sin_family = AF_INET;

	// Устанавливаем член структуры servaddr с именем sin_addr.s_addr равным INADDR_ANY. INADDR_ANY представляет собой
	// специальную константу, обозначающую, что сервер будет слушать на всех доступных сетевых интерфейсах. Мы также
	// используем функцию htonl, чтобы конвертировать это значение в сетевой порядок байтов (big-endian), что важно при
	// работе с сетевыми функциями.
	servaddr.sin_addr.s_addr = htonl(INADDR_ANY);

	servaddr.sin_port = htons(PORT);  // Порт 13 - это порт daytime сервера.

	// Привязываем соксет к адресу и порту.
	Bind(listenfd, (SA*)&servaddr, sizeof(servaddr));

	// Переводим соксет в режим прослушивания с максимальной очередью ожидающих соединений LISTENQ.
	Listen(listenfd, LISTENQ);

	for (;;)
	{
		// Принимаем входящее соединение и создаем новый соксет connfd для общения с клиентом.
		connfd = Accept(listenfd, (SA*)NULL, NULL);

		// Получаем текущее время.
		ticks = time(NULL);

		// Формируем строку с текущим временем в формате "День, Месяц ДД ГГГГ ЧЧ:ММ:СС\r\n".
		snprintf(buff, sizeof(buff), "%.24s\r\n", ctime(&ticks));

		// Отправляем клиенту строку с временем.
		Write(connfd, buff, strlen(buff));

		// Закрываем соксет для завершения соединения с клиентом.
		Close(connfd);
	}
}


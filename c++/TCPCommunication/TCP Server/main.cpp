#include "pch.h"
#include <iostream>
#include <stdexcept>

int main()
{
	CommandParser p;
	SimpleCommandHandler connection(10, p);

	try {
		TCPServer server(7070, "127.0.0.1", connection);
		server.listen();
	} catch (const std::exception& ex) {
		std::cerr << "Error occurred: " << ex.what() << std::endl;
		return 1;
	}

	return 0;
}

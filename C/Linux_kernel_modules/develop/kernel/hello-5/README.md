# hello-5.c – The Linux kernel module supports passing command-line arguments during its loading. These arguments, 
specified after the module loading command (e.g., insmod), can influence the configuration and parameters of the module.
To pass values for variables, including arrays, the module_param_array macro is used. This macro enables the module to 
accept arrays of data provided by the user during module loading.

## Steps on Ubuntu 23.10:

1. Install the necessary tools for building programs and managing kernel modules on our system:

    ```bash
    sudo apt-get install build-essential kmod
    ```

2. Display information about the loaded kernel modules in the system:

   a. Using the `lsmod` command, which outputs a formatted list of modules:

    ```bash
    sudo lsmod
    ```

   b. Read the contents of the /proc/modules file:

    ```bash
    sudo cat /proc/modules
    ```

3. Update the package list and upgrade the system:

    ```bash
    sudo apt update && sudo full-upgrade
    ```

   or

    ```bash
    sudo apt update && sudo dist-upgrade
    ```

4. Install the corresponding header files:

    ```bash
    sudo apt-get install linux-headers-$(uname -r)
    ```

5. Create a new project at the path - `/home/current_user/develop/kernel/hello-5`.

6. In the project's root, create the files `hello-5.c`.

7. In the project's root, create `Makefile`.

8. Navigate to our project directory:

    ```bash
    cd /home/current_user/develop/kernel/hello-5
    ```

9. Use `make` to compile its code:

    ```bash
    make
    ```

   Example input and output:

    ```bash
    current_user@current_user:~/develop/kernel/hello-5$ make
    make -C /lib/modules/6.5.0-13-generic/build M=/home/current_user/develop/kernel/hello-5 modules
    make[1]: Entering directory '/usr/src/linux-headers-6.5.0-13-generic'
    warning: the compiler differs from the one used to build the kernel
      The kernel was built by: aarch64-linux-gnu-gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
      You are using:           gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
      CC [M]  /home/current_user/develop/kernel/hello-5/hello-5.o
      MODPOST /home/current_user/develop/kernel/hello-5/Module.symvers
      CC [M]  /home/current_user/develop/kernel/hello-5/hello-5.mod.o
      LD [M]  /home/current_user/develop/kernel/hello-5/hello-5.ko
      BTF [M] /home/current_user/develop/kernel/hello-5/hello-5.ko
    Skipping BTF generation for /home/current_user/develop/kernel/hello-5/hello-5.ko due to unavailability of vmlinux
    make[1]: Leaving directory '/usr/src/linux-headers-6.5.0-13-generic'
    ```

10. Get information about the module:

	```bash
    current_user@current_user:~/develop/kernel/hello-5$ modinfo hello-5.ko
    filename:       /home/current_user/develop/kernel/hello-5/hello-5.ko
    description:    Pass command line arguments to a kernel module
    author:         shrekulka
    license:        GPL
    srcversion:     1364F2CAEE85112C5F2EE04
    depends:        
    name:           hello_5
    vermagic:       6.5.0-13-generic SMP preempt mod_unload modversions aarch64
    parm:           myshort:A short integer (short)
    parm:           myint:An integer (int)
    parm:           mylong:A long integer (long)
    parm:           mystring:A character string (charp)
    parm:           myintarray:An array of integers (array of int)
    ```

11. Ensure that the module named "hello_5" is not loaded:

	```bash
    sudo lsmod | grep hello
    ```

12. After successful compilation, load the module into the kernel:

	```bash
    sudo insmod hello-5.ko mystring="bebop" myintarray=-1
    ```

13. Check the module's loading:

	```bash
    current_user@current_user:~/develop/kernel/hello-5$ sudo lsmod | grep hello
    hello_5                12288  0
    ```

14. It is recommended to experiment with the following code:

	(Code execution examples)

15. To remove the module, use the command:

	```bash
    sudo rmmod hello_5
    ```

16. This allows viewing kernel-related system logs and filters lines containing "kernel":
	```bash
	current_user@current_user:~/develop/kernel/hello-5$ sudo journalctl --since "1 hour ago" | grep kernel
	...
	Nov 25 11:40:27 current_user kernel: Hello, world 5
	Nov 25 11:40:27 current_user kernel: myshort is a short integer: 1
	Nov 25 11:40:27 current_user kernel: myint is an integer: 420
	Nov 25 11:40:27 current_user kernel: mylong is a long integer: 9999
	Nov 25 11:40:27 current_user kernel: mystring is a string: bebop
	Nov 25 11:40:27 current_user kernel: myintarray[0] = -1
	Nov 25 11:40:27 current_user kernel: myintarray[1] = 420
	Nov 25 11:40:27 current_user kernel: got 1 argument for myintarray.
	Nov 25 11:41:24 current_user sudo[12171]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-5 ;
	 USER=root ; COMMAND=/usr/sbin/lsmod
	Nov 25 11:46:34 current_user kernel: audit: type=1400 audit(1700905594.294:290): apparmor="DENIED" operation="open" 
	class="file" profile="snap.chromium.chromium" name="/proc/pressure/cpu" pid=3153 comm="ThreadPoolForeg" 
	requested_mask="r" denied_mask="r" fsuid=1000 ouid=0
	Nov 25 11:46:34 current_user kernel: audit: type=1400 audit(1700905594.294:291): apparmor="DENIED" operation="open" 
	class="file" profile="snap.chromium.chromium" name="/proc/pressure/io" pid=3153 comm="ThreadPoolForeg" 
	requested_mask="r" denied_mask="r" fsuid=1000 ouid=0
	Nov 25 11:46:34 current_user kernel: audit: type=1400 audit(1700905594.294:292): apparmor="DENIED" operation="open"
	 class="file" profile="snap.chromium.chromium" name="/proc/pressure/memory" pid=3153 comm="ThreadPoolForeg" 
	requested_mask="r" denied_mask="r" fsuid=1000 ouid=0
	Nov 25 11:50:39 current_user sudo[12191]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-5 ;
	 USER=root ; COMMAND=/usr/bin/dmesg -t
	Nov 25 11:51:40 current_user sudo[12197]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-5 ;
	 USER=root ; COMMAND=/usr/sbin/lsmod
	Nov 25 11:52:20 current_user sudo[12205]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-5 ;
	 USER=root ; COMMAND=/usr/sbin/rmmod hello_5
	Nov 25 11:52:20 current_user kernel: Goodbye, world 5
	Nov 25 11:52:43 current_user sudo[12212]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-5 ;
	 USER=root ; COMMAND=/usr/bin/journalctl --since '1 hour ago'
	```
	




# hello-5.c – Модуль ядра Linux поддерживает передачу аргументов командной строки при его загрузке. Эти аргументы, 
указанные после команды загрузки модуля (например, insmod), могут влиять на конфигурацию и параметры модуля. Для 
передачи значений переменных, включая массивы, используется макрос module_param_array. Этот макрос позволяет модулю 
принимать массивы данных, предоставляемые пользователем при загрузке модуля.

## Шаги в Ubuntu 23.10:

1. Устанавливаем необходимые инструменты для сборки программ и управления модулями ядра на нашей системе:

    ```bash
    sudo apt-get install build-essential kmod
    ```

2. Отображаем информацию о загруженных модулях ядра в системе:

    a. С помощью команды `lsmod`, которая выводит отформатированный список модулей:

    ```bash
    sudo lsmod
    ```

    b. Читаем содержимое файла /proc/modules:

    ```bash
    sudo cat /proc/modules
    ```

3. Обновляем список пакетов и обновляем систему:

    ```bash
    sudo apt update && sudo full-upgrade
    ```

    или

    ```bash
    sudo apt update && sudo dist-upgrade
    ```

4. Устанавливаем соответствующие заголовочные файлы:

    ```bash
    sudo apt-get install linux-headers-$(uname -r)
    ```

5. Создаем новый проект по пути - `/home/current_user/develop/kernel/hello-5`.

6. В корне проекта создаем файлы `hello-5.c`.

7. В корне проекта создаем `Makefile`.

8. Переходим в нашу директорию проекта:

    ```bash
    cd /home/current_user/develop/kernel/hello-5
    ```

9. Использует `make` для компиляции его кода:

    ```bash
    make
    ```

    Пример ввода и вывода:

    ```bash
    current_user@current_user:~/develop/kernel/hello-5$ make
    make -C /lib/modules/6.5.0-13-generic/build M=/home/current_user/develop/kernel/hello-5 modules
    make[1]: вход в каталог «/usr/src/linux-headers-6.5.0-13-generic»
    warning: the compiler differs from the one used to build the kernel
      The kernel was built by: aarch64-linux-gnu-gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
      You are using:           gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
      CC [M]  /home/current_user/develop/kernel/hello-5/hello-5.o
      MODPOST /home/current_user/develop/kernel/hello-5/Module.symvers
      CC [M]  /home/current_user/develop/kernel/hello-5/hello-5.mod.o
      LD [M]  /home/current_user/develop/kernel/hello-5/hello-5.ko
      BTF [M] /home/current_user/develop/kernel/hello-5/hello-5.ko
    Skipping BTF generation for /home/current_user/develop/kernel/hello-5/hello-5.ko due to unavailability of vmlinux
    make[1]: выход из каталога «/usr/src/linux-headers-6.5.0-13-generic»
    ```

10. Получаем информацию о модуле:

    ```bash
    current_user@current_user:~/develop/kernel/hello-5$ modinfo hello-5.ko
    filename:       /home/current_user/develop/kernel/hello-5/hello-5.ko
    description:    Pass command line arguments to a kernel module
    author:         shrekulka
    license:        GPL
    srcversion:     1364F2CAEE85112C5F2EE04
    depends:        
    name:           hello_5
    vermagic:       6.5.0-13-generic SMP preempt mod_unload modversions aarch64
    parm:           myshort:A short integer (short)
    parm:           myint:An integer (int)
    parm:           mylong:A long integer (long)
    parm:           mystring:A character string (charp)
    parm:           myintarray:An array of integers (array of int)
    ```

11. Убеждаемся, что модуль с именем "hello_5" не загружен:

    ```bash
    sudo lsmod | grep hello
    ```

12. После успешной компиляции загружаем модуль в ядро:

    ```bash
    sudo insmod hello-5.ko mystring="bebop" myintarray=-1
    ```

13. Проверяем загрузку модуля:

    ```bash
    current_user@current_user:~/develop/kernel/hello-5$ sudo lsmod | grep hello
    hello_5                12288  0
    ```
14. Рекомендовано поэкспериментировать со следующим кодом:
	```bash
	# Загружаем модуль hello-5.ko с аргументами командной строки mystring="bebop" и myintarray=-1
	$ sudo insmod hello-5.ko mystring="bebop" myintarray=-1

	# Выводим последние 7 строк из системного журнала с тегами
	$ sudo dmesg -t | tail -7

	# Вывод информации о переменных, установленных в модуле, после его загрузки
	myshort is a short integer: 1
	myint is an integer: 420
	mylong is a long integer: 9999
	mystring is a string: bebop
	myintarray[0] = -1
	myintarray[1] = 420
	got 1 arguments for myintarray.

	# Выгружаем модуль hello-5
	$ sudo rmmod hello-5

	# Выводим последнюю строку из системного журнала с тегами после выгрузки модуля
	$ sudo dmesg -t | tail -1
	Goodbye, world 5

	# Загружаем модуль hello-5.ko с аргументами командной строки mystring="supercalifragilisticexpialidocious"
	$ sudo insmod hello-5.ko mystring="supercalifragilisticexpialidocious"

	# Выводим последние 7 строк из системного журнала с тегами
	$ sudo dmesg -t | tail -7

	# Вывод информации о переменных, установленных в модуле, после его загрузки
	myshort is a short integer: 1
	myint is an integer: 420
	mylong is a long integer: 9999
	mystring is a string: supercalifragilisticexpialidocious
	myintarray[0] = -1
	myintarray[1] = -1
	got 2 arguments for myintarray.

	# Выгружаем модуль hello-5
	$ sudo rmmod hello-5

	# Выводим последнюю строку из системного журнала с тегами после выгрузки модуля
	$ sudo dmesg -t | tail -1

	# Загружаем модуль hello-5.ko с аргументом командной строки mylong=hello
	insmod: ERROR: could not insert module hello-5.ko: Invalid parameters
	```

15. Для удаления модуля используется команда:

    ```bash
    sudo rmmod hello_5
    ```

16. Это позволяет просмотреть системные логи, связанные с ядром Linux, и фильтрует строки, содержащие "kernel":

    ```bash
    current_user@current_user:~/develop/kernel/hello-5$ sudo journalctl --since "1 hour ago" | grep kernel
    ...
    ноя 25 11:40:27 current_user kernel: Hello, world 5
	ноя 25 11:40:27 current_user kernel: myshort is a short integer: 1
	ноя 25 11:40:27 current_user kernel: myint is an integer: 420
	ноя 25 11:40:27 current_user kernel: mylong is a long integer: 9999
	ноя 25 11:40:27 current_user kernel: mystring is a string: bebop
	ноя 25 11:40:27 current_user kernel: myintarray[0] = -1
	ноя 25 11:40:27 current_user kernel: myintarray[1] = 420
	ноя 25 11:40:27 current_user kernel: got 1 arguments for myintarray.
	ноя 25 11:41:24 current_user sudo[12171]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-5 ;
     USER=root ; COMMAND=/usr/sbin/lsmod
	ноя 25 11:46:34 current_user kernel: audit: type=1400 audit(1700905594.294:290): apparmor="DENIED" operation="open" 
    class="file" profile="snap.chromium.chromium" name="/proc/pressure/cpu" pid=3153 comm="ThreadPoolForeg" 
    requested_mask="r" denied_mask="r" fsuid=1000 ouid=0
	ноя 25 11:46:34 current_user kernel: audit: type=1400 audit(1700905594.294:291): apparmor="DENIED" operation="open" 
    class="file" profile="snap.chromium.chromium" name="/proc/pressure/io" pid=3153 comm="ThreadPoolForeg" 
    requested_mask="r" denied_mask="r" fsuid=1000 ouid=0
	ноя 25 11:46:34 current_user kernel: audit: type=1400 audit(1700905594.294:292): apparmor="DENIED" operation="open"
     class="file" profile="snap.chromium.chromium" name="/proc/pressure/memory" pid=3153 comm="ThreadPoolForeg" 
    requested_mask="r" denied_mask="r" fsuid=1000 ouid=0
	ноя 25 11:50:39 current_user sudo[12191]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-5 ;
     USER=root ; COMMAND=/usr/bin/dmesg -t
	ноя 25 11:51:40 current_user sudo[12197]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-5 ;
     USER=root ; COMMAND=/usr/sbin/lsmod
	ноя 25 11:52:20 current_user sudo[12205]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-5 ;
     USER=root ; COMMAND=/usr/sbin/rmmod hello_5
	ноя 25 11:52:20 current_user kernel: Goodbye, world 5
	ноя 25 11:52:43 current_user sudo[12212]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-5 ;
     USER=root ; COMMAND=/usr/bin/journalctl --since '1 hour ago'
    ```


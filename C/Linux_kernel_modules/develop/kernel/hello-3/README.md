# hello-3.c – Demonstration of __initdata, __init, __exit Macros, and Module Documentation

## Example of a Linux kernel module using __initdata, __init, and __exit macros to optimize kernel memory usage. The 
module also includes documentation, including license, author, description, and version.

## Steps on Ubuntu 23.10:

1. Install necessary tools for building programs and managing kernel modules on our system:
    ```bash
    sudo apt-get install build-essential kmod
    ```
2. Display information about loaded kernel modules in the system:
    a. Using the lsmod command, which outputs a formatted list of modules:
    ```bash
    sudo lsmod
    ```
    b. Read the contents of the /proc/modules file:
    ```bash
    sudo cat /proc/modules
   ```
3. Update the package list (apt update) and upgrade the system (full-upgrade or dist-upgrade):
    ```bash
    sudo apt update && full-upgrade
    ```
    or
    ```bash
    sudo apt update && dist-upgrade
    ```
4. Install the corresponding header files that may be required for kernel module compilation (for the current kernel 
   version) or other programs:
    ```bash
    sudo apt-get install linux-headers-$(uname -r)
    ```
5. Create a new project at the path - /home/current_user/develop/kernel/hello-3.
6. In the project root, create the file hello-3.c.
7. In the project root, create a Makefile.
8. Navigate to our project directory:
    ```bash
    cd /home/current_user/develop/kernel/hello-3
    ```
9. Use make to compile the code:
    ```bash
    make
    ```
    Example input and output:
    ```bash
    current_user@current_user:~/develop/kernel/hello-3$ make
    make -C /lib/modules/6.5.0-13-generic/build M=/home/current_user/develop/kernel/hello-3 modules
    make[1]: Entering directory '/usr/src/linux-headers-6.5.0-13-generic'
    warning: the compiler differs from the one used to build the kernel
    The kernel was built by: aarch64-linux-gnu-gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
    You are using:           gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
    CC [M]  /home/current_user/develop/kernel/hello-3/hello-3.o
    MODPOST /home/current_user/develop/kernel/hello-3/Module.symvers
    CC [M]  /home/current_user/develop/kernel/hello-3/hello-3.mod.o
    LD [M]  /home/current_user/develop/kernel/hello-3/hello-3.ko
    BTF [M] /home/current_user/develop/kernel/hello-3/hello-3.ko
    Skipping BTF generation for /home/current_user/develop/kernel/hello-3/hello-3.ko due to unavailability of vmlinux
    make[1]: Leaving directory '/usr/src/linux-headers-6.5.0-13-generic'
    ```
10. Get information about the module:
    ```bash
    filename:       /home/shrekulka/develop/kernel/hello-3/hello-3.ko
    version:        1.0
    description:    A sample driver
    author:         shrekulka
    license:        GPL
    srcversion:     CACABD3A0FB0EB1E07BB8BE
    depends:        
    name:           hello_3
    vermagic:       6.5.0-13-generic SMP preempt mod_unload modversions aarch64
    ```
11. Ensure that the module with the name "hello_3" is not loaded:
    ```bash
    sudo lsmod | grep hello
    ```
12. After successful compilation, load the module into the kernel:
    ```bash
    sudo insmod hello-3.ko
    ```
13. Verify the module is loaded:
    ```bash
    current_user@current_user:~/develop/kernel/hello-3$ sudo lsmod | grep hello
    hello_3                12288  0
    ```
14. To remove the module, use the command:
    ```bash
    sudo rmmod hello-3
    ```
15. This allows viewing system logs related to the Linux kernel, filtering lines containing "kernel":
    ```bash
    current_user@current_user:~/develop/kernel/hello-3$ sudo journalctl --since "1 hour ago" | grep kernel
    Nov 24 18:31:56 current_user sudo[8259]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-3 ;
    USER=root ; COMMAND=/usr/sbin/lsmod
    Nov 24 18:32:06 current_user sudo[8265]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-3 ;
    USER=root ; COMMAND=/usr/sbin/insmod hello-3.ko
    Nov 24 18:32:06 current_user kernel: Hello, world 3
    Nov 24 18:32:20 current_user sudo[8271]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-3 ;
    USER=root ; COMMAND=/usr/sbin/lsmod
    Nov 24 18:32:30 current_user sudo[8276]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-3 ;
    USER=root ; COMMAND=/usr/sbin/rmmod hello_3
    Nov 24 18:32:30 current_user kernel: Goodbye, world 3
    Nov 24 18:32:41 current_user sudo[8281]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-3 ;
    USER=root ; COMMAND=/usr/bin/journalctl --since '1 hour ago'
    ```



# hello-3.c – демонстрация макросов `__initdata`, `__init` и `__exit`, а также документирование модуля.

## Пример модуля ядра Linux, который использует макросы `__initdata`, `__init` и `__exit` для оптимизации использования 
памяти ядра. Модуль также содержит документацию, включая лицензию, автора, описание и версию.

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

    b. Читаем содержимое файла `/proc/modules`:

    ```bash
    sudo cat /proc/modules
    ```

3. Обновляем список пакетов (apt update) и обновляем систему (full-upgrade или dist-upgrade):

    ```bash
    sudo apt update && full-upgrade
    ```

    или

    ```bash
    sudo apt update && dist-upgrade
    ```

4. Устанавливаем соответствующие заголовочные файлы, которые могут быть необходимы для компиляции модулей ядра (для 
   текущей версии ядра) или других программ:

    ```bash
    sudo apt-get install linux-headers-$(uname -r)
    ```

5. Создаем новый проект по пути - `/home/current_user/develop/kernel/hello-3`.

6. В корне проекта создаем файл `hello-3.c`.

7. В корне проекта создаем `Makefile`.

8. Переходим в нашу директорию проекта:

    ```bash
    cd /home/current_user/develop/kernel/hello-3
    ```

9. Используем `make` для компиляции кода:

    ```bash
    make
    ```

    Пример ввода и вывода:

    ```bash
    current_user@current_user:~/develop/kernel/hello-3$ make
    make -C /lib/modules/6.5.0-13-generic/build M=/home/current_user/develop/kernel/hello-3 modules
    make[1]: вход в каталог «/usr/src/linux-headers-6.5.0-13-generic»
    warning: the compiler differs from the one used to build the kernel
      The kernel was built by: aarch64-linux-gnu-gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
      You are using:           gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
      CC [M]  /home/current_user/develop/kernel/hello-3/hello-3.o
      MODPOST /home/current_user/develop/kernel/hello-3/Module.symvers
      CC [M]  /home/current_user/develop/kernel/hello-3/hello-3.mod.o
      LD [M]  /home/current_user/develop/kernel/hello-3/hello-3.ko
      BTF [M] /home/current_user/develop/kernel/hello-3/hello-3.ko
    Skipping BTF generation for /home/current_user/develop/kernel/hello-3/hello-3.ko due to unavailability of vmlinux
    make[1]: выход из каталога «/usr/src/linux-headers-6.5.0-13-generic»
    ```

10. Получаем информацию о модуле:

    ```bash
    filename:       /home/shrekulka/develop/kernel/hello-3/hello-3.ko
    version:        1.0
    description:    A sample driver
    author:         shrekulka
    license:        GPL
    srcversion:     CACABD3A0FB0EB1E07BB8BE
    depends:        
    name:           hello_3
    vermagic:       6.5.0-13-generic SMP preempt mod_unload modversions aarch64

    ```

11. Убеждаемся, что модуль с именем "hello_3" не загружен:

    ```bash
    sudo lsmod | grep hello
    ```

12. После успешной компиляции загружаем модуль в ядро:

    ```bash
    sudo insmod hello-3.ko
    ```

13. Проверяем загрузку модуля:

    ```bash
    current_user@current_user:~/develop/kernel/hello-3$ sudo lsmod | grep hello
    hello_3                12288  0
    ```

14. Для удаления модуля используется команда:

    ```bash
    sudo rmmod hello-3
    ```

15. Это позволяет просмотреть системные логи, связанные с ядром Linux, и фильтрует строки, содержащие "kernel":

    ```bash
    current_user@current_user:~/develop/kernel/hello-3$ sudo journalctl --since "1 hour ago" | grep kernel
    ноя 24 18:31:56 current_user sudo[8259]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-3 ; 
    USER=root ; COMMAND=/usr/sbin/lsmod
    ноя 24 18:32:06 current_user sudo[8265]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-3 ; 
    USER=root ; COMMAND=/usr/sbin/insmod hello-3.ko
    ноя 24 18:32:06 current_user kernel: Hello, world 3
    ноя 24 18:32:20 current_user sudo[8271]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-3 ;
     USER=root ; COMMAND=/usr/sbin/lsmod
    ноя 24 18:32:30 current_user sudo[8276]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-3 ; 
    USER=root ; COMMAND=/usr/sbin/rmmod hello_3
    ноя 24 18:32:30 current_user kernel: Goodbye, world 3
    ноя 24 18:32:41 current_user sudo[8281]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-3 ; 
    USER=root ; COMMAND=/usr/bin/journalctl --since '1 hour ago'
    ```

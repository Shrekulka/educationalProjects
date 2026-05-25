# Example of Using sysfs

## Steps in Ubuntu 23.10:

1. Install necessary tools for building programs and managing kernel modules on our system:

    ```bash
    sudo apt-get install build-essential kmod
    ```

2. Update the package list (apt update) and upgrade the system (full-upgrade or dist-upgrade):

    ```bash
    sudo apt update && full-upgrade
    ```

   or

    ```bash
    sudo apt update && dist-upgrade
    ```

3. Install corresponding header files that may be needed for compiling kernel modules (for the current kernel version) or other programs:

    ```bash
    sudo apt-get install linux-headers-$(uname -r)
    ```

4. Create a new project at the path - `/home/current_user/develop/kernel/sysfs/hello-sysfs`.

5. In the project's root, create files `hello-sysfs.h` and `hello-sysfs.c`.

6. In the project's root, create a `Makefile`.

7. Navigate to our project directory:

    ```bash
    cd /home/current_user/develop/kernel/sysfs/hello-sysfs
    ```

8. Use `make` to compile the code:

    ```bash
    make
    ```

   Example input and output:

    ```bash
    current_user@current_user:~/develop/kernel/sysfs/hello-sysfs$ make
    make -C /lib/modules/6.5.0-14-generic/build M=/home/current_user/develop/kernel/sysfs/hello-sysfs modules
    make[1]: Entering directory '/usr/src/linux-headers-6.5.0-14-generic'
    warning: the compiler differs from the one used to build the kernel
    The kernel was built by: aarch64-linux-gnu-gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
    You are using:           gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
    CC [M]  /home/current_user/develop/kernel/sysfs/hello-sysfs/hello-sysfs.o
    MODPOST /home/current_user/develop/kernel/sysfs/hello-sysfs/Module.symvers
    CC [M]  /home/current_user/develop/kernel/sysfs/hello-sysfs/hello-sysfs.mod.o
    LD [M]  /home/current_user/develop/kernel/sysfs/hello-sysfs/hello-sysfs.ko
    BTF [M] /home/current_user/develop/kernel/sysfs/hello-sysfs/hello-sysfs.ko
    Skipping BTF generation for /home/current_user/develop/kernel/sysfs/hello-sysfs/hello-sysfs.ko due to unavailability of vmlinux
    make[1]: Leaving directory '/usr/src/linux-headers-6.5.0-14-generic'
    ```

9. Get information about the module:

    ```bash
    current_user@current_user:~/develop/kernel/sysfs/hello-sysfs$ modinfo hello-sysfs.ko
    filename:       /home/current_user/develop/kernel/sysfs/hello-sysfs/hello-sysfs.ko
    license:        GPL
    srcversion:     79A6F177609C17903F1DB9E
    depends:        
    name:           hello_sysfs
    vermagic:       6.5.0-14-generic SMP preempt mod_unload modversions aarch64
    ```

10. Ensure that the module named "hello_sysfs" is not loaded:

    ```bash
    sudo lsmod | grep hello_sysfs
    ```

11. After successful compilation, load the module into the kernel:

    ```bash
    sudo insmod hello-sysfs.ko
    ```

12. Check if the module is loaded:

    ```bash
    current_user@current_user:~/develop/kernel/sysfs/hello-sysfs$ sudo lsmod | grep hello_sysfs
    hello_sysfs               12288  0
    ```

13. Check the value of the myvariable variable:

    ```bash
    current_user@current_user:~/develop/kernel/sysfs/hello-sysfs$ sudo cat /sys/kernel/mymodule/myvariable
    0
    ```

14. Change the value of the myvariable variable to 32:

    ```bash
    current_user@current_user:~/develop/kernel/sysfs/hello-sysfs$ sudo echo "32" | sudo tee /sys/kernel/mymodule/myvariable
    32
    ```

15. Check the changed value of the myvariable variable:

    ```bash
    current_user@current_user:~/develop/kernel/sysfs/hello-sysfs$ sudo cat /sys/kernel/mymodule/myvariable
    32
    ```

16. Change the value of the myvariable variable to 12:

    ```bash
    current_user@current_user:~/develop/kernel/sysfs/hello-sysfs$ echo "12" | sudo tee /sys/kernel/mymodule/myvariable
    12
    ```

17. Check the changed value of the myvariable variable:

    ```bash
    current_user@current_user:~/develop/kernel/sysfs/hello-sysfs$ sudo cat /sys/kernel/mymodule/myvariable
    12
    ```

18. To remove the module, use the command:

    ```bash
    current_user@current_user:~/develop/kernel/sysfs/hello-sysfs$ sudo rmmod hello_sysfs
    ```

19. Ensure that the module is no longer loaded:

    ```bash
    current_user@current_user:~/develop/kernel/sysfs/hello-sysfs$ sudo lsmod | grep hello-sysfs
    ```

20. View system logs related to the Linux kernel and filter lines containing "hello":

    ```bash
    current_user@current_user:~/develop/kernel/sysfs/hello-sysfs$ sudo journalctl --since "1 hour ago" | grep "hello"
    Dec 07 14:10:57 current_user sudo[12244]: current_user : TTY=pts/0 ; 
    PWD=/home/current_user/develop/kernel/sysfs/hello-sysfs ; USER=root ; 
    COMMAND=/usr/sbin/insmod hello-sysfs.ko
    Dec 07 14:11:37 current_user sudo[12254]: current_user : TTY=pts/0 ; 
    PWD=/home/current_user/develop/kernel/sysfs/hello-sysfs ; USER=root ; 
    COMMAND=/usr/bin/cat /sys/kernel/mymodule/myvariable
    Dec 07 14:12:07 current_user sudo[12261]: current_user : TTY=pts/0 ; 
    PWD=/home/current_user/develop/kernel/sysfs/hello-sysfs ; USER=root ; 
    COMMAND=/usr/bin/tee /sys/kernel/mymodule/myvariable
    Dec 07 14:12:56 current_user sudo[12274]: current_user : TTY=pts/0 ; 
    PWD=/home/current_user/develop/kernel/sysfs/hello-sysfs ; USER=root ; 
    COMMAND=/usr/bin/cat /sys/kernel/mymodule/myvariable
    Dec 07 14:13:01 current_user sudo[12278]: current_user : TTY=pts/0 ; 
    PWD=/home/current_user/develop/kernel/sysfs/hello-sysfs ; USER=root ; 
    COMMAND=/usr/sbin/rmmod hello_sysfs
    Dec 07 14:13:07 current_user sudo[12283]: current_user : TTY=pts/0 ; 
    PWD=/home/current_user/develop/kernel/sysfs/hello-sysfs ; USER=root ; 
    COMMAND=/usr/sbin/lsmod
    Dec 07 14:13:56 current_user sudo[12287]: current_user : TTY=pts/0 ; 
    PWD=/home/current_user/develop/kernel/sysfs/hello-sysfs ; USER=root ; 
    COMMAND=/usr/bin/journalctl --since '1 hour ago'
    Dec 07 14:14:03 current_user sudo[12291]: current_user : TTY=pts/0 ; 
    PWD=/home/current_user/develop/kernel/sysfs/hello-sysfs ; USER=root ; 
    COMMAND=/usr/bin/journalctl --since '1 hour ago'
    Dec 07 14:18:42 current_user sudo[12311]: current_user : TTY=pts/0 ; 
    PWD=/home/current_user/develop/kernel/sysfs/hello-sysfs ; USER=root ; 
    COMMAND=/usr/bin/journalctl --since '1 hour ago'
    ```





# Пример использования sysfs

## Шаги в Ubuntu 23.10:

1. Устанавливаем необходимые инструменты для сборки программ и управления модулями ядра на нашей системе:

    ```bash
    sudo apt-get install build-essential kmod
    ```

2. Обновляем список пакетов (apt update) и обновляем систему (full-upgrade или dist-upgrade):

    ```bash
    sudo apt update && full-upgrade
    ```

   или

    ```bash
    sudo apt update && dist-upgrade
    ```

3. Устанавливаем соответствующие заголовочные файлы, которые могут быть необходимы для компиляции модулей ядра (для
   текущей версии ядра) или других программ:

    ```bash
    sudo apt-get install linux-headers-$(uname -r)
    ```

4. Создаем новый проект по пути - `/home/current_user/develop/kernel/sysfs/hello-sysfs`.

5. В корне проекта создаем файлы `hello-sysfs.h` и `hello-sysfs.c`.

6. В корне проекта создаем `Makefile`.

7. Переходим в нашу директорию проекта:

    ```bash
    cd /home/current_user/develop/kernel/sysfs/hello-sysfs
    ```

8. Используем `make` для компиляции кода:

    ```bash
    make
    ```

   Пример ввода и вывода:

    ```bash
    current_user@current_user:~/develop/kernel/sysfs/hello-sysfs$ make
    make -C /lib/modules/6.5.0-14-generic/build M=/home/current_user/develop/kernel/sysfs/hello-sysfs modules
    make[1]: вход в каталог «/usr/src/linux-headers-6.5.0-14-generic»
    warning: the compiler differs from the one used to build the kernel
    The kernel was built by: aarch64-linux-gnu-gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
    You are using:           gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
    CC [M]  /home/current_user/develop/kernel/sysfs/hello-sysfs/hello-sysfs.o
    MODPOST /home/current_user/develop/kernel/sysfs/hello-sysfs/Module.symvers
    CC [M]  /home/current_user/develop/kernel/sysfs/hello-sysfs/hello-sysfs.mod.o
    LD [M]  /home/current_user/develop/kernel/sysfs/hello-sysfs/hello-sysfs.ko
    BTF [M] /home/current_user/develop/kernel/sysfs/hello-sysfs/hello-sysfs.ko
    Skipping BTF generation for /home/current_user/develop/kernel/sysfs/hello-sysfs/hello-sysfs.ko due to unavailability of vmlinux
    make[1]: выход из каталога «/usr/src/linux-headers-6.5.0-14-generic»
    ```
9. Получаем информацию о модуле:

    ```bash
    current_user@current_user:~/develop/kernel/sysfs/hello-sysfs$ modinfo hello-sysfs.ko
    filename:       /home/current_user/develop/kernel/sysfs/hello-sysfs/hello-sysfs.ko
    license:        GPL
    srcversion:     79A6F177609C17903F1DB9E
    depends:        
    name:           hello_sysfs
    vermagic:       6.5.0-14-generic SMP preempt mod_unload modversions aarch64
    ```

10. Убеждаемся, что модуль с именем "hello_sysfs" не загружен:

    ```bash
    sudo lsmod | grep hello_sysfs
    ```

11. После успешной компиляции загружаем модуль в ядро:

    ```bash
    sudo insmod hello-sysfs.ko
    ```

12. Проверяем загрузку модуля:

    ```bash
    current_user@current_user:~/develop/kernel/sysfs/hello-sysfs$ sudo lsmod | grep hello_sysfs
	hello_sysfs               12288  0
    ```

13. Проверяем значение переменной myvariable:

    ```bash
    current_user@current_user:~/develop/kernel/sysfs/hello-sysfs$ sudo cat /sys/kernel/mymodule/myvariable
    0
    ```

14. Изменяем значение переменной myvariable на 32:

    ```bash
    current_user@current_user:~/develop/kernel/sysfs/hello-sysfs$ sudo echo "32" | sudo tee /sys/kernel/mymodule/myvariable
    32
    ```

15. Проверяем измененное значение переменной myvariable:

    ```bash
    current_user@current_user:~/develop/kernel/sysfs/hello-sysfs$ sudo cat /sys/kernel/mymodule/myvariable
    32
    ```

16. Изменяем значение переменной myvariable на 12:

    ```bash
    current_user@current_user:~/develop/kernel/sysfs/hello-sysfs$ echo "12" | sudo tee /sys/kernel/mymodule/myvariable
    12
    ```

17. Проверяем измененное значение переменной myvariable:

    ```bash
    current_user@current_user:~/develop/kernel/sysfs/hello-sysfs$ sudo cat /sys/kernel/mymodule/myvariable
    12
    ```

18. Для удаления модуля используется команда:

    ```bash
    current_user@current_user:~/develop/kernel/sysfs/hello-sysfs$ sudo rmmod hello_sysfs
    ```

19. Убеждаемся, что модуль больше не загружен:

    ```bash
    current_user@current_user:~/develop/kernel/sysfs/hello-sysfs$ sudo lsmod | grep hello-sysfs
    ```

20. Просматриваем системные логи, связанные с ядром Linux, и фильтруем строки, содержащие "hello":

    ```bash
    current_user@current_user:~/develop/kernel/sysfs/hello-sysfs$ sudo journalctl --since "1 hour ago" | grep "hello"
    дек 07 14:10:19 current_user sudo[12238]: current_user : TTY=pts/0 ; 
    PWD=/home/current_user/develop/kernel/sysfs/hello-sysfs ; USER=root ; 
    COMMAND=/usr/sbin/lsmod
    дек 07 14:10:57 current_user sudo[12244]: current_user : TTY=pts/0 ; 
    PWD=/home/current_user/develop/kernel/sysfs/hello-sysfs ; USER=root ; 
    COMMAND=/usr/sbin/insmod hello-sysfs.ko
    дек 07 14:11:29 current_user sudo[12248]: current_user : TTY=pts/0 ; 
    PWD=/home/current_user/develop/kernel/sysfs/hello-sysfs ; USER=root ; 
    COMMAND=/usr/sbin/lsmod
    дек 07 14:11:37 current_user sudo[12254]: current_user : TTY=pts/0 ; 
    PWD=/home/current_user/develop/kernel/sysfs/hello-sysfs ; USER=root ; 
    COMMAND=/usr/bin/cat /sys/kernel/mymodule/myvariable
    дек 07 14:12:07 current_user sudo[12260]: current_user : TTY=pts/0 ; 
    PWD=/home/current_user/develop/kernel/sysfs/hello-sysfs ; USER=root ; 
    COMMAND=/usr/bin/echo 32
    дек 07 14:12:07 current_user sudo[12261]: current_user : TTY=pts/0 ; 
    PWD=/home/current_user/develop/kernel/sysfs/hello-sysfs ; USER=root ; 
    COMMAND=/usr/bin/tee /sys/kernel/mymodule/myvariable
    дек 07 14:12:20 current_user sudo[12266]: current_user : TTY=pts/0 ; 
    PWD=/home/current_user/develop/kernel/sysfs/hello-sysfs ; USER=root ; 
    COMMAND=/usr/bin/cat /sys/kernel/mymodule/myvariable
    дек 07 14:12:51 current_user sudo[12271]: current_user : TTY=pts/0 ; 
    PWD=/home/current_user/develop/kernel/sysfs/hello-sysfs ; USER=root ; 
    COMMAND=/usr/bin/tee /sys/kernel/mymodule/myvariable
    дек 07 14:12:56 current_user sudo[12274]: current_user : TTY=pts/0 ; 
    PWD=/home/current_user/develop/kernel/sysfs/hello-sysfs ; USER=root ; 
    COMMAND=/usr/bin/cat /sys/kernel/mymodule/myvariable
    дек 07 14:13:01 current_user sudo[12278]: current_user : TTY=pts/0 ; 
    PWD=/home/current_user/develop/kernel/sysfs/hello-sysfs ; USER=root ; 
    COMMAND=/usr/sbin/rmmod hello_sysfs
    дек 07 14:13:07 current_user sudo[12283]: current_user : TTY=pts/0 ; 
    PWD=/home/current_user/develop/kernel/sysfs/hello-sysfs ; USER=root ; 
    COMMAND=/usr/sbin/lsmod
    дек 07 14:13:56 current_user sudo[12287]: current_user : TTY=pts/0 ; 
    PWD=/home/current_user/develop/kernel/sysfs/hello-sysfs ; USER=root ; 
    COMMAND=/usr/bin/journalctl --since '1 hour ago'
    дек 07 14:14:03 current_user sudo[12291]: current_user : TTY=pts/0 ; 
    PWD=/home/current_user/develop/kernel/sysfs/hello-sysfs ; USER=root ; 
    COMMAND=/usr/bin/journalctl --since '1 hour ago'
    дек 07 14:18:42 current_user sudo[12311]: current_user : TTY=pts/0 ; 
    PWD=/home/current_user/develop/kernel/sysfs/hello-sysfs ; USER=root ; 
    COMMAND=/usr/bin/journalctl --since '1 hour ago'
    ```
# hello-1.c – Simple Kernel Module

## Steps on Ubuntu 23.10:

1. Install necessary tools for program compilation and kernel module management on your system:

    ```bash
    sudo apt-get install build-essential kmod
    ```

2. Display information about loaded kernel modules in the system:

   a. Using the `lsmod` command, which outputs a formatted list of modules:

    ```bash
    sudo lsmod
    ```

   b. Read the contents of the `/proc/modules` file:

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

4. Install the corresponding header files, which may be needed for kernel module compilation (for the current kernel 
   version) or other programs:

    ```bash
    sudo apt-get install linux-headers-$(uname -r)
    ```

5. Create a new project at the path - `/home/current_user/develop/kernel/hello-1`.

6. In the project root, create the files `hello-1.c`.

7. In the project root, create `Makefile`.

8. Change to our project directory:

    ```bash
    cd /home/current_user/develop/kernel/hello-1
    ```

9. Use `make` to compile the code:

    ```bash
    make
    ```

   Example input and output:

    ```bash
    current_user@current_user:~/develop/kernel/hello-1$ make
    make -C /lib/modules/6.5.0-13-generic/build M=/home/current_user/develop/kernel/hello-1 modules
    make[1]: Entering directory '/usr/src/linux-headers-6.5.0-13-generic'
    warning: the compiler differs from the one used to build the kernel
      The kernel was built by: aarch64-linux-gnu-gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
      You are using:           gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
      CC [M]  /home/current_user/develop/kernel/hello-1/hello-1.o
      MODPOST /home/current_user/develop/kernel/hello-1/Module.symvers
      CC [M]  /home/current_user/develop/kernel/hello-1/hello-1.mod.o
      LD [M]  /home/current_user/develop/kernel/hello-1/hello-1.ko
      BTF [M] /home/current_user/develop/kernel/hello-1/hello-1.ko
    Skipping BTF generation for /home/current_user/develop/kernel/hello-1/hello-1.ko due to unavailability of vmlinux
    make[1]: Leaving directory '/usr/src/linux-headers-6.5.0-13-generic'
    ```

10. Get information about the module:

    ```bash
    current_user@current_user:~/develop/kernel/hello-1$ modinfo hello-1.ko
    filename:       /home/current_user/develop/kernel/hello-1/hello-1.ko
    license:        GPL
    srcversion:     6EEFF9BA2D82E6F0305588C
    depends:        
    name:           hello_1
    vermagic:       6.5.0-13-generic SMP preempt mod_unload modversions aarch64
    ```

11. Ensure that the module with the name "hello_1" is not loaded:

    ```bash
    sudo lsmod | grep hello
    ```

12. After successful compilation, load the module into the kernel:

    ```bash
    sudo insmod hello-1.ko
    ```

13. Check the module loading:

    ```bash
    current_user@current_user:~/develop/kernel/hello-1$ sudo lsmod | grep hello
    hello_1                12288  0
    ```

14. To remove the module, use the command:

    ```bash
    sudo rmmod hello_1
    ```

15. This allows you to view system logs related to the Linux kernel and filter lines containing "kernel" -
    `sudo journalctl --since "1 hour ago" | grep kernel`:

    ```bash
    ...
    Nov 24 14:09:57 current_user sudo[11585]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-1 ; 
    USER=root ; COMMAND=/usr/sbin/insmod hello-1.ko
    Nov 24 14:09:57 current_user kernel: Hello world 1.
    Nov 24 14:11:07 current_user sudo[11596]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-1 ; 
    USER=root ; COMMAND=/usr/sbin/rmmod hello_1
    Nov 24 14:11:07 current_user kernel: Goodbye world 1.
    Nov 24 14:11:34 current_user sudo[11602]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-1 ; 
    USER=root ; COMMAND=/usr/bin/journalctl --since '1 hour ago'
    ```





# hello-1.c – простейший модуль ядра

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

5. Создаем новый проект по пути - `/home/current_user/develop/kernel/hello-1`.

6. В корне проекта создаем файлы `hello-1.c`.

7. В корне проекта создаем `Makefile`.

8. Переходим в нашу директорию проекта:

    ```bash
    cd /home/current_user/develop/kernel/hello-1
    ```

9. Используем `make` для компиляции кода:

    ```bash
    make
    ```

    Пример ввода и вывода:

    ```bash
    current_user@current_user:~/develop/kernel/hello-1$ make
    make -C /lib/modules/6.5.0-13-generic/build M=/home/current_user/develop/kernel/hello-1 modules
    make[1]: вход в каталог «/usr/src/linux-headers-6.5.0-13-generic»
    warning: the compiler differs from the one used to build the kernel
      The kernel was built by: aarch64-linux-gnu-gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
      You are using:           gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
      CC [M]  /home/current_user/develop/kernel/hello-1/hello-1.o
      MODPOST /home/current_user/develop/kernel/hello-1/Module.symvers
      CC [M]  /home/current_user/develop/kernel/hello-1/hello-1.mod.o
      LD [M]  /home/current_user/develop/kernel/hello-1/hello-1.ko
      BTF [M] /home/current_user/develop/kernel/hello-1/hello-1.ko
    Skipping BTF generation for /home/current_user/develop/kernel/hello-1/hello-1.ko due to unavailability of vmlinux
    make[1]: выход из каталога «/usr/src/linux-headers-6.5.0-13-generic»
    ```

10. Получаем информацию о модуле:

    ```bash
    current_user@current_user:~/develop/kernel/hello-1$ modinfo hello-1.ko
    filename:       /home/current_user/develop/kernel/hello-1/hello-1.ko
    license:        GPL
    srcversion:     6EEFF9BA2D82E6F0305588C
    depends:        
    name:           hello_1
    vermagic:       6.5.0-13-generic SMP preempt mod_unload modversions aarch64
    ```

11. Убеждаемся, что модуль с именем "hello_1" не загружен:

    ```bash
    sudo lsmod | grep hello
    ```

12. После успешной компиляции загружаем модуль в ядро:

    ```bash
    sudo insmod hello-1.ko
    ```

13. Проверяем загрузку модуля:

    ```bash
    current_user@current_user:~/develop/kernel/hello-1$ sudo lsmod | grep hello
    hello_1                12288  0
    ```

14. Для удаления модуля используется команда:

    ```bash
    sudo rmmod hello_1
    ```

15. Это позволяет просмотреть системные логи, связанные с ядром Linux, и фильтрует строки, содержащие "kernel" - 
    sudo journalctl --since "1 hour ago" | grep kernel:

    ```bash
    ...
    ноя 24 14:09:57 current_user sudo[11585]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-1 ; 
    USER=root ; COMMAND=/usr/sbin/insmod hello-1.ko
    ноя 24 14:09:57 current_user kernel: Hello world 1.
    ноя 24 14:11:07 current_user sudo[11596]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-1 ; 
    USER=root ; COMMAND=/usr/sbin/rmmod hello_1
    ноя 24 14:11:07 current_user kernel: Goodbye world 1.
    ноя 24 14:11:34 current_user sudo[11602]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-1 ; 
    USER=root ; COMMAND=/usr/bin/journalctl --since '1 hour ago'
     ```

# hello-1.c – Simplest Kernel Module
# hello-2.c – Demonstration of module_init() and module_exit() macros. This approach is preferred over using 
              init_module() and cleanup_module().

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

5. Create a new project at the path - `/home/current_user/develop/kernel/hello-2`.

6. In the project root, create files `hello-1.c` and `hello-2.c`.

7. In the project root, create `Makefile`.

8. Change to our project directory:

    ```bash
    cd /home/current_user/develop/kernel/hello-2
    ```

9. Use `make` to compile the code:

    ```bash
    make
    ```

   Example input and output:

    ```bash
    current_user@current_user:~/develop/kernel/hello-2$ make 
    make -C /lib/modules/6.5.0-13-generic/build M=/home/current_user/develop/kernel/hello-2 modules
    make[1]: Entering directory '/usr/src/linux-headers-6.5.0-13-generic'
    warning: the compiler differs from the one used to build the kernel
      The kernel was built by: aarch64-linux-gnu-gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
      You are using:           gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
      CC [M]  /home/current_user/develop/kernel/hello-2/hello-1.o
      CC [M]  /home/current_user/develop/kernel/hello-2/hello-2.o
      MODPOST /home/current_user/develop/kernel/hello-2/Module.symvers
      CC [M]  /home/current_user/develop/kernel/hello-2/hello-1.mod.o
      LD [M]  /home/current_user/develop/kernel/hello-2/hello-1.ko
      BTF [M] /home/current_user/develop/kernel/hello-2/hello-1.ko
    Skipping BTF generation for /home/current_user/develop/kernel/hello-2/hello-1.ko due to unavailability of vmlinux
      CC [M]  /home/current_user/develop/kernel/hello-2/hello-2.mod.o
      LD [M]  /home/current_user/develop/kernel/hello-2/hello-2.ko
      BTF [M] /home/current_user/develop/kernel/hello-2/hello-2.ko
    Skipping BTF generation for /home/current_user/develop/kernel/hello-2/hello-2.ko due to unavailability of vmlinux
    make[1]: Leaving directory '/usr/src/linux-headers-6.5.0-13-generic'
    ```

10. Get information about the modules `modinfo hello-1.ko` and `modinfo hello-2.ko`:

    ```bash
    current_user@current_user:~/develop/kernel/hello-2$ modinfo hello-1.ko
    filename:       /home/current_user/develop/kernel/hello-2/hello-1.ko
    license:        GPL
    srcversion:     6EEFF9BA2D82E6F0305588C
    depends:        
    name:           hello_1
    vermagic:       6.5.0-13-generic SMP preempt mod_unload modversions aarch64

    current_user@current_user:~/develop/kernel/hello-2$ modinfo hello-2.ko
    filename:       /home/current_user/develop/kernel/hello-2/hello-2.ko
    version:        0.1
    description:    A simple example Linux module.
    author:         Your Name
    license:        GPL
    srcversion:     682083FB93D95DEF7A501AC
    depends:        
    name:           hello_2
    vermagic:       6.5.0-13-generic SMP preempt mod_unload modversions aarch64
    ```

11. Ensure that the module with the name "hello" is not loaded:

    ```bash
    lsmod | grep hello
    ```

12. After successful compilation, load the modules into the kernel:

    ```bash
    sudo insmod hello-1.ko
    sudo insmod hello-2.ko
    ```

13. Check the module loading:

    ```bash
    lsmod | grep hello
    ```

    Example output:

    ```bash
    hello_2                12288  0
    hello_1                12288  0
    ```

14. To remove the modules, use the command:

    ```bash
    sudo rmmod hello-1
    sudo rmmod hello-2
    ```

15. This allows you to view system logs related to the Linux kernel and filter lines containing "kernel" -
    `sudo journalctl --since "1 hour ago" | grep kernel`:
```bash
... Nov 24 11:14:42 current_user sudo[6353]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-1 ;
USER=root ; COMMAND=/usr/bin/apt-get install build-essential kmodsudo apt-get install build-essential kmodsudo apt-get 
install build-essential kmodsudo apt-get install build-essential kmodsudo apt-get install build-essential kmodsudo 
apt-get install build-essential kmodsudo apt-get install build-essential kmodsudo apt-get install build-essential 
kmodsudo apt-get install build-essential kmodsudo apt-get install build-essential kmod Nov 24 11:14:53 current_user 
sudo[6362]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-1 ; USER=root ; 
COMMAND=/usr/bin/apt-get install build-essential kmod Nov 24 11:15:45 current_user sudo[6370]: current_user : TTY=pts/0 ;
PWD=/home/current_user/develop/kernel/hello-1 ; USER=root ; COMMAND=/usr/bin/apt update Nov 24 11:16:01 current_user 
sudo[6872]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-1 ; USER=root ; 
COMMAND=/usr/bin/apt-get install linux-headers-6.5.0-13-generic Nov 24 11:17:10 current_user sudo[7119]: current_user : 
TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-1 ; USER=root ; COMMAND=/usr/sbin/lsmod Nov 24 11:17:22 
current_user sudo[7124]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-1 ; USER=root ; 
COMMAND=/usr/sbin/insmod hello-1.ko Nov 24 11:17:22 current_user kernel: hello_1: loading out-of-tree module taints 
kernel. Nov 24 11:17:22 current_user kernel: hello_1: module verification failed: signature and/or required key missing
 - tainting kernel Nov 24 11:17:22 current_user kernel: Hello world 1. Nov 24 11:18:27 current_user sudo[7137]: 
current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-1 ; USER=root ; COMMAND=/usr/sbin/lsmod 
Nov 24 11:20:29 current_user sudo[7153]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-1 ; 
USER=root ; COMMAND=/usr/sbin/rmmod hello_1 Nov 24 11:20:29 current_user kernel: Goodbye world 1. Nov 24 11:20:50 
current_user sudo[7160]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-1 ; USER=root ; 
COMMAND=/usr/bin/journalctl --since '1 hour ago'
```





#hello-1.c – простейший модуль ядра
#hello-2.c – демонстрация макросов module_init() и module_exit(). Этот вариант предпочтительнее использования 
             init_module() и cleanup_module().

##Шаги в Ubuntu 23.10:

1. Устанавливаем необходимые инструменты для сборки программ и управления модулями ядра на нашей системе:
    ```bash
    sudo apt-get install build-essential kmod
    ```
2. Отображаем информацию о загруженных модулях ядра в системе:

    a. С помощью команды lsmod, которая выводит отформатированный список модулей:
    ```bash
    sudo lsmod
   ```
    b. Читаем содержимое файла /proc/modules:
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
5. Создаем новый проект по пути - /home/current_user/develop/kernel/hello-2.

6. В корне проекта создаем файлы hello-1.c и hello-2.c.

7. В корне проекта создаем Makefile.

8. Переходим в нашу директорию проекта:
    ```bash
    cd /home/current_user/develop/kernel/hello-2
    ```
9. Используем make для компиляции кода:
    ```bash
    make
    ```
   
    Пример ввода и вывода:
    ```bash
    current_user@current_user:~/develop/kernel/hello-2$ make
    make -C /lib/modules/6.5.0-13-generic/build M=/home/current_user/develop/kernel/hello-2 modules
    make[1]: вход в каталог «/usr/src/linux-headers-6.5.0-13-generic»
    warning: the compiler differs from the one used to build the kernel
    The kernel was built by: aarch64-linux-gnu-gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
    You are using:           gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
    CC [M]  /home/current_user/develop/kernel/hello-2/hello-1.o
    CC [M]  /home/current_user/develop/kernel/hello-2/hello-2.o
    MODPOST /home/current_user/develop/kernel/hello-2/Module.symvers
    CC [M]  /home/current_user/develop/kernel/hello-2/hello-1.mod.o
    LD [M]  /home/current_user/develop/kernel/hello-2/hello-1.ko
    BTF [M] /home/current_user/develop/kernel/hello-2/hello-1.ko
    Skipping BTF generation for /home/current_user/develop/kernel/hello-2/hello-1.ko due to unavailability of vmlinux
    CC [M]  /home/current_user/develop/kernel/hello-2/hello-2.mod.o
    LD [M]  /home/current_user/develop/kernel/hello-2/hello-2.ko
    BTF [M] /home/current_user/develop/kernel/hello-2/hello-2.ko
    Skipping BTF generation for /home/current_user/develop/kernel/hello-2/hello-2.ko due to unavailability of vmlinux
    make[1]: выход из каталога «/usr/src/linux-headers-6.5.0-13-generic»
    ```

10. Получаем информацию о модуле modinfo hello-1.ko и modinfo hello-2.ko:
    ```bash
    current_user@current_user:~/develop/kernel/hello-2$ modinfo hello-1.ko
    filename:       /home/current_user/develop/kernel/hello-2/hello-1.ko
    license:        GPL
    srcversion:     6EEFF9BA2D82E6F0305588C
    depends:        
    name:           hello_1
    vermagic:       6.5.0-13-generic SMP preempt mod_unload modversions aarch64
    current_user@current_user:~/develop/kernel/hello-2$ modinfo hello-2.ko
    filename:       /home/current_user/develop/kernel/hello-2/hello-2.ko
    version:        0.1
    description:    A simple example Linux module.
    author:         Your Name
    license:        GPL
    srcversion:     682083FB93D95DEF7A501AC
    depends:        
    name:           hello_2
    vermagic:       6.5.0-13-generic SMP preempt mod_unload modversions aarch64
    ```
11. Убеждаемся, что модуль с именем "hello" не загружен:
    ```bash
    lsmod | grep hello
    ```
12. После успешной компиляции загружаем модули в ядро:
    ```bash
    sudo insmod hello-1.ko
    sudo insmod hello-2.ko
    ```
13. Проверяем загрузку модулей:
    ```bash
    lsmod | grep hello
    ```
    Пример вывода:
    ```bash
    hello_2                12288  0
    hello_1                12288  0
    ```
14. Для удаления модулей используется команда:
```bash
sudo rmmod hello-1
sudo rmmod hello-2
```
15. Это позволяет просмотреть системные логи, связанные с ядром Linux, и фильтрует строки, содержащие "kernel" - 
    sudo journalctl --since "1 hour ago" | grep kernel:
```bash
... ноя 24 11:14:42 current_user sudo[6353]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-1 ; 
USER=root ; COMMAND=/usr/bin/apt-get install build-essential kmodsudo apt-get install build-essential kmodsudo apt-get 
install build-essential kmodsudo apt-get install build-essential kmodsudo apt-get install build-essential kmodsudo 
apt-get install build-essential kmodsudo apt-get install build-essential kmodsudo apt-get install build-essential 
kmodsudo apt-get install build-essential kmodsudo apt-get install build-essential kmod ноя 24 11:14:53 current_user 
sudo[6362]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-1 ; USER=root ; 
COMMAND=/usr/bin/apt-get install build-essential kmod ноя 24 11:15:45 current_user sudo[6370]: current_user : TTY=pts/0 ;
 PWD=/home/current_user/develop/kernel/hello-1 ; USER=root ; COMMAND=/usr/bin/apt update ноя 24 11:16:01 current_user 
 sudo[6872]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-1 ; USER=root ; 
 COMMAND=/usr/bin/apt-get install linux-headers-6.5.0-13-generic ноя 24 11:17:10 current_user sudo[7119]: current_user : 
 TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-1 ; USER=root ; COMMAND=/usr/sbin/lsmod ноя 24 11:17:22 
 current_user sudo[7124]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-1 ; USER=root ; 
 COMMAND=/usr/sbin/insmod hello-1.ko ноя 24 11:17:22 current_user kernel: hello_1: loading out-of-tree module taints 
 kernel. ноя 24 11:17:22 current_user kernel: hello_1: module verification failed: signature and/or required key missing
  - tainting kernel ноя 24 11:17:22 current_user kernel: Hello world 1. ноя 24 11:18:27 current_user sudo[7137]: 
  current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-1 ; USER=root ; COMMAND=/usr/sbin/lsmod 
  ноя 24 11:20:29 current_user sudo[7153]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-1 ; 
  USER=root ; COMMAND=/usr/sbin/rmmod hello_1 ноя 24 11:20:29 current_user kernel: Goodbye world 1. ноя 24 11:20:50 
  current_user sudo[7160]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/hello-1 ; USER=root ; 
  COMMAND=/usr/bin/journalctl --since '1 hour ago' 
```
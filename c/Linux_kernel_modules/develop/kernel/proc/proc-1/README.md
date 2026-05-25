# procfs-1.h and procfs-1.c – this code demonstrates the creation, reading, and deletion of the /proc/helloworld file 
using the /proc file system in the Linux kernel.

## Steps on Ubuntu 23.10:

1. Install the necessary tools for building programs and managing kernel modules on our system:

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

3. Install the corresponding header files that may be needed for compiling kernel modules (for the current kernel 
   version) or other programs:

    ```bash
    sudo apt-get install linux-headers-$(uname -r)
    ```

4. Create a new project at the path - `/home/current_user/develop/kernel/proc/proc-1`.

5. In the project's root, create the file `procfs-1.c`.

6. In the project's root, create a `Makefile`.

7. Navigate to our project directory:

    ```bash
    cd /home/current_user/develop/kernel/proc/proc-1
    ```

8. Use `make` to compile the code:

    ```bash
    make
    ```

   Example input and output:

    ```bash
	current_user@current_user:~/develop/kernel/proc/proc-1$ make
	make -C /lib/modules/6.5.0-13-generic/build M=/home/current_user/develop/kernel/proc/proc-1 modules
	make[1]: Entering directory '/usr/src/linux-headers-6.5.0-13-generic'
	warning: the compiler differs from the one used to build the kernel
	  The kernel was built by: aarch64-linux-gnu-gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
	  You are using:           gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
	  CC [M]  /home/current_user/develop/kernel/proc/proc-1/procfs-1.o
	  MODPOST /home/current_user/develop/kernel/proc/proc-1/Module.symvers
	  CC [M]  /home/current_user/develop/kernel/proc/proc-1/procfs-1.mod.o
	  LD [M]  /home/current_user/develop/kernel/proc/proc-1/procfs-1.ko
	  BTF [M] /home/current_user/develop/kernel/proc/proc-1/procfs-1.ko
	Skipping BTF generation for /home/current_user/develop/kernel/proc/proc-1/procfs-1.ko due to unavailability of vmlinux
	make[1]: Leaving directory '/usr/src/linux-headers-6.5.0-13-generic'
    ```
9. Get information about the module:

    ```bash
	current_user@current_user:~/develop/kernel/proc/proc-1$ modinfo procfs-1.ko
	filename:       /home/current_user/develop/kernel/proc/proc-1/procfs-1.ko
	license:        GPL
	srcversion:     57BCBFA4CFE446C89E99C85
	depends:        
	name:           procfs_1
	vermagic:       6.5.0-13-generic SMP preempt mod_unload modversions aarch64
    ```

10. Ensure that the module named "procfs_1" is not loaded:

    ```bash
    sudo lsmod | grep procfs
    ```

11. After successful compilation, load the module into the kernel:

    ```bash
    sudo insmod procfs-1.ko
    ```

12. Check the module loading:

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-1$ sudo lsmod | grep procfs
	procfs_1               16384  0
    ```

13. Confirm the existence of the helloworld file in the system in the /proc directory.

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-1$ ls /proc/helloworld
	/proc/helloworld
    ```

14. Read the contents of the /proc/helloworld file:

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-1$ cat /proc/helloworld
    HelloWorld!
    ```

16. To remove the module, use the command:

    ```bash
    sudo rmmod proc-1
    ```

15. This allows you to view system logs related to the Linux kernel and filter lines containing "procfs" - sudo 
    journalctl --since "1 hour ago" | grep procfs:

    ```bash
	current_user@current_user:~/develop/kernel/proc/proc-1$ sudo journalctl --since "1 hour ago" | grep procfs
	Nov 30 14:16:47 current_user sudo[20207]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/proc/proc-1 
    ; USER=root ; COMMAND=/usr/sbin/insmod procfs-1.ko
	Nov 30 14:23:06 current_user sudo[20263]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/proc/proc-1 ; 
    USER=root ; COMMAND=/usr/sbin/rmmod procfs-1
    ```





# procfs-1.h и procfs-1.c – данный код демонстрирует создание, чтение и удаление файла /proc/helloworld с использованием 
файловой системы /proc в ядре Linux.

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

4. Создаем новый проект по пути - `/home/current_user/develop/kernel/proc/proc-1`.

5. В корне проекта создаем файлы `proc-1.c`.

6. В корне проекта создаем `Makefile`.

7. Переходим в нашу директорию проекта:

    ```bash
    cd /home/current_user/develop/kernel/proc/proc-1
    ```

8. Используем `make` для компиляции кода:

    ```bash
    make
    ```

    Пример ввода и вывода:

    ```bash
	current_user@current_user:~/develop/kernel/proc/proc-1$ make
	make -C /lib/modules/6.5.0-13-generic/build M=/home/current_user/develop/kernel/proc/proc-1 modules
	make[1]: вход в каталог «/usr/src/linux-headers-6.5.0-13-generic»
	warning: the compiler differs from the one used to build the kernel
	  The kernel was built by: aarch64-linux-gnu-gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
	  You are using:           gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
	  CC [M]  /home/current_user/develop/kernel/proc/proc-1/procfs-1.o
	  MODPOST /home/current_user/develop/kernel/proc/proc-1/Module.symvers
	  CC [M]  /home/current_user/develop/kernel/proc/proc-1/procfs-1.mod.o
	  LD [M]  /home/current_user/develop/kernel/proc/proc-1/procfs-1.ko
	  BTF [M] /home/current_user/develop/kernel/proc/proc-1/procfs-1.ko
	Skipping BTF generation for /home/current_user/develop/kernel/proc/proc-1/procfs-1.ko due to unavailability of vmlinux
	make[1]: выход из каталога «/usr/src/linux-headers-6.5.0-13-generic»
    ```
9. Получаем информацию о модуле:

    ```bash
	current_user@current_user:~/develop/kernel/proc/proc-1$ modinfo procfs-1.ko
	filename:       /home/current_user/develop/kernel/proc/proc-1/procfs-1.ko
	license:        GPL
	srcversion:     57BCBFA4CFE446C89E99C85
	depends:        
	name:           procfs_1
	vermagic:       6.5.0-13-generic SMP preempt mod_unload modversions aarch64
    ```

10. Убеждаемся, что модуль с именем "procfs_1" не загружен:

    ```bash
    sudo lsmod | grep procfs
    ```

11. После успешной компиляции загружаем модуль в ядро:

    ```bash
    sudo insmod procfs-1.ko
    ```

12. Проверяем загрузку модуля:

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-1$ sudo lsmod | grep procfs
	procfs_1               16384  0
    ```

13. Убеждаемся в наличии файла helloworld в системе в каталоге /proc.
	```bash
	current_user@current_user:~/develop/kernel/proc/proc-1$ ls /proc/helloworld
	/proc/helloworld
	```

14. Читаем содержимое файла /proc/helloworld:
	```bash
	current_user@current_user:~/develop/kernel/proc/proc-1$ cat /proc/helloworld
	HelloWorld!
	```

16. Для удаления модуля используется команда:

    ```bash
    sudo rmmod proc-1
    ```

15. Это позволяет просмотреть системные логи, связанные с ядром Linux, и фильтрует строки, содержащие "procfs" - 
    sudo journalctl --since "1 hour ago" | grep procfs:

    ```bash
	current_user@current_user:~/develop/kernel/proc/proc-1$ sudo journalctl --since "1 hour ago" | grep procfs
	ноя 30 14:16:47 current_user sudo[20207]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/proc/proc-1 
    ; USER=root ; COMMAND=/usr/sbin/insmod procfs-1.ko
	ноя 30 14:23:06 current_user sudo[20263]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/proc/proc-1 ; 
    USER=root ; COMMAND=/usr/sbin/rmmod procfs-1
     ```

# procfs-2.h and procfs-2.c – this code demonstrates the creation, reading, and deletion of the /proc/helloworld file 
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

4. Create a new project at the path - `/home/current_user/develop/kernel/proc/proc-2`.

5. In the project's root, create the files `procfs-2.h` and `procfs-2.c`.

6. In the project's root, create a `Makefile`.

7. Navigate to our project directory:

    ```bash
    cd /home/current_user/develop/kernel/proc/proc-2
    ```

8. Use `make` to compile the code:

    ```bash
    make
    ```

   Example input and output:

    ```bash
	current_user@current_user:~/develop/kernel/proc/proc-2$ make
	make -C /lib/modules/6.5.0-13-generic/build M=/home/current_user/develop/kernel/proc/proc-2 modules
	make[1]: Entering directory '/usr/src/linux-headers-6.5.0-13-generic'
	warning: the compiler differs from the one used to build the kernel
	  The kernel was built by: aarch64-linux-gnu-gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
	  You are using:           gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
	  CC [M]  /home/current_user/develop/kernel/proc/proc-2/procfs-2.o
	  MODPOST /home/current_user/develop/kernel/proc/proc-2/Module.symvers
	  CC [M]  /home/current_user/develop/kernel/proc/proc-2/procfs-2.mod.o
	  LD [M]  /home/current_user/develop/kernel/proc/proc-2/procfs-2.ko
	  BTF [M] /home/current_user/develop/kernel/proc/proc-2/procfs-2.ko
	Skipping BTF generation for /home/current_user/develop/kernel/proc/proc-2/procfs-2.ko due to unavailability of vmlinux
	make[1]: Leaving directory '/usr/src/linux-headers-6.5.0-13-generic'
    ```
9. Get information about the module:

    ```bash
	current_user@current_user:~/develop/kernel/proc/proc-2$ modinfo procfs-2.ko
	filename:       /home/current_user/develop/kernel/proc/proc-2/procfs-2.ko
	license:        GPL
	srcversion:     EE16E84C45661D7CE1E9C19
	depends:        
	name:           procfs_2
	vermagic:       6.5.0-13-generic SMP preempt mod_unload modversions aarch64
    ```

10. Ensure that the module named "procfs_2" is not loaded:

    ```bash
    sudo lsmod | grep procfs
    ```

11. After successful compilation, load the module into the kernel:

    ```bash
    sudo insmod procfs-2.ko
    ```

12. Check the module loading:

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-2$ sudo lsmod | grep procfs
	procfs_2               16384  0
    ```

13. Confirm the existence of the Helloworld! file in the system in the /proc directory.

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-2$ ls /proc/buffer1k
	/proc/buffer1k
    ```

14. Read the contents of the file cat /proc/buffer1k:

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-2$ cat /proc/buffer1k
    HelloWorld!
    ```

15. In this step, an attempt is made to write a new value ("NewValue") to the /proc/buffer1k file. This operation uses 
    the tee command, which first outputs data to standard output and then writes it to the specified file. After 
    executing the command, the new value itself is output.

    ```bash
    echo "NewValue" | sudo tee /proc/buffer1k
    NewValue
    ```

16. Read the contents of the /proc/buffer1k file using the cat command. However, the result shows the old value 
    ("HelloWorld!"), not "NewValue".

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-2$ cat /proc/buffer1k
    HelloWorld!
    ```

    ### Explanation:
    When we write data to the /proc/buffer1k file, it is processed by our kernel module procfs-2. Our code in the 
    procfile_write function copies data from user space to the procfs_buffer. However, the code in the procfile_read 
    function, when reading from the /proc/buffer1k file, uses the hard-coded string "HelloWorld!\n" instead of the 
    procfs_buffer. This is why we see the old value when reading.

17. To remove the module, use the command:

    ```bash
    sudo rmmod procfs-2
    ```

18. This allows you to view system logs related to the Linux kernel and filter lines containing "procfs" - sudo 
    journalctl --since "1 hour ago" | grep procfs:

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-2$ sudo journalctl --since "1 hour ago" | grep "procfs"
    Dec 01 14:41:01 shrekulka sudo[29619]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/proc/proc-2 ;
    USER=root ; COMMAND=/usr/sbin/insmod procfs-2.ko
    Dec 01 14:57:23 shrekulka sudo[29795]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/proc/proc-2 ;
    USER=root ; COMMAND=/usr/sbin/rmmod procfs-2
    ```





# procfs-2.h и procfs-2.c – данный код демонстрирует создание, чтение и удаление файла /proc/helloworld с использованием
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

4. Создаем новый проект по пути - `/home/current_user/develop/kernel/proc/proc-2`.

5. В корне проекта создаем файлы `procfs-2.h` и `procfs-2.c`.

6. В корне проекта создаем `Makefile`.

7. Переходим в нашу директорию проекта:

    ```bash
    cd /home/current_user/develop/kernel/proc/proc-2
    ```

8. Используем `make` для компиляции кода:

    ```bash
    make
    ```

   Пример ввода и вывода:

    ```bash
	current_user@current_user:~/develop/kernel/proc/proc-2$ make
	make -C /lib/modules/6.5.0-13-generic/build M=/home/current_user/develop/kernel/proc/proc-2 modules
	make[1]: вход в каталог «/usr/src/linux-headers-6.5.0-13-generic»
	warning: the compiler differs from the one used to build the kernel
	  The kernel was built by: aarch64-linux-gnu-gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
	  You are using:           gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
	  CC [M]  /home/current_user/develop/kernel/proc/proc-2/procfs-2.o
	  MODPOST /home/current_user/develop/kernel/proc/proc-2/Module.symvers
	  CC [M]  /home/current_user/develop/kernel/proc/proc-2/procfs-2.mod.o
	  LD [M]  /home/current_user/develop/kernel/proc/proc-2/procfs-2.ko
	  BTF [M] /home/current_user/develop/kernel/proc/proc-2/procfs-2.ko
	Skipping BTF generation for /home/current_user/develop/kernel/proc/proc-2/procfs-2.ko due to unavailability of vmlinux
	make[1]: выход из каталога «/usr/src/linux-headers-6.5.0-13-generic»
    ```
9. Получаем информацию о модуле:

    ```bash
	current_user@current_user:~/develop/kernel/proc/proc-2$ modinfo procfs-2.ko
	filename:       /home/current_user/develop/kernel/proc/proc-2/procfs-2.ko
	license:        GPL
	srcversion:     EE16E84C45661D7CE1E9C19
	depends:        
	name:           procfs_2
	vermagic:       6.5.0-13-generic SMP preempt mod_unload modversions aarch64
    ```

10. Убеждаемся, что модуль с именем "procfs_2" не загружен:

    ```bash
    sudo lsmod | grep procfs
    ```

11. После успешной компиляции загружаем модуль в ядро:

    ```bash
    sudo insmod procfs-2.ko
    ```

12. Проверяем загрузку модуля:

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-2$ sudo lsmod | grep procfs
	procfs_2               16384  0
    ```

13. Убеждаемся в наличии файла Helloworld! в системе в каталоге /proc.
    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-2$ ls /proc/buffer1k
	/proc/buffer1k
    ```

14. Читаем содержимое файла cat /proc/buffer1k:
    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-2$ cat /proc/buffer1k
    HelloWorld!
    ```
15. В данном шаге происходит попытка записи нового значения ("NewValue") в файл /proc/buffer1k. Эта операция использует 
    команду tee, которая сначала выводит данные в стандартный вывод, а затем их записывает в указанный файл. После 
    выполнения команды выводится само новое значение.
	```bash
	echo "NewValue" | sudo tee /proc/buffer1k
	NewValue
	```

16. Читаем содержимое файла /proc/buffer1k с помощью команды cat. Однако, результат показывает старое значение 	   
    ("HelloWorld!"), а не "NewValue".
    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-2$ cat /proc/buffer1k
    HelloWorld!
    ```
    ### Пояснение:
	Когда мы записываем данные в файл /proc/buffer1k, они обрабатываются нашим ядерным модулем procfs-2. Наш код в 
    функции procfile_write копирует данные из пользовательского пространства в буфер procfs_buffer. Однако, код в функции
    procfile_read при чтении из файла /proc/buffer1k вместо буфера procfs_buffer жестко закодированной строки 
    "HelloWorld!\n". Именно поэтому при чтении мы видим старое значение.

17. Для удаления модуля используется команда:

    ```bash
    sudo rmmod procfs-2
    ```

18. Это позволяет просмотреть системные логи, связанные с ядром Linux, и фильтрует строки, содержащие "procfs" -
    sudo journalctl --since "1 hour ago" | grep procfs:

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-2$ sudo journalctl --since "1 hour ago" | grep "procfs"
    дек 01 14:41:01 shrekulka sudo[29619]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/proc/proc-2 ;
    USER=root ; COMMAND=/usr/sbin/insmod procfs-2.ko
    дек 01 14:57:23 shrekulka sudo[29795]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/proc/proc-2 ;
    USER=root ; COMMAND=/usr/sbin/rmmod procfs-2
    ```

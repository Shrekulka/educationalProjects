# Step-by-Step Guide to Creating a Device Driver with ioctl in Linux

## Steps in Ubuntu 23.10:

### Step I. Install necessary tools for program compilation and kernel module management on our system:

    ```bash
    sudo apt-get install build-essential kmod
    ```

### Step II. Update the package list (apt update) and upgrade the system (full-upgrade or dist-upgrade):

    ```bash
    sudo apt update && full-upgrade
    ```
    or
    ```bash
    sudo apt update && dist-upgrade
    ```

### Step III. Install corresponding header files that may be required for kernel module compilation (for the current 
    kernel version) or other programs:

    ```bash
    sudo apt-get install linux-headers-$(uname -r)
    ```

### Step IV. Create a new project at the path - /home/current_user/develop/kernel/dev/chardev/ioctl.
### Step V. In the project root, create files ioctl.h and ioctl.c.
### Step VI. In the project root, create a Makefile.
### Step VII. Navigate to our project directory:

    ```bash
    cd /home/current_user/develop/kernel/dev/chardev/ioctl
    ```

### Step VIII. Use make to compile the code:

    ```bash
    make
    ```

Example input and output:

    ```bash
    current_user@current_user:~/develop/kernel/dev/chardev/ioctl$ sudo make
    make -C /lib/modules/6.5.0-14-generic/build M=/home/current_user/develop/kernel/dev/chardev/ioctl modules
    make[1]: Entering directory '/usr/src/linux-headers-6.5.0-14-generic'
    warning: the compiler differs from the one used to build the kernel
    The kernel was built by: aarch64-linux-gnu-gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
    You are using:           gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
    CC [M]  /home/current_user/develop/kernel/dev/chardev/ioctl/ioctl.o
    MODPOST /home/current_user/develop/kernel/dev/chardev/ioctl/Module.symvers
    CC [M]  /home/current_user/develop/kernel/dev/chardev/ioctl/ioctl.mod.o
    LD [M]  /home/current_user/develop/kernel/dev/chardev/ioctl/ioctl.ko
    BTF [M] /home/current_user/develop/kernel/dev/chardev/ioctl/ioctl.ko
    Skipping BTF generation for /home/current_user/develop/kernel/dev/chardev/ioctl/ioctl.ko due to unavailability of vmlinux
    make[1]: Leaving directory '/usr/src/linux-headers-6.5.0-14-generic'
    ```

### Step IX. Get information about the module:

    ```bash
    current_user@current_user:~/develop/kernel/dev/chardev/ioctl$ modinfo ioctl.ko
    filename:       /home/shrekulka/develop/kernel/dev/chardev/ioctl/ioctl.ko
    description:    This is test_ioctl module
    license:        GPL
    srcversion:     BCB7E03A5FBB82FC6C1B85D
    depends:        
    name:           ioctl
    vermagic:       6.5.0-14-generic SMP preempt mod_unload modversions aarch64
    ```

### Step X. Ensure that the module named "ioctl" is not loaded:

    ```bash
    sudo lsmod | grep ioctl
    ```

### Step XI. After successful compilation, load the module into the kernel:

    ```bash
    sudo insmod ioctl.ko
    ```

### Step XII. Verify the module loading:

    ```bash
    current_user@current_user:~/develop/kernel/dev/chardev/ioctl$ sudo lsmod | grep ioctl
    ioctl               20480  0
    ```

### Step XIII. The command `sudo mknod /dev/ioctltest c 510 0` creates a device node `/dev/ioctltest` for accessing our 
driver:

- `/dev/ioctltest` - the path to the created device node
- `c` - indicates that we are creating a character device
- `510` - is the MAJOR number of our device, assigned by the kernel during `init_module()`
- `0` - is the MINOR number of the device. In our case, we created only one device with a minor number of 0

Thus, `mknod` creates the interface `/dev/ioctltest` for interacting with the ioctl driver.

User-space programs can access this device, perform read/write operations (like a regular file), and send ioctl commands.
All these calls go to the kernel handlers in our driver.

This step registers the device node in the file system. After this, programs can open `/dev/ioctltest` and interact with
our driver as with a device.

Now, let's examine the contents of the /dev directory with subsequent filtering of the output to find an entry associated
with the ioctltest device.

    ```bash
    current_user@current_user:~/develop/kernel/dev/chardev/ioctl$ ls /dev | grep ioctltest
    ioctltest
    ```

###### Here's an explanation of the command components:
- ls /dev: Displays the list of contents in the /dev directory.
- |: The pipe operator, which takes the output of the command on the left and uses it as input for the command on the 
  right.
- grep ioctltest: Searches for lines containing the text "ioctltest" in the output.
The output indicates whether a device with the name ioctltest exists in the /dev directory. In this case, the presence of
the entry confirms the successful creation of the device node and its availability for interaction with the kernel module.

##### Let's break down step 13 when using IOCTL operations in our driver:
1. The user program makes an ioctl system call, specifying the file descriptor of our device (e.g., `/dev/ioctltest`) 
   and IOCTL command parameters.
2. The call goes to the file operations (`file_operations`) of our driver, specifically to the `ioctl()` method.
3. Control is then passed to the `test_ioctl_ioctl()` function, which is the IOCTL command handler in our driver.
4. In the `test_ioctl_ioctl()` function, the IOCTL command is recognized and processed using a switch-case statement. 

For example:

    ```bash
    switch(cmd)
    {
        case IOCTL_VALSET:
        // set a value in the driver
        break;
    
        case IOCTL_VALGET:
        // get a value from the driver
        break;
    }
    ```

5. The `test_ioctl_data` structure is used to access the driver's data. Access is synchronized using the `rwlock_t lock`.
6. After handling the command, control returns to the file operations `ioctl()` method.
7. The result of the IOCTL command is returned to the calling process.

Thus, when calling `ioctl()` from user space, control is transferred to file operations and the IOCTL handler in the 
kernel, which interacts with the driver's data.

##### Let's look at examples of main IOCTL commands for the driver and their corresponding numbers defined in the code:
In the driver code, commands are defined as:

    ```bash
    #define IOCTL_VALSET _IOW(IOC_MAGIC, 0, struct ioctl_arg)  
    #define IOCTL_VALGET _IOR(IOC_MAGIC, 1, struct ioctl_arg)
    #define IOCTL_VALSET_NUM _IOW(IOC_MAGIC, 2, int)
    #define IOCTL_VALGET_NUM _IOR(IOC_MAGIC, 3, int)
    ```

###### These commands correspond to the numbers:
1. IOCTL_VALSET - set value - number 0
2. IOCTL_VALGET - get value - number 1
3. IOCTL_VALSET_NUM - set numeric value - number 2
4. IOCTL_VALGET_NUM - get numeric value - number 3

0, 1, 2, 3 are arbitrarily chosen command numbers.

##### Examples of usage:

1. Setting the value to 15:

    ```bash
    sudo bash -c 'echo 0 15 > /dev/ioctltest'
    ```

   Here, the number 0 corresponds to IOCTL_VALSET. The value 15 is stored in the `val` field of the `ioctl_arg` 
   structure, which is of type unsigned int.
   The IOCTL_VALSET command uses a structure to pass data:

    ```bash
    struct ioctl_arg
    {
    unsigned int val;  
    }
    ```

   This means that with the IOCTL_VALSET command, we can set 32-bit unsigned integers (unsigned int) in the `val` field 
   of this structure.

2. Getting the current value:

    ```bash
    sudo cat /dev/ioctltest
    ```

   Here, the sequence of actions is:

   a) The `cat` command reads the contents of the file `/dev/ioctltest` and outputs it to the standard output (terminal).
   b) Thus, `cat` reads the value from the `val` variable in the driver and outputs it to the terminal.
   c) This allows obtaining the current value from the driver without using ioctl commands.

   Reading data and passing it to the application at the kernel level

   To read data from the driver and pass it to the user-level application at the kernel level, the following commands 
   are used:

    ```bash
    #define IOCTL_VALGET _IOR(IOC_MAGIC, 1, struct ioctl_arg)
    #define IOCTL_VALGET_NUM _IOR(IOC_MAGIC, 3, int)
    ```

   IOCTL_VALGET (command 1) reads the value from the `ioctl_arg` structure.
   IOCTL_VALGET_NUM (command 3) reads a numeric value of type int.
   Then data is copied to user space using `copy_to_user()`.
   Thus, these ioctl commands allow transferring data from the driver to the low-level kernel application.

3. Setting the number to 10:

    ```bash
    sudo bash -c 'echo 2 10 > /dev/ioctltest'
    ```

   Here, in the command, we specify the number 2, corresponding to IOCTL_VALSET_NUM. The value 10 will be converted to 
   the integer type int and stored in the driver, as it accepts int.

    ```bash
    #define IOCTL_VALSET_NUM _IOW(IOC_MAGIC, 2, int)
    ```

#### In our case, attempting to write to this device with echo commands results in an error:

    ```bash
    sudo bash -c 'echo 0 15 > /dev/ioctltest'
    ```

bash: line 1: echo: write error: Invalid argument.
This is normal since the driver does not yet support writing, only reading and ioctl.
When opening /dev/ioctltest, open/close driver calls are logged:

    ```bash
    test_ioctl_open call.
    test_ioctl_close call.
    ```

Thus, the basic functionality of the driver works - loading/unloading the module, creating a device, handling open/close.

#### Explanation about the test_ioctl_data structure and the purpose of some macros.

So, the `test_ioctl_data` structure is used to store data that our device, implemented as a driver, works with.

It contains two fields:
1. `val`
   This is the value that we can control through IOCTL commands. For example, set it with IOCTL_VALSET or 
   IOCTL_VALSET_NUM. And read it with IOCTL_VALGET.
   This is some "state" of our device implemented in the driver.

2. `lock`
   This is a lock for synchronizing access to the `val` field from different threads. Since the Linux kernel is 
   multi-threaded, without this lock, simultaneous access could cause problems and data corruption.
   Therefore, reading-modifying the `val` field happens only inside the lock using read/write lock for synchronization. 
   This ensures data integrity.

#### Now about some macros:

1. `IOC_MAGIC` – this is a magic number (ours is \x66) by which the Linux kernel determines that the IOCTL command is 
   intended specifically for our driver. Without this command number, IOCTL commands simply won't be processed.
   This is done to prevent IOCTL commands from different drivers conflicting with each other.

2. `IOCTL_VAL_MAXNR` - this macro defines the maximum IOCTL command number supported by your driver. This macro is used 
   in the Linux kernel to ensure correct processing of IOCTL commands for your driver.
   Why it's needed: When a request to execute an IOCTL command comes in, the kernel uses the command number (cmd) passed
   to the ioctl function to determine which operation to perform. The IOCTL_VAL_MAXNR macro serves as a limiter for 
   command numbers. It tells the kernel that your driver supports commands with numbers from 0 to IOCTL_VAL_MAXNR.

   Example usage: In this case, our driver supports four commands:

    ```bash
    #define IOCTL_VALSET _IOW(IOC_MAGIC, 0, struct ioctl_arg)  
    #define IOCTL_VALGET _IOR(IOC_MAGIC, 1, struct ioctl_arg)
    #define IOCTL_VALSET_NUM _IOW(IOC_MAGIC, 2, int)
    #define IOCTL_VALGET_NUM _IOR(IOC_MAGIC, 3, int)
    ```

   Then `IOCTL_VAL_MAXNR` should be set to 3 (from 0 to 3 inclusive) – four commands.

    ```bash
    #define IOCTL_VAL_MAXNR 3
    ```

3. `DRIVER_NAME` - Defines the name of your driver. This is used when registering the device.

### Step XIV. Unloading the Kernel Module and Removing Character Device Nodes:

    ```bash
    sudo rmmod ioctl
    sudo rm /dev/ioctltest
    ```

### Step XV. Checking System Logs to Ensure the Module was Successfully Unloaded:
    ```bash
    current_user@current_user:/develop/kernel/dev/chardev/ioctl$ sudo journalctl --since "1 hour ago" | grep "ioctltest"
    Dec 12 19:26:54 current_user kernel: ioctltest driver removed.
    Dec 12 19:27:06 current_user sudo[28872]: current_user : TTY=pts/0 ; PWD=/home/current_user/.local/share/Trash/files/ioctl ; 
USER=root ; COMMAND=/usr/bin/rm /dev/ioctltest
    current_user@current_user:/develop/kernel/dev/chardev/ioctl$ sudo journalctl --since "1 hour ago" | grep "ioctl"
    Dec 12 19:26:54 current_user sudo[28866]: current_user : TTY=pts/0 ; PWD=/home/current_user/.local/share/Trash/files/ioctl ; 
USER=root ; COMMAND=/usr/sbin/rmmod ioctl
    Dec 12 19:26:54 current_user kernel: ioctltest driver removed.
    Dec 12 19:27:06 current_user sudo[28872]: current_user : TTY=pts/0 ; PWD=/home/current_user/.local/share/Trash/files/ioctl ; 
USER=root ; COMMAND=/usr/bin/rm /dev/ioctltest
    Dec 12 19:27:12 current_user sudo[28875]: current_user : TTY=pts/0 ; PWD=/home/current_user/.local/share/Trash/files/ioctl ; 
USER=root ; COMMAND=/usr/sbin/lsmod
    Dec 12 19:38:16 current_user sudo[28986]: current_user : TTY=pts/0 ; PWD=/home/current_user/.local/share/Trash/files/ioctl ; 
USER=root ; COMMAND=/usr/sbin/lsmod
    Dec 12 19:38:28 current_user sudo[28990]: current_user : TTY=pts/0 ; PWD=/home/current_user/.local/share/Trash/files/ioctl ; 
USER=root ; COMMAND=/usr/bin/journalctl --since '1 hour ago'
    Dec 12 19:38:41 current_user sudo[28995]: current_user : TTY=pts/0 ; PWD=/home/current_user/.local/share/Trash/files/ioctl ; 
USER=root ; COMMAND=/usr/bin/journalctl --since '1 hour ago'
    current_user@current_user:/develop/kernel/dev/chardev/ioctl$ sudo dmesg | grep ioctltest
    [ 3470.349448] ioctltest driver(major: 510) installed.
    [ 3881.650341] ioctltest driver removed.
    [ 4402.422718] ioctltest driver(major: 510) installed.
    [ 6511.538812] ioctltest driver removed.
    [100806.994287] ioctltest driver(major: 510) installed.
    [109686.205333] ioctltest driver removed.
    [109839.657702] ioctltest driver(major: 510) installed.
    [135289.520975] ioctltest driver removed.
    [135659.767446] ioctltest driver(major: 510) installed.
    [136747.096903] ioctltest driver removed.
    [137368.935906] ioctltest driver(major: 510) installed.
    [146429.866113] ioctltest driver removed.
    [151753.294087] ioctltest driver(major: 510) installed.
    [155093.188677] ioctltest driver removed.
    current_user@current_user:/develop/kernel/dev/chardev/ioctl$ sudo dmesg | grep ioctl
    [ 0.088567] device-mapper: ioctl: 4.48.0-ioctl (2023-03-01) initialised: dm-devel@redhat.com
    [ 3470.348093] ioctl: loading out-of-tree module taints kernel.
    [ 3470.348143] ioctl: module verification failed: signature and/or required key missing - tainting kernel
    [ 3470.349448] ioctltest driver(major: 510) installed.
    [ 3624.045472] test_ioctl_open call.
    [ 3624.048356] test_ioctl_close call.
    [ 3673.803562] test_ioctl_open call.
    [ 3673.804132] test_ioctl_close call.
    [ 3793.446842] test_ioctl_open call.
    [ 3812.352249] test_ioctl_close call.
    [ 3881.650341] ioctltest driver removed.
    [ 4402.422718] ioctltest driver(major: 510) installed.
    [ 6511.538812] ioctltest driver removed.
    [100806.994287] ioctltest driver(major: 510) installed.
    [109686.205333] ioctltest driver removed.
    [109839.657702] ioctltest driver(major: 510) installed.
    [110204.447385] test_ioctl_open call.
    [110204.449016] test_ioctl_close call.
    [110448.164679] test_ioctl_open call.
    [110448.165143] test_ioctl_close call.
    [111563.265989] test_ioctl_open call.
    [111563.266297] test_ioctl_close call.
    [111646.883354] test_ioctl_open call.
    [114061.912741] test_ioctl_open call.
    [114061.913295] test_ioctl_close call.
    [114116.230858] test_ioctl_open call.
    [114116.231180] test_ioctl_close call.
    [135277.079326] test_ioctl_close call.
    [135289.520975] ioctltest driver removed.
    [135659.767446] ioctltest driver(major: 510) installed.
    [135915.258723] test_ioctl_open call.
    [135915.259156] test_ioctl_close call.
    [135944.323678] test_ioctl_open call.
    [135944.323918] test_ioctl_close call.
    [136076.117777] test_ioctl_open call.
    [136076.118239] test_ioctl_close call.
    [136258.092553] test_ioctl_open call.
    [136258.093213] test_ioctl_close call.
    [136289.768766] test_ioctl_open call.
    [136296.148247] test_ioctl_close call.
    [136347.479834] test_ioctl_open call.
    [136347.480312] test_ioctl_close call.
    [136356.369914] test_ioctl_open call.
    [136356.370208] test_ioctl_close call.
    [136367.289870] test_ioctl_open call.
    [136367.290283] test_ioctl_close call.
    [136413.795763] test_ioctl_open call.
    [136413.796128] test_ioctl_close call.
    [136462.390742] test_ioctl_open call.
    [136462.391267] test_ioctl_close call.
    [136747.096903] ioctltest driver removed.
    [137368.935906] ioctltest driver(major: 510) installed.
    [137444.605300] test_ioctl_open call.
    [137444.605603] test_ioctl_close call.
    [137460.258473] test_ioctl_open call.
    [137460.258792] test_ioctl_close call.
    [137479.896868] test_ioctl_open call.
    [137479.897331] test_ioctl_close call.
    [138724.039400] test_ioctl_open call.
    [138724.039760] test_ioctl_close call.
    [138864.709790] test_ioctl_open call.
    [138864.710361] test_ioctl_close call.
    [139072.267044] test_ioctl_open call.
    [139072.267561] test_ioctl_close call.
    [142097.607794] test_ioctl_open call.
    [142097.608029] test_ioctl_close call.
    [142142.685122] test_ioctl_open call.
    [142142.685602] test_ioctl_close call.
    [142196.710044] test_ioctl_open call.
    [142196.710284] test_ioctl_close call.
    [142743.958100] test_ioctl_open call.
    [142743.958724] test_ioctl_close call.
    [146429.866113] ioctltest driver removed.
    [151753.294087] ioctltest driver(major: 510) installed.
    [151885.751317] test_ioctl_open call.
    [151885.751747] test_ioctl_close call.
    [151911.457129] test_ioctl_open call.
    [151911.457711] test_ioctl_close call.
    [155093.188677] ioctltest driver removed.
    ```
These steps provide the main process for building, loading, and testing our Linux kernel module providing an IOCTL 
interface.






# Пошаговое руководство по созданию драйвера устройства с ioctl в Linux

## Шаги в Ubuntu 23.10:

### Шаг I. Устанавливаем необходимые инструменты для сборки программ и управления модулями ядра на нашей системе:

    ```bash
    sudo apt-get install build-essential kmod
    ```

### Шаг II. Обновляем список пакетов (apt update) и обновляем систему (full-upgrade или dist-upgrade):

    ```bash
    sudo apt update && full-upgrade
    ```

или

    ```bash
    sudo apt update && dist-upgrade
    ```

### Шаг III. Устанавливаем соответствующие заголовочные файлы, которые могут быть необходимы для компиляции модулей ядра
         (для текущей версии ядра) или других программ:

    ```bash
    sudo apt-get install linux-headers-$(uname -r)
    ```

### Шаг IV. Создаем новый проект по пути - `/home/current_user/develop/kernel/dev/chardev/ioctl`.

### Шаг V. В корне проекта создаем файлы `ioctl.h` и `ioctl.c`.

### Шаг VI. В корне проекта создаем `Makefile`.

### Шаг VII. Переходим в нашу директорию проекта:

    ```bash
    cd /home/current_user/develop/kernel/dev/chardev/ioctl
    ```

### Шаг VIII. Используем `make` для компиляции кода:

    ```bash
    make
    ```

Пример ввода и вывода:

    ```bash
    current_user@current_user:~/develop/kernel/dev/chardev/ioctl$ sudo make
    make -C /lib/modules/6.5.0-14-generic/build M=/home/current_user/develop/kernel/dev/chardev/ioctl modules
    make[1]: вход в каталог «/usr/src/linux-headers-6.5.0-14-generic»
    warning: the compiler differs from the one used to build the kernel
    The kernel was built by: aarch64-linux-gnu-gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
    You are using:           gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
    CC [M]  /home/current_user/develop/kernel/dev/chardev/ioctl/ioctl.o
    MODPOST /home/current_user/develop/kernel/dev/chardev/ioctl/Module.symvers
    CC [M]  /home/current_user/develop/kernel/dev/chardev/ioctl/ioctl.mod.o
    LD [M]  /home/current_user/develop/kernel/dev/chardev/ioctl/ioctl.ko
    BTF [M] /home/current_user/develop/kernel/dev/chardev/ioctl/ioctl.ko
    Skipping BTF generation for /home/current_user/develop/kernel/dev/chardev/ioctl/ioctl.ko due to unavailability of vmlinux
    make[1]: выход из каталога «/usr/src/linux-headers-6.5.0-14-generic»
    ```

### Шаг IX.	Получаем информацию о модуле:

    ```bash
    current_user@current_user:~/develop/kernel/dev/chardev/ioctl$ modinfo ioctl.ko
    filename:       /home/shrekulka/develop/kernel/dev/chardev/ioctl/ioctl.ko
    description:    This is test_ioctl module
    license:        GPL
    srcversion:     BCB7E03A5FBB82FC6C1B85D
    depends:        
    name:           ioctl
    vermagic:       6.5.0-14-generic SMP preempt mod_unload modversions aarch64
    ```

### Шаг X. Убеждаемся, что модуль с именем "ioctl" не загружен:

    ```bash
    sudo lsmod | grep ioctl
    ```

### Шаг XI. После успешной компиляции загружаем модуль в ядро:

    ```bash
    sudo insmod ioctl.ko
    ```

### Шаг XII. Проверяем загрузку модуля:

    ```bash
    current_user@current_user:~/develop/kernel/dev/chardev/ioctl$ sudo lsmod | grep ioctl
    ioctl               20480  0
    ```

### Шаг XIII. Команда sudo mknod /dev/ioctltest c 510 0 создает узел устройства (device node) /dev/ioctltest для доступа
к нашему драйверу:

•	/dev/ioctltest - путь к создаваемому узлу устройства
•	c - указывает, что мы создаём символьное (character) устройство
•	510 - это MAJOR номер нашего устройства, который назначается ядром при init_module()
•	0 - это MINOR номер устройства. В нашем случае мы создали только одно устройство с минорным номером 0

Таким образом, mknod создаёт интерфейс /dev/ioctltest для взаимодействия с драйвером ioctl.

Программы в userspace могут обращаться к этому устройству, выполнять read/write (как через обычный файл), так и 
отправлять команды ioctl. Все эти вызовы попадают в обработчики ядра в нашем драйвере.

Данный шаг регистрирует узел устройства в файловой системе. После чего программы могут открывать /dev/ioctltest и 
работать с нашим драйвером как с устройством.

Теперь просмотрим содержимоt каталога /dev с последующим фильтрованием вывода для поиска записи, связанной с 
устройством ioctltest. 

    ```bash
    current_user@current_user:~/develop/kernel/dev/chardev/ioctl$ ls /dev | grep ioctltest
    ioctltest
    ```
###### Вот объяснение компонентов команды:

- ls /dev: Выводит список содержимого каталога /dev.
- |: Оператор конвейера, который берет вывод команды слева и использует его в качестве входных данных для команды справа.
- grep ioctltest: Ищет строки, содержащие текст "ioctltest" в выводе.

Вывод указывает на то, существует ли устройство с именем ioctltest в каталоге /dev. В данном случае наличие записи 
подтверждает успешное создание узла устройства и его доступность для взаимодействия с модулем ядра.

##### Разберем пошагово, что происходит в шаге 13 при использовании операций IOCTL в нашем драйвере:
1.	Пользовательская программа выполняет системный вызов ioctl(), указывая файловый дескриптор нашего устройства 
    (например, /dev/ioctltest) и параметры команды IOCTL.
2.	Вызов попадает в файловые операции (file_operations) нашего драйвера, в частности в метод ioctl().
3.	Далее управление передается в функцию test_ioctl_ioctl(), которая является обработчиком команд IOCTL в нашем драйвере.
4.	В функции test_ioctl_ioctl() происходит распознавание и обработка команды IOCTL с помощью switch-case. 
    Например:

    ```bash
    switch(cmd)
    {
        case IOCTL_VALSET:
        // установка значения в драйвер
        break;
    
        case IOCTL_VALGET:
        // получение значения из драйвера
        break;
    }
    ```

5.	Для доступа к данным драйвера используется структура test_ioctl_data. Доступ синхронизируется с помощью блокировки 
    rwlock_t lock.
6.	По завершению обработки команды управление возвращается обратно в метод ioctl() файловых операций.
7.	Результат команды IOCTL возвращается вызвавшему процессу.

Таким образом, при вызове ioctl() из пользовательского пространства происходит передача управления в файловые операции и
обработчик IOCTL в ядре, который взаимодействует с данными драйвера.

##### Давайте рассмотрим примеры основных команд IOCTL для драйвера и как им соответствуют номера:
В коде драйвера определены команды:

    ```bash
    #define IOCTL_VALSET _IOW(IOC_MAGIC, 0, struct ioctl_arg)  
    #define IOCTL_VALGET _IOR(IOC_MAGIC, 1, struct ioctl_arg)
    #define IOCTL_VALSET_NUM _IOW(IOC_MAGIC, 2, int)
    #define IOCTL_VALGET_NUM _IOR(IOC_MAGIC, 3, int)
    ```

###### Этим командам соответствуют номера:
1.	IOCTL_VALSET - установить значение - номер 0
2.	IOCTL_VALGET - получить значение - номер 1
3.	IOCTL_VALSET_NUM - установить числовое значение - номер 2
4.	IOCTL_VALGET_NUM - получить числовое значение - номер 3

0, 1, 2, 3 - произвольно выбранные номера команд.

##### Примеры вызова:

1. Установка значения 15:

    ```bash
    sudo bash -c 'echo 0 15 > /dev/ioctltest'
    ```
   
    Тут номер 0 - это IOCTL_VALSET. А значение 15 сохраняется в поле val структуры ioctl_arg, имеющего тип unsigned int.
    В команде IOCTL_VALSET используется структура для передачи данных:

    ```bash
    struct ioctl_arg
    {
    unsigned int val;  
    };
    ```
   
    Это означает, что с помощью команды IOCTL_VALSET мы можем устанавливать 32-битные беззнаковые целые числа (unsigned int)
    в поле val этой структуры.

2. Получение текущего значения:

    ```bash
    sudo cat /dev/ioctltest
    ```
   
    Здесь последовательность действий такая:
    
    a) Команда cat считывает содержимое файла /dev/ioctltest и выводит его в стандартный вывод (терминал).
    b) Таким образом, cat читает значение из переменной val в драйвере и выводит в терминал.
    c) Это позволяет получить текущее значение из драйвера без использования команд ioctl.
    
    Чтение данных и передача в приложение на уровне ядра
    
    Для чтения данных из драйвера и передачи их в приложение пользователя на уровне ядра используются команды:

    ```bash
    #define IOCTL_VALGET _IOR(IOC_MAGIC, 1, struct ioctl_arg)
    #define IOCTL_VALGET_NUM _IOR(IOC_MAGIC, 3, int)
    ```
   
    IOCTL_VALGET (команда 1) считывает значение из структуры ioctl_arg.
    IOCTL_VALGET_NUM (команда 3) считывает числовое значение типа int.
    Далее выполняется копирование данных в пространство пользователя с помощью copy_to_user().
    Таким образом, эти команды ioctl позволяют передать данные из драйвера в приложение на низком уровне ядра.

3. Установка числа 10:

    ```bash
    sudo bash -c 'echo 2 10 > /dev/ioctltest'
    ```

    Здесь в команде мы указываем номер 2, соответствующий IOCTL_VALSET_NUM. А значение 10 будет преобразовано к 
    целочисленному типу int и сохранено в драйвере, так как принимает int.

    ```bash
    #define IOCTL_VALSET_NUM _IOW(IOC_MAGIC, 2, int)
    ```
   
#### В нашем случае, при попытке записи в это устройство командами echo возникает ошибка:

    ```bash
    sudo bash -c 'echo 0 15 > /dev/ioctltest'
    ```

bash: строка 1: echo: ошибка записи: Недопустимый аргумент.
Это нормально, так как в драйвере пока не реализована поддержка записи, только чтение и ioctl.
При открытии /dev/ioctltest в лог попадают вызовы функций open/close драйвера:

    ```bash
    test_ioctl_open call.
    test_ioctl_close call.
    ```

Таким образом, базовая функциональность драйвера работает - загрузка/выгрузка модуля, создание устройства, обработка 
open/close.

#### Объяснение про структуру test_ioctl_data и назначение некоторых макросов.

Итак, структура test_ioctl_data используется для хранения данных, с которыми работает наше устройство, реализованное в 
виде драйвера.

Она содержит два поля:
1.	Val
      Это значение, которым мы можем управлять через команды IOCTL. Например, устанавливать его командами IOCTL_VALSET 
      или IOCTL_VALSET_NUM. И считывать командами IOCTL_VALGET.
      Это некое "состояние" нашего устройства, реализованного в драйвере.

2.	Lock
      Это блокировка для синхронизации доступа к полю val из разных потоков. Так как ядро Linux многопоточное, то без 
      этой блокировки при одновременном доступе могут возникнуть проблемы и данные могут повредиться.
      Поэтому чтение-изменение поля val происходит только внутри блокировки с использованием read/write lock для 
      синхронизации. Это гарантирует целостность данных.

#### Теперь насчет некоторых макросов:

1.	IOC_MAGIC – это магическое число (у нас \x66), по которому ядро Linux определяет, что команда IOCTL предназначена 
    именно для нашего драйвера. Без этого номера команды IOCTL просто не будут обрабатываться.
    Это сделано для того, чтобы команды IOCTL из разных драйверов не конфликтовали между собой.

2.	IOCTL_VAL_MAXNR - это макрос, который определяет максимальный номер команды IOCTL, поддерживаемый вашим драйвером. 
    Этот макрос используется в ядре Linux для обеспечения корректной обработки команд IOCTL для вашего драйвера.
    Зачем это нужно: Когда приходит запрос на выполнение команды IOCTL, ядро использует номер команды (cmd), переданный 
    в ioctl-функцию, чтобы определить, какую операцию выполнять. Макрос IOCTL_VAL_MAXNR служит ограничителем для номеров
    команд. Он говорит ядру, что ваш драйвер поддерживает команды с номерами от 0 до IOCTL_VAL_MAXNR.
 
    Пример использования: в данном случае наш драйвер поддерживает четыре команды:

    ```bash
    #define IOCTL_VALSET _IOW(IOC_MAGIC, 0, struct ioctl_arg)  
    #define IOCTL_VALGET _IOR(IOC_MAGIC, 1, struct ioctl_arg)
    #define IOCTL_VALSET_NUM _IOW(IOC_MAGIC, 2, int)
    #define IOCTL_VALGET_NUM _IOR(IOC_MAGIC, 3, int)
    ```
    
    то IOCTL_VAL_MAXNR должен быть установлен в 3 (от 0 до 3 включительно) – четыре команды.

    ```bash
    #define IOCTL_VAL_MAXNR 3
    ```

3.	DRIVER_NAME - Определение имени вашего драйвера. Это используется при регистрации устройства.


### Шаг XIV.	Выгрузка модуля ядра и удаление узлов символьных устройств:

    ```bash
    sudo rmmod ioctl
    sudo rm /dev/ioctltest
    ```
### Шаг XV.	Проверяем системные логи, чтобы убедиться, что модуль был успешно выгружен:

```bash
    current_user@current_user:/develop/kernel/dev/chardev/ioctl$ sudo journalctl --since "1 hour ago" | grep "ioctltest"
    дек 12 19:26:54 current_user kernel: ioctltest driver removed.
    дек 12 19:27:06 current_user sudo[28872]: current_user : TTY=pts/0 ; PWD=/home/current_user/.local/share/Trash/files/ioctl ;
     USER=root ; COMMAND=/usr/bin/rm /dev/ioctltest
    current_user@current_user:/develop/kernel/dev/chardev/ioctl$ sudo journalctl --since "1 hour ago" | grep "ioctl"
    дек 12 19:26:54 current_user sudo[28866]: current_user : TTY=pts/0 ; PWD=/home/current_user/.local/share/Trash/files/ioctl ; 
    USER=root ; COMMAND=/usr/sbin/rmmod ioctl
    дек 12 19:26:54 current_user kernel: ioctltest driver removed.
    дек 12 19:27:06 current_user sudo[28872]: current_user : TTY=pts/0 ; PWD=/home/current_user/.local/share/Trash/files/ioctl ; 
    USER=root ; COMMAND=/usr/bin/rm /dev/ioctltest
    дек 12 19:27:12 current_user sudo[28875]: current_user : TTY=pts/0 ; PWD=/home/current_user/.local/share/Trash/files/ioctl ;
     USER=root ; COMMAND=/usr/sbin/lsmod
    дек 12 19:38:16 current_user sudo[28986]: current_user : TTY=pts/0 ; PWD=/home/current_user/.local/share/Trash/files/ioctl ; 
    USER=root ; COMMAND=/usr/sbin/lsmod
    дек 12 19:38:28 current_user sudo[28990]: current_user : TTY=pts/0 ; PWD=/home/current_user/.local/share/Trash/files/ioctl ;
     USER=root ; COMMAND=/usr/bin/journalctl --since '1 hour ago'
    дек 12 19:38:41 current_user sudo[28995]: current_user : TTY=pts/0 ; PWD=/home/current_user/.local/share/Trash/files/ioctl ; 
    USER=root ; COMMAND=/usr/bin/journalctl --since '1 hour ago'
    current_user@current_user:/develop/kernel/dev/chardev/ioctl$ sudo dmesg | grep ioctltest
    [ 3470.349448] ioctltest driver(major: 510) installed.
    [ 3881.650341] ioctltest driver removed.
    [ 4402.422718] ioctltest driver(major: 510) installed.
    [ 6511.538812] ioctltest driver removed.
    [100806.994287] ioctltest driver(major: 510) installed.
    [109686.205333] ioctltest driver removed.
    [109839.657702] ioctltest driver(major: 510) installed.
    [135289.520975] ioctltest driver removed.
    [135659.767446] ioctltest driver(major: 510) installed.
    [136747.096903] ioctltest driver removed.
    [137368.935906] ioctltest driver(major: 510) installed.
    [146429.866113] ioctltest driver removed.
    [151753.294087] ioctltest driver(major: 510) installed.
    [155093.188677] ioctltest driver removed.
    current_user@current_user:/develop/kernel/dev/chardev/ioctl$ sudo dmesg | grep ioctl
    [ 0.088567] device-mapper: ioctl: 4.48.0-ioctl (2023-03-01) initialised: dm-devel@redhat.com
    [ 3470.348093] ioctl: loading out-of-tree module taints kernel.
    [ 3470.348143] ioctl: module verification failed: signature and/or required key missing - tainting kernel
    [ 3470.349448] ioctltest driver(major: 510) installed.
    [ 3624.045472] test_ioctl_open call.
    [ 3624.048356] test_ioctl_close call.
    [ 3673.803562] test_ioctl_open call.
    [ 3673.804132] test_ioctl_close call.
    [ 3793.446842] test_ioctl_open call.
    [ 3812.352249] test_ioctl_close call.
    [ 3881.650341] ioctltest driver removed.
    [ 4402.422718] ioctltest driver(major: 510) installed.
    [ 6511.538812] ioctltest driver removed.
    [100806.994287] ioctltest driver(major: 510) installed.
    [109686.205333] ioctltest driver removed.
    [109839.657702] ioctltest driver(major: 510) installed.
    [110204.447385] test_ioctl_open call.
    [110204.449016] test_ioctl_close call.
    [110448.164679] test_ioctl_open call.
    [110448.165143] test_ioctl_close call.
    [111563.265989] test_ioctl_open call.
    [111563.266297] test_ioctl_close call.
    [111646.883354] test_ioctl_open call.
    [114061.912741] test_ioctl_open call.
    [114061.913295] test_ioctl_close call.
    [114116.230858] test_ioctl_open call.
    [114116.231180] test_ioctl_close call.
    [135277.079326] test_ioctl_close call.
    [135289.520975] ioctltest driver removed.
    [135659.767446] ioctltest driver(major: 510) installed.
    [135915.258723] test_ioctl_open call.
    [135915.259156] test_ioctl_close call.
    [135944.323678] test_ioctl_open call.
    [135944.323918] test_ioctl_close call.
    [136076.117777] test_ioctl_open call.
    [136076.118239] test_ioctl_close call.
    [136258.092553] test_ioctl_open call.
    [136258.093213] test_ioctl_close call.
    [136289.768766] test_ioctl_open call.
    [136296.148247] test_ioctl_close call.
    [136347.479834] test_ioctl_open call.
    [136347.480312] test_ioctl_close call.
    [136356.369914] test_ioctl_open call.
    [136356.370208] test_ioctl_close call.
    [136367.289870] test_ioctl_open call.
    [136367.290283] test_ioctl_close call.
    [136413.795763] test_ioctl_open call.
    [136413.796128] test_ioctl_close call.
    [136462.390742] test_ioctl_open call.
    [136462.391267] test_ioctl_close call.
    [136747.096903] ioctltest driver removed.
    [137368.935906] ioctltest driver(major: 510) installed.
    [137444.605300] test_ioctl_open call.
    [137444.605603] test_ioctl_close call.
    [137460.258473] test_ioctl_open call.
    [137460.258792] test_ioctl_close call.
    [137479.896868] test_ioctl_open call.
    [137479.897331] test_ioctl_close call.
    [138724.039400] test_ioctl_open call.
    [138724.039760] test_ioctl_close call.
    [138864.709790] test_ioctl_open call.
    [138864.710361] test_ioctl_close call.
    [139072.267044] test_ioctl_open call.
    [139072.267561] test_ioctl_close call.
    [142097.607794] test_ioctl_open call.
    [142097.608029] test_ioctl_close call.
    [142142.685122] test_ioctl_open call.
    [142142.685602] test_ioctl_close call.
    [142196.710044] test_ioctl_open call.
    [142196.710284] test_ioctl_close call.
    [142743.958100] test_ioctl_open call.
    [142743.958724] test_ioctl_close call.
    [146429.866113] ioctltest driver removed.
    [151753.294087] ioctltest driver(major: 510) installed.
    [151885.751317] test_ioctl_open call.
    [151885.751747] test_ioctl_close call.
    [151911.457129] test_ioctl_open call.
    [151911.457711] test_ioctl_close call.
    [155093.188677] ioctltest driver removed.
    ```

Эти шаги предоставляют основной процесс сборки, загрузки и тестирования нашего модуля ядра Linux, предоставляющего IOCTL 
интерфейс. 



# procfs-3.h and procfs-3.c – Managing /proc File Using Standard Linux Kernel File System.

## Steps on Ubuntu 23.10:
1. Install necessary tools for building programs and managing kernel modules on your system:

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
   
3. Install corresponding header files that may be needed for kernel module compilation (for the current kernel version) 
   or other programs:

    ```bash
    sudo apt-get install linux-headers-$(uname -r)
    ```
   
4. Create a new project at the path - /home/current_user/develop/kernel/proc/proc-3.
5. In the project root, create files procfs-3.h and procfs-3.c.
6. In the project root, create Makefile.
7. Navigate to your project directory:

    ```bash
    cd /home/current_user/develop/kernel/proc/proc-3
    ```
   
8. Use make to compile the code:

    ```bash
    make
    ```
    Example input and output:
    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-3$ sudo make
    make -C /lib/modules/6.5.0-13-generic/build M=/home/current_user/develop/kernel/proc/proc-3 modules
    make[1]: Entering directory '/usr/src/linux-headers-6.5.0-13-generic'
    warning: the compiler differs from the one used to build the kernel
    The kernel was built by: aarch64-linux-gnu-gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
    You are using:           gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
    CC [M]  /home/current_user/develop/kernel/proc/proc-3/procfs-3.o
    MODPOST /home/current_user/develop/kernel/proc/proc-3/Module.symvers
    CC [M]  /home/current_user/develop/kernel/proc/proc-3/procfs-3.mod.o
    LD [M]  /home/current_user/develop/kernel/proc/proc-3/procfs-3.ko
    BTF [M] /home/current_user/develop/kernel/proc/proc-3/procfs-3.ko
    make[1]: Leaving directory '/usr/src/linux-headers-6.5.0-13-generic'
    ```

9. Get information about the module:

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-3$ modinfo procfs-3.ko
    filename:       /home/current_user/develop/kernel/proc/proc-3/procfs-3.ko
    license:        GPL
    srcversion:     42DF6553807AF26E9A76F4B
    depends:        
    name:           procfs_3
    vermagic:       6.5.0-13-generic SMP preempt mod_unload modversions aarch64
    ```

10. Ensure the module named "procfs_3" is not loaded:

    ```bash
    sudo lsmod | grep procfs
    ```

11. After successful compilation, load the module into the kernel:

    ```bash
    sudo insmod procfs-3.ko
    ```

12. Check the module loading:

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-3$ sudo lsmod | grep procfs
    procfs_3               20480  0
    ```

13. Confirm the existence of the buffer2k file in the system in the /proc directory.

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-3$ ls /proc
    1     1355  199   2245  246   2746  39    63   926            kallsyms
    100   14    1995  2253  2465  2767  4     64   927            kcore
    1007  1433  2     2256  247   28    40    65   93             keys
    101   1488  20    226   2473  2813  41    66   94             key-users
    1010  1498  200   2266  2475  2847  43    67   95             kmsg
    1015  1499  2006  2272  248   2854  432   68   96             kpagecgroup
    1016  15    201   2275  2484  2856  44    69   97             kpagecount
    102   153   2015  228   249   2861  4448  7    98             kpageflags
    1020  1530  2017  2284  25    2868  45    70   987            loadavg
    103   1550  202   2287  250   287   454   71   99             locks
    104   157   203   2289  2504  288   46    72   990            mdstat
    105   158   204   229   251   2880  467   73   991            meminfo
    1055  16    205   2292  2511  289   47    74   992            misc
    106   17    206   2299  252   29    4717  75   997            modules
    1060  18    2068  23    2527  290   49    76   998            mounts
    1061  1834  207   230   2528  291   5     77   999            net
    107   1876  2079  2307  253   2929  50    78   acpi           pagetypeinfo
    108   188   208   2309  254   2962  51    79   asound         partitions
    1087  189   2082  2310  2546  3     53    8    bootconfig     pressure
    11    19    209   2311  255   3020  539   80   buddyinfo      schedstat
    111   1901  2092  2313  2554  3063  54    81   buffer2k       scsi
    112   1905  21    2315  256   31    540   82   bus            self
    113   191   210   2319  2566  3116  541   826  cgroups        slabinfo
    115   1916  211   232   2567  32    55    827  cmdline        softirqs
    1185  1917  212   2326  257   326   56    828  consoles       stat
    1187  192   213   234   2579  33    566   829  cpuinfo        swaps
    1188  193   2136  2350  258   34    567   83   crypto         sys
    1197  1933  2137  2351  259   345   568   84   devices        sysrq-trigger
    12    1935  214   236   26    35    569   85   diskstats      sysvipc
    121   194   2145  237   260   3697  57    86   driver         thread-self
    122   1940  215   238   261   37    571   866  dynamic_debug  timer_list
    1228  1942  216   239   262   3724  572   87   execdomains    tty
    123   195   217   2393  263   3735  573   878  fb             uptime
    125   1957  218   241   264   3769  58    88   filesystems    version
    13    196   219   242   265   38    59    89   fs             version_signature
    130   197   22    243   2651  3814  6     9    interrupts     vmallocinfo
    1328  1972  220   2436  2678  387   60    90   iomem          vmstat
    1335  198   2226  244   27    3870  61    91   ioports        zoneinfo
    1341  1985  223   2454  2718  388   62    92   irq
    ```


14. In this step, a new value "Hello, Kernelcat /proc/buffer2k!" is written to the /proc/buffer2k file. This operation 
    uses the tee command, which first outputs data to the standard output and then writes it to the specified file. The 
    command output displays the new value.

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-3$ echo "Hello, Kernelcat /proc/buffer2k!" |
    sudo tee /proc/buffer2k
    Hello, Kernelcat /proc/buffer2k!
    ```

15. Read the contents of the /proc/buffer2k file using the cat command.

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-3$ cat /proc/buffer2k
    Hello, Kernelcat /proc/buffer2k!
    ```

16. To remove the module, use the following command:

    ```bash
    sudo rmmod procfs-3
    ```
    
17. View kernel-related system logs and filter the lines containing "procfs" - sudo journalctl --since "1 hour ago" | 
    grep procfs:

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-3$ sudo journalctl --since "1 hour ago" | grep "procfs"
    Dec 04 13:57:38 current_user sudo[9611]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/proc/proc-3 ;
    USER=root ; COMMAND=/usr/sbin/insmod procfs-3.ko
    Dec 04 14:10:17 current_user sudo[9709]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/proc/proc-3 ;
    USER=root ; COMMAND=/usr/sbin/rmmod procfs-3
    ```
    

# /proc Interface Depending on Kernel Version

The proc_ops interface is available starting from kernel version 5.6. For compatibility with older kernels, the 
file_operations interface can be used. Below is an example code demonstrating the implementation of read and write 
handlers for the /proc/buffer2k file, as well as corresponding open and close handlers. The code includes a check for 
the availability of proc_ops using the HAVE_PROC_OPS macro.

In the file.h

```bash
// This macro is used to check the availability of proc_ops in kernel versions 5.6 and above.
#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 6, 0)
#define HAVE_PROC_OPS
#endif
```

In the file.c

/proc Interface
```bash
static ssize_t procfile_read(struct file *filePointer, char __user *buffer, size_t buffer_length, loff_t *offset)
{... implementation ...}

static ssize_t procfile_write(struct file *file, const char __user *buff, size_t len, loff_t *off)
{... implementation ...}

// Depending on the kernel version, either proc_ops or standard file_operations may be used.
#ifdef HAVE_PROC_OPS
static const struct proc_ops proc_file_fops = {
.proc_read = procfile_read,
.proc_write = procfile_write,
};
#else
static const struct file_operations proc_file_fops = {
.read = procfile_read,
.write = procfile_write,
};
#endif
```

inode_operations Interface for Open and Close
```bash
// inode_operations
static int procfs_open(struct inode *inode, struct file *file)
{... implementation ...}

static int procfs_close(struct inode *inode, struct file *file)
{... implementation ...}

// Depending on the kernel version, either proc_ops or standard file_operations may be used.
#ifdef HAVE_PROC_OPS
static struct proc_ops file_ops_4_our_proc_file = {
.proc_read = procfs_read,
.proc_write = procfs_write,
.proc_open = procfs_open,
.proc_release = procfs_close,
};
#else
static const struct file_operations file_ops_4_our_proc_file = {
.read = procfs_read,
.write = procfs_write,
.open = procfs_open,
.release = procfs_close,
};
#endif
```



# procfs-3.h и procfs-3.c – данный код демонстрирует управление файлом /proc с помощью стандартной файловой системы в 
ядре Linux.

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

4. Создаем новый проект по пути - `/home/current_user/develop/kernel/proc/proc-3`.

5. В корне проекта создаем файлы `procfs-3.h` и `procfs-3.c`.

6. В корне проекта создаем `Makefile`.

7. Переходим в нашу директорию проекта:

    ```bash
    cd /home/current_user/develop/kernel/proc/proc-3
    ```

8. Используем `make` для компиляции кода:

    ```bash
    make
    ```

   Пример ввода и вывода:

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-3$ sudo make
    make -C /lib/modules/6.5.0-13-generic/build M=/home/current_user/develop/kernel/proc/proc-3 modules
    make[1]: вход в каталог «/usr/src/linux-headers-6.5.0-13-generic»
    warning: the compiler differs from the one used to build the kernel
    The kernel was built by: aarch64-linux-gnu-gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
    You are using:           gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
    CC [M]  /home/current_user/develop/kernel/proc/proc-3/procfs-3.o
    MODPOST /home/current_user/develop/kernel/proc/proc-3/Module.symvers
    CC [M]  /home/current_user/develop/kernel/proc/proc-3/procfs-3.mod.o
    LD [M]  /home/current_user/develop/kernel/proc/proc-3/procfs-3.ko
    BTF [M] /home/current_user/develop/kernel/proc/proc-3/procfs-3.ko
    Skipping BTF generation for /home/current_user/develop/kernel/proc/proc-3/procfs-3.ko due to unavailability of vmlinux
    make[1]: выход из каталога «/usr/src/linux-headers-6.5.0-13-generic»
    ```
9. Получаем информацию о модуле:

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-3$ modinfo procfs-3.ko
    filename:       /home/current_user/develop/kernel/proc/proc-3/procfs-3.ko
    license:        GPL
    srcversion:     42DF6553807AF26E9A76F4B
    depends:        
    name:           procfs_3
    vermagic:       6.5.0-13-generic SMP preempt mod_unload modversions aarch64
    ```

10. Убеждаемся, что модуль с именем "procfs_3" не загружен:

    ```bash
    sudo lsmod | grep procfs
    ```

11. После успешной компиляции загружаем модуль в ядро:

    ```bash
    sudo insmod procfs-3.ko
    ```

12. Проверяем загрузку модуля:

    ```bash
    current_user@current_user:~/develop/kernel/z/proc-3$ sudo lsmod | grep procfs
	procfs_3               20480  0
    ```

13. Убеждаемся в наличии файла buffer2k в системе в каталоге /proc.
    ```bash
	current_user@current_user:~/develop/kernel/proc/proc-3$ ls /proc
    1     1355  199   2245  246   2746  39    63   926            kallsyms
    100   14    1995  2253  2465  2767  4     64   927            kcore
    1007  1433  2     2256  247   28    40    65   93             keys
    101   1488  20    226   2473  2813  41    66   94             key-users
    1010  1498  200   2266  2475  2847  43    67   95             kmsg
    1015  1499  2006  2272  248   2854  432   68   96             kpagecgroup
    1016  15    201   2275  2484  2856  44    69   97             kpagecount
    102   153   2015  228   249   2861  4448  7    98             kpageflags
    1020  1530  2017  2284  25    2868  45    70   987            loadavg
    103   1550  202   2287  250   287   454   71   99             locks
    104   157   203   2289  2504  288   46    72   990            mdstat
    105   158   204   229   251   2880  467   73   991            meminfo
    1055  16    205   2292  2511  289   47    74   992            misc
    106   17    206   2299  252   29    4717  75   997            modules
    1060  18    2068  23    2527  290   49    76   998            mounts
    1061  1834  207   230   2528  291   5     77   999            net
    107   1876  2079  2307  253   2929  50    78   acpi           pagetypeinfo
    108   188   208   2309  254   2962  51    79   asound         partitions
    1087  189   2082  2310  2546  3     53    8    bootconfig     pressure
    11    19    209   2311  255   3020  539   80   buddyinfo      schedstat
    111   1901  2092  2313  2554  3063  54    81   buffer2k       scsi
    112   1905  21    2315  256   31    540   82   bus            self
    113   191   210   2319  2566  3116  541   826  cgroups        slabinfo
    115   1916  211   232   2567  32    55    827  cmdline        softirqs
    1185  1917  212   2326  257   326   56    828  consoles       stat
    1187  192   213   234   2579  33    566   829  cpuinfo        swaps
    1188  193   2136  2350  258   34    567   83   crypto         sys
    1197  1933  2137  2351  259   345   568   84   devices        sysrq-trigger
    12    1935  214   236   26    35    569   85   diskstats      sysvipc
    121   194   2145  237   260   3697  57    86   driver         thread-self
    122   1940  215   238   261   37    571   866  dynamic_debug  timer_list
    1228  1942  216   239   262   3724  572   87   execdomains    tty
    123   195   217   2393  263   3735  573   878  fb             uptime
    125   1957  218   241   264   3769  58    88   filesystems    version
    13    196   219   242   265   38    59    89   fs             version_signature
    130   197   22    243   2651  3814  6     9    interrupts     vmallocinfo
    1328  1972  220   2436  2678  387   60    90   iomem          vmstat
    1335  198   2226  244   27    3870  61    91   ioports        zoneinfo
    1341  1985  223   2454  2718  388   62    92   irq
    ```

14. В данном шаге происходит запись нового значения "Hello, Kernelcat /proc/buffer2k!" в файл /proc/buffer2k. Эта 
    операция использует команду tee, которая сначала выводит данные в стандартный вывод, а затем их записывает в 
    указанный файл. После выполнения команды выводится само новое значение.
    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-3$ echo "Hello, Kernelcat /proc/buffer2k!" | 
    sudo tee /proc/buffer2k
    Hello, Kernelcat /proc/buffer2k!
    ```

15. Читаем содержимое файла /proc/buffer2k с помощью команды cat. 

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-3$ cat /proc/buffer2k
    Hello, Kernelcat /proc/buffer2k!
    ```
    
16. Для удаления модуля используется команда:

    ```bash
    sudo rmmod procfs-3
    ```

17. Это позволяет просмотреть системные логи, связанные с ядром Linux, и фильтрует строки, содержащие "procfs" -
    sudo journalctl --since "1 hour ago" | grep procfs:

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-3$ sudo journalctl --since "1 hour ago" | grep "procfs"
    дек 04 13:57:38 current_user sudo[9611]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/proc/proc-3 ; 
    USER=root ; COMMAND=/usr/sbin/insmod procfs-3.ko
    дек 04 14:10:17 current_user sudo[9709]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/proc/proc-3 ; 
    USER=root ; COMMAND=/usr/sbin/rmmod procfs-3
    ```

## Интерфейс /proc в зависимости от версии ядра

proc_ops - доступен только начиная с ядра версии 5.6. Для совместимости со старыми ядрами можно использовать
file_operations:
1. в файле.h
    ```bash
    // этот макрос используется для проверки доступности proc_ops в версиях ядра 5.6 и выше.
    #if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 6, 0)
    #define HAVE_PROC_OPS
    #endif
    ```
2. в файле.c
    a) интерфейс /proc
    ```bash
    static ssize_t procfile_read(struct file *filePointer, char __user *buffer, size_t buffer_length, loff_t *offset)
    {... реализация ...}

	static ssize_t procfile_write(struct file *file, const char __user *buff, size_t len, loff_t *off)
	{... реализация ...}

	//  В зависимости от версии ядра может использоваться либо proc_ops, либо стандартные file_operations.
	#ifdef HAVE_PROC_OPS
	static const struct proc_ops proc_file_fops = {
		.proc_read = procfile_read,
		.proc_write = procfile_write,
	};
	#else
	static const struct file_operations proc_file_fops = {
		.read = procfile_read,
		.write = procfile_write,
	};
	#endif
    ```
    b) интерфейс - /proc для read и write - это специальный интерфейс, оптимизированный непосредственно под /proc 
       файловую систему. С его помощью мы регистрируем обработчики, которые будут вызываться ядром именно при обращении 
       к /proc файлам.
       inode_operations для open и close - это общий интерфейс в ядре Linux для регистрации файловых операций,
       работающих на уровне inode любой файловой системы (не только /proc).
    ```bash
	// интерфейс /proc
   	static ssize_t procfs_read(struct file *filePointer, char __user *buffer, size_t buffer_length, loff_t *offset)
   	{... реализация ...}

   	static ssize_t procfs_write(struct file *file, const char __user *buff, size_t len, loff_t *off)
   	{... реализация ...}
    
   
   	// inode_operations - является общим интерфейсом для файловых операций на уровне inode в любой файловой системе
   	static int procfs_open(struct inode *inode, struct file *file)
    {... реализация ...}

    static int procfs_close(struct inode *inode, struct file *file)
    {... реализация ...}

	//  В зависимости от версии ядра может использоваться либо proc_ops, либо стандартные file_operations.
    #ifdef HAVE_PROC_OPS
    static struct proc_ops file_ops_4_our_proc_file = {
        .proc_read = procfs_read,
        .proc_write = procfs_write,
        .proc_open = procfs_open,
        .proc_release = procfs_close,
    };
    #else
    static const struct file_operations file_ops_4_our_proc_file = {
        .read = procfs_read,
        .write = procfs_write,
        .open = procfs_open,
        .release = procfs_close,
    };
    #endif
    ```
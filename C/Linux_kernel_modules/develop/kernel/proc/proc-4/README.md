# procfs-4.h and procfs-4.c - Creating a "file" in /proc. This program utilizes the seq_file library to manage the /proc
file.

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

3. Install relevant header files that may be needed for compiling kernel modules or other programs for the current kernel version:

    ```bash
    sudo apt-get install linux-headers-$(uname -r)
    ```

4. Create a new project at the path - `/home/current_user/develop/kernel/proc/proc-4`.

5. In the project root, create files `procfs-4.h` and `procfs-4.c`.

6. In the project root, create a `Makefile`.

7. Navigate to our project directory:

    ```bash
    cd /home/current_user/develop/kernel/proc/proc-4
    ```

8. Use `make` to compile the code:

    ```bash
    make
    ```

   Example input and output:

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-4$ make
    make -C /lib/modules/6.5.0-14-generic/build M=/home/current_user/develop/kernel/proc/proc-4 modules
    make[1]: Entering directory '/usr/src/linux-headers-6.5.0-14-generic'
    warning: the compiler differs from the one used to build the kernel
      The kernel was built by: aarch64-linux-gnu-gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
      You are using:           gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
      CC [M]  /home/current_user/develop/kernel/proc/proc-4/procfs-4.o
      MODPOST /home/current_user/develop/kernel/proc/proc-4/Module.symvers
      CC [M]  /home/current_user/develop/kernel/proc/proc-4/procfs-4.mod.o
      LD [M]  /home/current_user/develop/kernel/proc/proc-4/procfs-4.ko
      BTF [M] /home/current_user/develop/kernel/proc/proc-4/procfs-4.ko
    Skipping BTF generation for /home/current_user/develop/kernel/proc/proc-4/procfs-4.ko due to unavailability of vmlinux
    make[1]: Leaving directory '/usr/src/linux-headers-6.5.0-14-generic'
    ```

9. Get information about the module:

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-4$ modinfo procfs-4.ko
    filename:       /home/shrekulka/develop/kernel/proc/proc-4/procfs-4.ko
    license:        GPL
    srcversion:     EBDB5A613BF353AE315D828
    depends:        
    name:           procfs_4
    vermagic:       6.5.0-14-generic SMP preempt mod_unload modversions aarch64
    ```

10. Ensure that the module named "procfs_4" is not loaded:

    ```bash
    sudo lsmod | grep procfs
    ```

11. After successful compilation, load the module into the kernel:

    ```bash
    sudo insmod procfs-4.ko
    ```

12. Check the module load:

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-4$ sudo lsmod | grep procfs
	procfs_4               16384  0
    ```

13. When executing the 'cat /proc/iter' command, the content of the /proc/iter file is read, and it is displayed in the terminal. In this case, the "0" value is the result of the my_seq_show function, which outputs the current value of the counter.

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-4$ cat /proc/iter
    0
    ```

14. In this step, a new value "Test data" is written to the /proc/iter file. After executing the command, the new value itself is displayed.

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-4$ echo "Test data" /proc/iter
    Test data /proc/iter
    ```

15. When executing the 'cat /proc/iter' command after the previous write, the value "1" is the result of the my_seq_show function, which increments the counter.

     ```bash
        current_user@current_user:~/develop/kernel/proc/proc-4$ cat /proc/iter
        1
     ```

16. Confirm the presence of the 'iter' file in the system in the /proc directory.

    ```bash
    rent_user@current_user:~/develop/kernel/proc/proc-4$ ls /proc
    1     1486  2062  2261  2530  28    4766  66   95             kmsg
    100   1492  208   228   254   280   4854  67   96             kpagecgroup
    1007  15    209   229   255   281   4856  68   97             kpagecount
    1009  152   2095  23    256   2835  49    69   98             kpageflags
    101   155   21    230   2574  2837  4907  70   985            loadavg
    1012  1551  211   231   258   29    4910  71   988            locks
    1013  158   212   232   2588  2908  4920  72   989            mdstat
    1019  16    2122  233   259   296   4926  73   99             meminfo
    102   17    2123  234   26    2996  4983  74   990            misc
    103   1766  213   235   260   3     5     75   994            modules
    104   18    214   236   2616  3044  50    76   996            mounts
    1046  1862  2166  2361  2617  307   5010  77   997            net
    105   188   217   237   262   3076  5013  78   acpi           pagetypeinfo
    106   1880  219   238   263   317   5060  79   asound         partitions
    1060  1884  2190  2393  264   32    51    8    bootconfig     pressure
    107   189   2198  240   265   33    53    80   buddyinfo      schedstat
    1077  1896  22    2404  2658  34    54    81   bus            self
    108   1897  2200  241   266   35    544   82   cgroups        slabinfo
    1084  19    2213  2413  2668  38    545   824  cmdline        softirqs
    11    1906  2217  242   267   385   546   825  consoles       stat
    111   1907  222   2432  268   386   55    826  cpuinfo        swaps
    112   1913  2221  2444  269   39    56    827  crypto         sys
    1181  1916  2226  2447  27    4     57    83   devices        sysrq-trigger
    1183  192   2227  2448  270   40    570   84   diskstats      sysvipc
    1184  193   2229  245   271   41    573   85   driver         thread-self
    119   194   223   2454  2710  4130  574   86   dynamic_debug  timer_list
    12    1942  2230  246   272   4165  575   860  execdomains    tty
    1203  195   2231  2466  273   4186  576   864  fb             uptime
    1226  1956  224   247   2730  42    579   868  filesystems    version
    124   1965  2243  2474  2731  430   58    87   fs             version_signature
    1260  1972  2244  2479  2733  44    580   879  interrupts     vmallocinfo
    1275  1982  2245  248   2736  4436  59    88   iomem          vmstat
    1277  1991  2246  249   274   45    6     89   ioports        zoneinfo
    129   2     2247  2490  275   46    60    9    irq
    13    20    225   25    276   464   61    90   kallsyms
    1359  2004  2252  251   277   466   62    91   kcore
    14    2040  2258  2517  278   4682  63    92   keys
    1420  2049  2259  252   279   4686  64    93   key-users
    1485  2051  2260  253   2795  47    65    94   kmsg
    ```

17. To remove the module, use the command:

    ```bash
    sudo rmmod procfs-4
    ```

18. After removing the module, verify that the 'iter' file is no longer present in /proc.

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-4$ ls /proc
    1     1486  2062  2261  2530  28    4766  66   95             kpagecgroup
    100   1492  208   228   254   280   4854  67   96             kpagecount
    1007  15    209   229   255   281   4856  68   97             kpageflags
    1009  152   2095  23    256   2835  49    69   98             loadavg
    101   155   21    230   2574  2837  4907  70   985            locks
    1012  1551  211   231   258   29    4910  71   988            mdstat
    1013  158   212   232   2588  2908  4920  72   989            meminfo
    1019  16    2122  233   259   296   4926  73   99             misc
    102   17    2123  234   26    2996  4983  74   990            modules
    103   1766  213   235   260   3     5     75   994            mounts
    104   18    214   236   2616  3044  50    76   996            net
    1046  1862  2166  2361  2617  307   5010  77   997            pagetypeinfo
    105   188   217   237   262   3076  5013  78   acpi           partitions
    106   1880  219   238   263   317   5060  79   asound         pressure
    1060  1884  2190  2393  264   32    51    8    bootconfig     schedstat
    107   189   2198  240   265   33    53    80   buddyinfo      scsi
    1077  1896  22    2404  2658  34    54    81   bus            self
    108   1897  2200  241   266   35    544   82   cgroups        slabinfo
    1084  19    2213  2413  2668  38    545   824  cmdline        softirqs
    11    1906  2217  242   267   385   546   825  consoles       stat
    111   1907  222   2432  268   386   55    826  cpuinfo        swaps
    112   1913  2221  2444  269   39    56    827  crypto         sys
    1181  1916  2226  2447  27    4     57    83   devices        sysrq-trigger
    1183  192   2227  2448  270   40    570   84   diskstats      sysvipc
    1184  193   2229  245   271   41    573   85   driver         thread-self
    119   194   223   2454  2710  4130  574   86   dynamic_debug  timer_list
    12    1942  2230  246   272   4165  575   860  execdomains    tty
    1203  195   2231  2466  273   4186  576   864  fb             uptime
    1226  1956  224   247   2730  42    579   868  filesystems    version
    124   1965  2243  2474  2731  430   58    87   fs             version_signature
    1260  1972  2244  2479  2733  44    580   879  interrupts     vmallocinfo
    1275  1982  2245  248   2736  4436  59    88   iomem          vmstat
    1277  1991  2246  249   274   45    6     89   ioports        zoneinfo
    129   2     2247  2490  275   46    60    9    irq
    13    20    225   25    276   464   61    90   kallsyms
    1359  2004  2252  251   277   466   62    91   kcore
    14    2040  2258  2517  278   4682  63    92   keys
    1420  2049  2259  252   279   4686  64    93   key-users
    1485  2051  2260  253   2795  47    65    94   kmsg
    ```

19. This command allows you to view system logs related to the Linux kernel and filters lines containing "procfs" within
    the last hour:

    ```bash
    Dec 05 13:12:58 current_user sudo[4555]: current_user: TTY=pts/0; PWD=/home/current_user/develop/kernel/proc/proc-4;
    USER=root; COMMAND=/usr/sbin/insmod procfs-4.ko
    Dec 05 13:12:58 current_user kernel: procfs_4: loading out-of-tree module taints kernel.
    Dec 05 13:12:58 current_user kernel: procfs_4: module verification failed: signature and/or required key missing -
    tainting kernel
    Dec 05 13:57:56 current_user sudo[5052]: current_user: TTY=pts/0; PWD=/home/current_user/develop/kernel/proc/proc-4;
    USER=root; COMMAND=/usr/sbin/rmmod procfs-4
    ```
    
20. The command 'sudo dmesg | grep procfs' outputs kernel messages related to the 'procfs-4' module:

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-4$ sudo dmesg | grep procfs
    [  213.049925] procfs_4: loading out-of-tree module taints kernel.
    [  213.049934] procfs_4: module verification failed: signature and/or requ
    ```


# When to Use proc_ops, inode_operations, seq_file:

1. proc_ops - Use when you need to quickly create a simple file in /proc for statistics or debugging.
2. inode_operations - Choose when low-level control over files, hard links, and permissions is required.
3. seq_file - Convenient for outputting debug data or statistics to /proc files. Allows easy organization of 
   "step-by-step" output.

# Explanations with Examples:

1. proc_ops
   proc_ops is a specialized interface optimized specifically for creating and managing files in the /proc file system 
   of the kernel. It includes elements such as (proc_ops - a simple API, specifically for /proc files):

    ```bash
   // Kernel version check for proc_ops usage
   #if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 6, 0)
   #define HAVE_PROC_OPS
   #endif

    // Function for reading from /proc file
    static ssize_t my_read(struct file *filp, char __user *buffer, size_t length, loff_t *offset);
    
    // Function for writing to /proc file
    static ssize_t my_write(struct file *file, const char __user *buffer, size_t len, loff_t *off);
    
    // Function for moving the file position pointer
    static loff_t my_llseek(struct file *file, loff_t offset, int whence);
    
    // Function for handling ioctl (input-output control) operations
    static long my_ioctl(struct file *file, unsigned int cmd, unsigned long arg);
    
    // Function for mapping the file into memory
    static int my_mmap(struct file *file, struct vm_area_struct *vma);
    
    // Function for flushing data to the file
    static int my_flush(struct file *file, fl_owner_t id);
    
    // Function for syncing file data with the disk
    static int my_fsync(struct file *file, loff_t start, loff_t end, int datasync);
    
    // Function for managing asynchronous file events
    static int my_fasync(int fd, struct file *file, int mode);
    
    // Use the proc_ops structure if the kernel is 5.6.0 or newer and supports the new proc_ops.
    #ifdef HAVE_PROC_OPS
    static const struct proc_ops my_file_ops = {
    .proc_read = my_read,
    .proc_write = my_write,
    .proc_llseek = my_llseek,
    .proc_ioctl = my_ioctl,
    .proc_mmap = my_mmap,
    .proc_flush = my_flush,
    .proc_fsync = my_fsync,
    .proc_fasync = my_fasync,
    };
    // Otherwise, if the kernel 5.6.0 or newer does not support new proc_ops, use file_operations.
    #else
    static const struct file_operations my_file_ops = {
    .read = my_read,
    .write = my_write,
    .llseek = my_llseek,
    .ioctl = my_ioctl,
    .mmap = my_mmap,
    .flush = my_flush,
    .fsync = my_fsync,
    .fasync = my_fasync,
    };
    #endif
    ```

2. inode_operations
   inode_operations is a lower-level and more universal API for implementing various file systems. It contains an 
   extended set of operations for working with file index descriptors (inode) (inode_operations - low-level and universal):
   ```bash
   // Kernel version check for proc_ops usage
   #if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 6, 0)
   #define HAVE_PROC_OPS
   #endif

    // Function for opening a file
    static int my_open(struct inode* inode, struct file* file);
    
    // Function for closing a file
    static int my_release(struct inode* inode, struct file* file);
    
    // Function for creating a file
    static struct dentry *my_create(struct inode *dir, struct dentry *dentry, umode_t mode, bool excl);
    
    // Function for finding a file in the directory
    static struct dentry *my_lookup(struct inode *dir, struct dentry *dentry, unsigned int flags);
    
    // Function for creating a hard link
    static int my_link(struct dentry *old_dentry, struct inode *dir, struct dentry *dentry);
    
    // Function for deleting a file
    static int my_unlink(struct inode *dir, struct dentry *dentry);
    
    // Function for creating a symbolic link
    static struct dentry *my_symlink(struct inode *dir, struct dentry *dentry, const char *symname);
    
    // Function for creating a subdirectory
    static int my_mkdir(struct inode *dir, struct dentry *dentry, umode_t mode);
    
    // Function for deleting a subdirectory
    static int my_rmdir(struct inode *dir, struct dentry *dentry);
    
    // Function for creating a device
    static int my_mknod(struct inode *dir, struct dentry *dentry, umode_t mode, dev_t dev);
    
    // Function for renaming a file or directory
    static int my_rename(struct inode *old_dir, struct dentry *old_dentry, struct inode *new_dir,
    struct dentry *new_dentry, unsigned int flags);
    
    // Function for setting file attributes
    static int my_setattr(struct dentry *dentry, struct iattr *attr);
    
    // Function for checking file access permissions
    static int my_permission(struct inode *inode, int mask);
    
    // Use the proc_ops structure if the kernel is 5.6.0 or newer and supports the new proc_ops.
    #ifdef HAVE_PROC_OPS
    // Structure representing operations on file index descriptors (inode) using proc_ops
    static struct proc_ops my_file_ops = {
    .proc_open = my_open,
    .proc_release = my_release,
    .proc_create = my_create,
    .proc_lookup = my_lookup,
    .proc_link = my_link,
    .proc_unlink = my_unlink,
    .proc_symlink = my_symlink,
    .proc_mkdir = my_mkdir,
    .proc_rmdir = my_rmdir,
    .proc_mknod = my_mknod,
    .proc_rename = my_rename,
    .proc_setattr = my_setattr,
    .proc_permission = my_permission,
    };
    // Otherwise, if the kernel 5.6.0 or newer does not support new proc_ops, use file_operations.
    #else
    // Structure representing operations on file index descriptors (inode) without using proc_ops
    static const struct file_operations my_file_ops = {
    .open = my_open,
    .release = my_release,
    .create = my_create,
    .lookup = my_lookup,
    .link = my_link,
    .unlink = my_unlink,
    .symlink = my_symlink,
    .mkdir = my_mkdir,
    .rmdir = my_rmdir,
    .mknod = my_mknod,
    .rename = my_rename,
    .setattr = my_setattr,
    .permission = my_permission,
    };
    #endif
   ```
   
3. seq_file
   seq_file is a special interface in the /proc file system that simplifies outputting data to /proc files using a 
   sequence of functions (seq_file - for convenient data output to /proc):

   ```bash
   // Handler for the start of the sequence
   static void *my_seq_start(struct seq_file *s, loff_t *pos);

    // Handler for moving to the next step
    static void *my_seq_next(struct seq_file *s, void *v, loff_t *pos);
    
    // Handler for completing the sequence
    static void my_seq_stop(struct seq_file *s, void *v);
    
    // User-defined function for formatting output
    static int my_seq_show(struct seq_file *s, void *v);
    
    // Add filler characters to the buffer
    static void my_seq_pad(struct seq_file *m, char c);
    
    // Structure representing operations on a sequence (seq_operations)
    static struct seq_operations my_seq_ops = {
    .start = my_seq_start,
    .next = my_seq_next,
    .stop = my_seq_stop,
    .show = my_seq_show,
    .pad = my_seq_pad,
    };
    ```
## Example:

    ```bash
    // Kernel version check for proc_ops usage
    #if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 6, 0)
    #define HAVE_PROC_OPS
    #endif
    
    // Handler for the start of the sequence
    static void *my_seq_start(struct seq_file *s, loff_t *pos);
    
    // Handler for moving to the next step
    static void *my_seq_next(struct seq_file *s, void *v, loff_t *pos);
    
    // Handler for completing the sequence
    static void my_seq_stop(struct seq_file *s, void *v);
    
    // Handler for outputting step data to the buffer
    static int my_seq_show(struct seq_file *s, void *v);
    
    // Structure representing operations on a sequence (seq_operations)
    static struct seq_operations my_seq_ops = {
    .start = my_seq_start,  // handler for the start of the sequence
    .next = my_seq_next,    // handler for moving to the next step
    .stop = my_seq_stop,    // handler for completing the sequence
    .show = my_seq_show,    // handler for outputting step data to the buffer
    };
    
    // Use the proc_ops structure if the kernel is 5.6.0 or newer and supports new proc_ops.
    #ifdef HAVE_PROC_OPS
    // Structure representing operations on a /proc file (using proc_ops)
    static const struct proc_ops my_file_ops = {
    .proc_open = my_open,        // handler for opening the file
    .proc_read = seq_read,       // handler for reading from the file
    .proc_lseek = seq_lseek,     // handler for setting the file position
    .proc_release = seq_release, // handler for closing the file
    };
    // Otherwise, if the kernel 5.6.0 or newer does not support new proc_ops, use file_operations.
    #else
    // Structure representing operations on a /proc file (without using proc_ops)
    static const struct file_operations my_file_ops = {
    .open = my_open,        // handler for opening the file
    .read = seq_read,       // handler for reading from the file
    .llseek = seq_lseek,    // handler for setting the file position
    .release = seq_release, // handler for closing the file
    };
    #endif
    ```




# procfs-4.h и procfs-4.c - создание "файла" в /proc. Эта программа задействует для управления файлом /proc библиотеку 
seq_file.

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

4. Создаем новый проект по пути - `/home/current_user/develop/kernel/proc/proc-4`.

5. В корне проекта создаем файлы `procfs-4.h` и `procfs-4.c`.

6. В корне проекта создаем `Makefile`.

7. Переходим в нашу директорию проекта:

    ```bash
    cd /home/current_user/develop/kernel/proc/proc-4
    ```

8. Используем `make` для компиляции кода:

    ```bash
    make
    ```

   Пример ввода и вывода:

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-4$ make
    make -C /lib/modules/6.5.0-14-generic/build M=/home/current_user/develop/kernel/proc/proc-4 modules
    make[1]: вход в каталог «/usr/src/linux-headers-6.5.0-14-generic»
    warning: the compiler differs from the one used to build the kernel
      The kernel was built by: aarch64-linux-gnu-gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
      You are using:           gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
      CC [M]  /home/current_user/develop/kernel/proc/proc-4/procfs-4.o
      MODPOST /home/current_user/develop/kernel/proc/proc-4/Module.symvers
      CC [M]  /home/current_user/develop/kernel/proc/proc-4/procfs-4.mod.o
      LD [M]  /home/current_user/develop/kernel/proc/proc-4/procfs-4.ko
      BTF [M] /home/current_user/develop/kernel/proc/proc-4/procfs-4.ko
    Skipping BTF generation for /home/current_user/develop/kernel/proc/proc-4/procfs-4.ko due to unavailability of vmlinux
    make[1]: выход из каталога «/usr/src/linux-headers-6.5.0-14-generic»
    ```
9. Получаем информацию о модуле:

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-4$ modinfo procfs-4.ko
    filename:       /home/shrekulka/develop/kernel/proc/proc-4/procfs-4.ko
    license:        GPL
    srcversion:     EBDB5A613BF353AE315D828
    depends:        
    name:           procfs_4
    vermagic:       6.5.0-14-generic SMP preempt mod_unload modversions aarch64
    ```

10. Убеждаемся, что модуль с именем "procfs_4" не загружен:

    ```bash
    sudo lsmod | grep procfs
    ```

11. После успешной компиляции загружаем модуль в ядро:

    ```bash
    sudo insmod procfs-4.ko
    ```

12. Проверяем загрузку модуля:

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-4$ sudo lsmod | grep procfs
	procfs_4               16384  0
    ```
    
13. При выполнении команды 'cat /proc/iter' происходит чтение содержимого файла /proc/iter, которое выводится в терминал.
    В данном случае, значение "0" является результатом работы функции my_seq_show, которая выводит текущее значение counter.

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-4$ cat /proc/iter
    0
    ```
    
14. В данном шаге происходит запись нового значения "Test data" в файл /proc/iter. После выполнения команды выводится 
    само новое значение.

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-4$ echo "Test data" /proc/iter
    Test data /proc/iter
    ```

15. При выполнении команды 'cat /proc/iter' происходит чтение содержимого файла /proc/iter после предыдущей записи.
    В данном случае, значение "1" является результатом работы функции my_seq_show, которая инкрементирует счетчик.

     ```bash
        current_user@current_user:~/develop/kernel/proc/proc-4$ cat /proc/iter
        1
     ```
 
16. Убеждаемся в наличии файла iter в системе в каталоге /proc.

    ```bash
    rent_user@current_user:~/develop/kernel/proc/proc-4$ ls /proc
    1     1486  2062  2261  2530  28    4766  66   95             kmsg
    100   1492  208   228   254   280   4854  67   96             kpagecgroup
    1007  15    209   229   255   281   4856  68   97             kpagecount
    1009  152   2095  23    256   2835  49    69   98             kpageflags
    101   155   21    230   2574  2837  4907  70   985            loadavg
    1012  1551  211   231   258   29    4910  71   988            locks
    1013  158   212   232   2588  2908  4920  72   989            mdstat
    1019  16    2122  233   259   296   4926  73   99             meminfo
    102   17    2123  234   26    2996  4983  74   990            misc
    103   1766  213   235   260   3     5     75   994            modules
    104   18    214   236   2616  3044  50    76   996            mounts
    1046  1862  2166  2361  2617  307   5010  77   997            net
    105   188   217   237   262   3076  5013  78   acpi           pagetypeinfo
    106   1880  219   238   263   317   5042  79   asound         partitions
    1060  1884  2190  2393  264   32    51    8    bootconfig     pressure
    107   189   2198  240   265   33    53    80   buddyinfo      schedstat
    1077  1896  22    2404  2658  34    54    81   bus            scsi
    108   1897  2200  241   266   35    544   82   cgroups        self
    1084  19    2213  2413  2668  38    545   824  cmdline        slabinfo
    11    1906  2217  242   267   385   546   825  consoles       softirqs
    111   1907  222   2432  268   386   55    826  cpuinfo        stat
    112   1913  2221  2444  269   39    56    827  crypto         swaps
    1181  1916  2226  2447  27    4     57    83   devices        sys
    1183  192   2227  2448  270   40    570   84   diskstats      sysrq-trigger
    1184  193   2229  245   271   41    573   85   driver         sysvipc
    119   194   223   2454  2710  4130  574   86   dynamic_debug  thread-self
    12    1942  2230  246   272   4165  575   860  execdomains    timer_list
    1203  195   2231  2466  273   4186  576   864  fb             tty
    1226  1956  224   247   2730  42    579   868  filesystems    uptime
    124   1965  2243  2474  2731  430   58    87   fs             version
    1260  1972  2244  2479  2733  44    580   879  interrupts     version_signature
    1275  1982  2245  248   2736  4436  59    88   iomem          vmallocinfo
    1277  1991  2246  249   274   45    6     89   ioports        vmstat
    129   2     2247  2490  275   46    60    9    irq            zoneinfo
    13    20    225   25    276   464   61    90   iter
    1359  2004  2252  251   277   466   62    91   kallsyms
    14    2040  2258  2517  278   4682  63    92   kcore
    1420  2049  2259  252   279   4686  64    93   keys
    1485  2051  2260  253   2795  47    65    94   key-users
    ```

17. Для удаления модуля используется команда:

    ```bash
    sudo rmmod procfs-4
    ```
    
18. После удаления модуля проверяем, что файл 'iter' больше не присутствует в /proc.

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-4$ ls /proc
    1     1486  2062  2261  2530  28    4766  66   95             kpagecgroup
    100   1492  208   228   254   280   4854  67   96             kpagecount
    1007  15    209   229   255   281   4856  68   97             kpageflags
    1009  152   2095  23    256   2835  49    69   98             loadavg
    101   155   21    230   2574  2837  4907  70   985            locks
    1012  1551  211   231   258   29    4910  71   988            mdstat
    1013  158   212   232   2588  2908  4920  72   989            meminfo
    1019  16    2122  233   259   296   4926  73   99             misc
    102   17    2123  234   26    2996  4983  74   990            modules
    103   1766  213   235   260   3     5     75   994            mounts
    104   18    214   236   2616  3044  50    76   996            net
    1046  1862  2166  2361  2617  307   5010  77   997            pagetypeinfo
    105   188   217   237   262   3076  5013  78   acpi           partitions
    106   1880  219   238   263   317   5060  79   asound         pressure
    1060  1884  2190  2393  264   32    51    8    bootconfig     schedstat
    107   189   2198  240   265   33    53    80   buddyinfo      scsi
    1077  1896  22    2404  2658  34    54    81   bus            self
    108   1897  2200  241   266   35    544   82   cgroups        slabinfo
    1084  19    2213  2413  2668  38    545   824  cmdline        softirqs
    11    1906  2217  242   267   385   546   825  consoles       stat
    111   1907  222   2432  268   386   55    826  cpuinfo        swaps
    112   1913  2221  2444  269   39    56    827  crypto         sys
    1181  1916  2226  2447  27    4     57    83   devices        sysrq-trigger
    1183  192   2227  2448  270   40    570   84   diskstats      sysvipc
    1184  193   2229  245   271   41    573   85   driver         thread-self
    119   194   223   2454  2710  4130  574   86   dynamic_debug  timer_list
    12    1942  2230  246   272   4165  575   860  execdomains    tty
    1203  195   2231  2466  273   4186  576   864  fb             uptime
    1226  1956  224   247   2730  42    579   868  filesystems    version
    124   1965  2243  2474  2731  430   58    87   fs             version_signature
    1260  1972  2244  2479  2733  44    580   879  interrupts     vmallocinfo
    1275  1982  2245  248   2736  4436  59    88   iomem          vmstat
    1277  1991  2246  249   274   45    6     89   ioports        zoneinfo
    129   2     2247  2490  275   46    60    9    irq
    13    20    225   25    276   464   61    90   kallsyms
    1359  2004  2252  251   277   466   62    91   kcore
    14    2040  2258  2517  278   4682  63    92   keys
    1420  2049  2259  252   279   4686  64    93   key-users
    1485  2051  2260  253   2795  47    65    94   kmsg
    ```

19. Это позволяет просмотреть системные логи, связанные с ядром Linux, и фильтрует строки, содержащие "procfs" -
    sudo journalctl --since "1 hour ago" | grep procfs:

    ```bash
    дек 05 13:12:58 current_user sudo[4555]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/proc/proc-4 ; 
    USER=root ; COMMAND=/usr/sbin/insmod procfs-4.ko
    дек 05 13:12:58 current_user kernel: procfs_4: loading out-of-tree module taints kernel.
    дек 05 13:12:58 current_user kernel: procfs_4: module verification failed: signature and/or required key missing - 
    tainting kernel
    дек 05 13:57:56 current_user sudo[5052]: current_user : TTY=pts/0 ; PWD=/home/current_user/develop/kernel/proc/proc-4 ; 
    USER=root ; COMMAND=/usr/sbin/rmmod procfs-4
    ```
    
20. Команда 'sudo dmesg | grep procfs' выводит сообщения ядра, связанные с модулем 'procfs-4'.

    ```bash
    current_user@current_user:~/develop/kernel/proc/proc-4$ sudo dmesg | grep procfs
    [  213.049925] procfs_4: loading out-of-tree module taints kernel.
    [  213.049934] procfs_4: module verification failed: signature and/or required key missing - tainting kernel
    ```



# Когда лучше использовать proc_ops, inode_operations, seq_file:

1. proc_ops - когда нужно быстро создать простой файл в /proc для статистики или отладки.

2. inode_operations - когда требуется низкоуровневое управление файлами, жесткими ссылками, правами доступа.

3. seq_file - удобно для вывода отладочных данных или статистики в /proc файлы. Позволяет легко организовать "пошаговый"
   вывод.

# Пояснения с примерами:

1. proc_ops - это специализированный интерфейс, оптимизированный конкретно для создания и управления файлами в /proc 
   файловой системе ядра. Он содержит такие элементы как (proc_ops - простой API, специально для /proc файлов):
   ```bash
   // Проверка версии ядра для использования proc_ops
   #if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 6, 0)
   #define HAVE_PROC_OPS
   #endif

   // Функция для чтения /proc файла
   static ssize_t my_read(struct file *filp, char __user *buffer, size_t length, loff_t *offset);

   // Функция для записи в /proc файл
   static ssize_t my_write(struct file *file, const char __user *buffer, size_t len, loff_t *off);
   
   // Функция для перемещения указателя положения в файле
   static loff_t my_llseek(struct file *file, loff_t offset, int whence);
   
   // Функция для обработки ioctl (ввод-вывод управления устройством)
   static long my_ioctl(struct file *file, unsigned int cmd, unsigned long arg);
   
   // Функция для отображения файла в память
   static int my_mmap(struct file *file, struct vm_area_struct *vma);
   
   // Функция для сброса данных в файл
   static int my_flush(struct file *file, fl_owner_t id);
   
   // Функция для синхронизации данных файла с диском
   static int my_fsync(struct file *file, loff_t start, loff_t end, int datasync);
   
   // Функция для управления асинхронными событиями файла
   static int my_fasync(int fd, struct file *file, int mode);

   // Используем структуру proc_ops, если ядро 5.6.0 или более новое и поддерживает новые proc_ops.
   #ifdef HAVE_PROC_OPS
   static const struct proc_ops my_file_ops = {
      .proc_read = my_read,        // обработчик чтение из файла
      .proc_write = my_write,      // обработчик запись в файл
      .proc_llseek = my_llseek,    // обработчик перемещения указателя положения в файле
      .proc_ioctl = my_ioctl,      // обработчик ioctl (ввод-вывод управления устройством)
      .proc_mmap = my_mmap,        // обработчик отображения файла в память
      .proc_flush = my_flush,      // обработчик сброса данных в файл
      .proc_fsync = my_fsync,      // обработчик синхронизации данных файла с диском
      .proc_fasync = my_fasync,    // обработчик управления асинхронными событиями файла
   };
   // В противном случае, если ядро 5.6.0 или более новое не поддерживает новые proc_ops, используем  file_operations.
   #else
   static const struct file_operations my_file_ops = {
   .read = my_read,        // обработчик чтение из файла
   .write = my_write,      // обработчик запись в файл
   .llseek = my_llseek,    // обработчик перемещения указателя положения в файле
   .ioctl = my_ioctl,      // обработчик ioctl (ввод-вывод управления устройством)
   .mmap = my_mmap,        // обработчик отображения файла в память
   .flush = my_flush,      // обработчик сброса данных в файл
   .fsync = my_fsync,      // обработчик синхронизации данных файла с диском
   .fasync = my_fasync,    // обработчик управления асинхронными событиями файла
   };
   #endif
   ```
   
2. inode_operations - это более низкоуровневый и универсальный API для реализации различных файловых систем. Содержит 
   расширенный набор операций для работы с индексными дескрипторами файлов (inode) (inode_operations - низкоуровневый и 
   универсальный):
   ```bash
   // Проверка версии ядра для использования proc_ops
   #if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 6, 0)
   #define HAVE_PROC_OPS
   #endif
   
   // Функция открытия файла
   static int my_open(struct inode* inode, struct file* file);
   
   // Функция закрытия файла
   static int my_release(struct inode* inode, struct file* file);
   
   // Функция создания файла
   static struct dentry *my_create(struct inode *dir, struct dentry *dentry, umode_t mode, bool excl);
   
   // Функция поиска файла в каталоге
   static struct dentry *my_lookup(struct inode *dir, struct dentry *dentry, unsigned int flags);
   
   // Функция создания жёсткой ссылки
   static int my_link(struct dentry *old_dentry, struct inode *dir, struct dentry *dentry);
   
   // Функция удаления файла
   static int my_unlink(struct inode *dir, struct dentry *dentry);
   
   // Функция создания символической ссылки
   static struct dentry *my_symlink(struct inode *dir, struct dentry *dentry, const char *symname);
   
   // Функция создания подкаталога
   static int my_mkdir(struct inode *dir, struct dentry *dentry, umode_t mode);
   
   // Функция удаления подкаталога
   static int my_rmdir(struct inode *dir, struct dentry *dentry);
   
   // Функция создания устройства
   static int my_mknod(struct inode *dir, struct dentry *dentry, umode_t mode, dev_t dev);
   
   // Функция переименования файла или каталога
   static int my_rename(struct inode *old_dir, struct dentry *old_dentry, struct inode *new_dir,
   struct dentry *new_dentry, unsigned int flags);
   
   // Функция установки атрибутов файла
   static int my_setattr(struct dentry *dentry, struct iattr *attr);
   
   // Функция проверки прав доступа к файлу
   static int my_permission(struct inode *inode, int mask);
   
   // Используем структуру proc_ops, если ядро 5.6.0 или более новое и поддерживает новые proc_ops.
   #ifdef HAVE_PROC_OPS
   // Структура, представляющая операции над индексными дескрипторами файлов (inode) с использованием proc_ops
   static struct proc_ops my_file_ops = {
       .proc_open = my_open,              // обработчик открытия файла
       .proc_release = my_release,        // обработчик закрытия файла
       .proc_create = my_create,          // обработчик создания файла
       .proc_lookup = my_lookup,          // обработчик поиска файла в каталоге
       .proc_link = my_link,              // обработчик создания жёсткой ссылки
       .proc_unlink = my_unlink,          // обработчик удаления файла
       .proc_symlink = my_symlink,        // обработчик создания символической ссылки
       .proc_mkdir = my_mkdir,            // обработчик создания подкаталога
       .proc_rmdir = my_rmdir,            // обработчик удаления подкаталога
       .proc_mknod = my_mknod,            // обработчик создания устройства
       .proc_rename = my_rename,          // обработчик переименования файла или каталога
       .proc_setattr = my_setattr,        // обработчик установки атрибутов файла
       .proc_permission = my_permission,  // обработчик проверки прав доступа к файлу
   };
   // В противном случае, если ядро 5.6.0 или более новое не поддерживает новые proc_ops, используем file_operations.
   #else
   // Структура, представляющая операции над индексными дескрипторами файлов (inode) без использования proc_ops
   static const struct file_operations my_file_ops = {
       .open = my_open,               // обработчик открытия файла
       .release = my_release,         // обработчик закрытия файла
       .create = my_create,           // обработчик создания файла
       .lookup = my_lookup,           // обработчик поиска файла в каталоге
       .link = my_link,               // обработчик создания жёсткой ссылки
       .unlink = my_unlink,           // обработчик удаления файла
       .symlink = my_symlink,         // обработчик создания символической ссылки
       .mkdir = my_mkdir,             // обработчик создания подкаталога
       .rmdir = my_rmdir,             // обработчик удаления подкаталога
       .mknod = my_mknod,             // обработчик создания устройства
       .rename = my_rename,           // обработчик переименования файла или каталога
       .setattr = my_setattr,         // обработчик установки атрибутов файла
       .permission = my_permission,   // обработчик проверки прав доступа к файлу
   };
   #endif
   ```

3. seq_file - это специальный интерфейс в /proc файловой системе, который позволяет упростить вывод данных в файлы /proc,
   используя последовательность функций (seq_file - для удобного вывода данных в /proc):
   ```bash
   // Обработчик начала последовательности
   static void *my_seq_start(struct seq_file *s, loff_t *pos);
   
   // Обработчик перехода к следующему шагу
   static void *my_seq_next(struct seq_file *s, void *v, loff_t *pos);
   
   // Обработчик завершения последовательности
   static void my_seq_stop(struct seq_file *s, void *v);
   
   // Пользовательская функция форматирования вывода
   static int my_seq_show(struct seq_file *s, void *v);
   
   // Добавление символов-заполнителей в буфер
   static void my_seq_pad(struct seq_file *m, char c);
   
   // Структура, представляющая операции над последовательностью (seq_operations)
   static struct seq_operations my_seq_ops = {
      .start = my_seq_start,        // обработчик начало последовательности
      .next = my_seq_next,          // обработчик переход к следующему шагу
      .stop = my_seq_stop,          // обработчик завершение последовательности
      .show = my_seq_show,          // обработчик вывод данных шага в буфер
      .pad = my_seq_paвб            // обработчик добавления символов-заполнителей в буфер
   };
   ```
   
## Пример:
   ```bash
   // Проверка версии ядра для использования proc_ops
   #if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 6, 0)
   #define HAVE_PROC_OPS
   #endif
   
   // Обработчик начала последовательности
   static void *my_seq_start(struct seq_file *s, loff_t *pos);
   
   // Обработчик перехода к следующему шагу
   static void *my_seq_next(struct seq_file *s, void *v, loff_t *pos);
   
   // Обработчик завершения последовательности
   static void my_seq_stop(struct seq_file *s, void *v);
   
   // Обработчик вывода данных шага в буфер
   static int my_seq_show(struct seq_file *s, void *v);
   
   // Структура, представляющая операции над последовательностью (seq_operations)
   static struct seq_operations my_seq_ops = {
       .start = my_seq_start,  // обработчик начала последовательности
       .next = my_seq_next,    // обработчик перехода к следующему шагу
       .stop = my_seq_stop,    // обработчик завершения последовательности
       .show = my_seq_show,    // обработчик вывода данных шага в буфер
   };
   
   // Используем структуру proc_ops, если ядро 5.6.0 или более новое и поддерживает новые proc_ops.
   #ifdef HAVE_PROC_OPS
   // Структура, представляющая операции над /proc файлом (используя proc_ops)
   static const struct proc_ops my_file_ops = {
       .proc_open = my_open,        // обработчик открытия файла
       .proc_read = seq_read,       // обработчик чтения из файла
       .proc_lseek = seq_lseek,     // обработчик установки позиции в файле
       .proc_release = seq_release, // обработчик закрытия файла
   };
   // В противном случае, если ядро 5.6.0 или более новое не поддерживает новые proc_ops, используем file_operations.
   #else
   // Структура, представляющая операции над /proc файлом (без использования proc_ops)
   static const struct file_operations my_file_ops = {
       .open = my_open,        // обработчик открытия файла
       .read = seq_read,       // обработчик чтения из файла
       .llseek = seq_lseek,    // обработчик установки позиции в файле
       .release = seq_release, // обработчик закрытия файла
   };
   #endif
   ```
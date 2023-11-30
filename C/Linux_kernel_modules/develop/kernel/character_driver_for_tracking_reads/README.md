*Creating a Linux Character Driver that Tracks File Reads*

**Steps in Ubuntu 23.10**

Brief Description:
The project implements a character driver, chardev, that tracks the number of reads from a file. Users can check 
registered character devices using the command cat /proc/devices. Writing to the device is not supported, and users are
notified of the invalidity of such an operation. The project ensures safe data interaction, preventing race conditions 
in parallel accesses.

Project Details:

Atomic Compare and Swap (CAS) instruction is utilized for individual access to shared resources, preventing race 
conditions.
The /proc/devices file displays registered character devices.
The chardev character driver is registered with the kernel and creates a device named /dev/chardev.
Upon opening the device file, the read counter is incremented, and a message is displayed.
Writing to the device is not supported, and attempts are processed with user notifications about the invalid operation.
Closing the device file decreases the usage counter, allowing subsequent accesses.

Notes:

The project is implemented in a multi-threaded environment using atomic operations to prevent race conditions.
Data read into the buffer is simply read, and the project does not provide additional processing for this data.
Writing to the device is not supported, making the project "read-only."

To run the code, follow these steps:

1. Compilation:
    Run make to compile your character driver. This will generate the object file chardev.o.
     ```bash
    current_user@current_user:~/develop/kernel/character_driver_for_tracking_reads$ make
    make -C /lib/modules/6.5.0-13-generic/build M=/home/current_user/develop/kernel/character_driver_for_tracking_reads 
    modules
    make[1]: Entering directory '/usr/src/linux-headers-6.5.0-13-generic'
    warning: the compiler differs from the one used to build the kernel
    The kernel was built by: aarch64-linux-gnu-gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
    You are using:           gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
    CC [M]  /home/current_user/develop/kernel/character_driver_for_tracking_reads/chardev.o
    MODPOST /home/current_user/develop/kernel/character_driver_for_tracking_reads/Module.symvers
    CC [M]  /home/current_user/develop/kernel/character_driver_for_tracking_reads/chardev.mod.o
    LD [M]  /home/current_user/develop/kernel/character_driver_for_tracking_reads/chardev.ko
    BTF [M] /home/current_user/develop/kernel/character_driver_for_tracking_reads/chardev.ko
    Skipping BTF generation for /home/current_user/develop/kernel/character_driver_for_tracking_reads/chardev.ko due to 
    unavailability of vmlinux
    make[1]: Leaving directory '/usr/src/linux-headers-6.5.0-13-generic'
     ```
2. Get information about the chardev.ko kernel module:
    ```bash
    current_user@current_user:~/develop/kernel/character_driver_for_tracking_reads$ modinfo chardev.ko
    filename:       /home/current_user/develop/kernel/character_driver_for_tracking_reads/chardev.ko
    license:        GPL
    srcversion:     214036C6E3CC6648710F82F
    depends:
    name:           chardev
    vermagic:       6.5.0-13-generic SMP preempt mod_unload modversions aarch64
    ```
3. Ensure the module named "chardev" is not loaded:
    ```bash
    current_user@current_user:~/develop/kernel/character_driver_for_tracking_reads$ sudo lsmod | grep chardev
    ```
4. After successful compilation, load the module into the kernel:
    ```bash
    sudo insmod chardev.ko
    ```
5. Check the results:
    After successfully loading the module, you can verify that the character device has been created and assigned a 
    major number. Also, you can use the command cat /proc/devices to view the list of registered character devices.
    ```bash
    current_user@current_user:~/develop/kernel/character_driver_for_tracking_reads$ cat /proc/devices
    # Character devices section:
    Character devices:
      1 mem                   # Memory device
      4 /dev/vc/0             # Virtual console
      4 tty                   # Terminal devices
      4 ttyS                  # Serial terminal devices
      5 /dev/tty              # Terminal devices
      5 /dev/console          # System console
      5 /dev/ptmx             # Pseudo terminal master
      5 ttyprintk             # Kernel message output
      7 vcs                   # Virtual console in memory
      10 misc                 # Miscellaneous devices
      13 input                # Input devices
      21 sg                   # Generic SCSI devices
      29 fb                   # Framebuffer devices
      81 video4linux          # Video4Linux devices
      89 i2c                  # I2C devices
     108 ppp                  # PPP (Point-to-Point Protocol) devices
     116 alsa                 # ALSA (Advanced Linux Sound Architecture) devices
     128 ptm                  # Pseudo terminal master
     136 pts                  # Pseudo terminals (slaves)
     180 usb                  # USB devices
     189 usb_device           # USB devices
     204 ttyMAX               # User terminal device
     207 ttymxc               # User terminal device
     226 drm                  # Direct Rendering Manager devices
     234 nvme-generic         # Generic NVMe devices
     235 nvme                 # NVMe devices
     236 rpmb                 # Replay Protected Memory Block devices
     237 ttyDBC               # User terminal device
     238 wwan_port            # WWAN (Wireless Wide Area Network) devices
     239 ttyOWL               # User terminal device
     240 ttyMSM               # User terminal device
     241 ttyAML               # User terminal device
     242 bsg                  # Block Scatter Gather devices
     243 watchdog             # Watchdog devices
     244 remoteproc           # Remote Processing Unit devices
     245 ptp                  # Precision Time Protocol devices
     246 pps                  # Pulse Per Second devices
     247 rtc                  # Real-Time Clock devices
     248 dma_heap             # Direct Memory Access heap devices
     249 dax                  # Direct Access devices
     250 dimmctl              # DIMM (Dual In-line Memory Module) control devices
     251 ndctl                # NVDIMM (Non-Volatile Dual In-line Memory Module) control devices
     252 tpm                  # Trusted Platform Module devices
     253 ttyMV                # User terminal device
     254 gpiochip             # GPIO (General Purpose Input/Output) devices
     261 accel                # Accelerometer devices
     509 chardev              # Custom character device (Your device)
     510 media                # Multimedia devices
     511 hidraw               # HID (Human Interface Device) raw input devices
    
    # Block devices section:
    Block devices:
      7 loop                  # Loop devices
      8 sd                    # SCSI disk devices
      9 md                    # Multiple disk devices (MD)
     11 sr                    # SCSI CD-ROM devices
     65 sd                    # SCSI disk devices
     66 sd                    # SCSI disk devices
     67 sd                    # SCSI disk devices
     68 sd                    # SCSI disk devices
     69 sd                    # SCSI disk devices
     70 sd                    # SCSI disk devices
     71 sd                    # SCSI disk devices
    128 sd                    # SCSI disk devices
    129 sd                    # SCSI disk devices
    130 sd                    # SCSI disk devices
    131 sd                    # SCSI disk devices
    132 sd                    # SCSI disk devices
    133 sd                    # SCSI disk devices
    134 sd                    # SCSI disk devices
    135 sd                    # SCSI disk devices
    179 mmc                   # MMC/SD card devices
    252 device-mapper         # Device mapper devices
    253 virtblk               # Virtual block devices
    254 mdp                   # MediaTek Display Port devices
    259 blkext                # Block extension devices
    ```
6. Interaction with the Character Device:
    You can interact with your character device through the file /dev/chardev. For example, you can use the command 
    sudo cat /dev/chardev to read data.
    ```bash
    current_user@current_user:~/develop/kernel/character_driver_for_tracking_reads$ sudo cat /dev/chardev
    I already told you 0 times Hello world!
    # Message read from the character device. The counter increases with each read.
    ```
7. Ensure the chardev Module is Loaded into the Kernel:
    ```bash
    current_user@current_user:~/develop/kernel/character_driver_for_tracking_reads$ sudo lsmod | grep chardev
    chardev                16384  0
    ```
8. Unload the Module:
    After testing and using your character driver, unload it from the kernel.
    ```bash
    current_user@current_user:~/develop/kernel/character_driver_for_tracking_reads$ sudo rmmod chardev
    ```
9. View Messages Related to the chardev Character Device in the System Log:
    ```bash
    current_user@current_user:~/develop/kernel/character_driver_for_tracking_reads$ sudo dmesg | grep chardev
    
    [ 9671.763564] chardev: loading out-of-tree module taints kernel.
    # Loading the chardev module. The message indicates that the module is loaded from outside and taints the kernel.
    
    [ 9671.763624] chardev: module verification failed: signature and/or required key missing - tainting kernel
    # Module verification failed, as the signature or required key is missing, also tainting the kernel.
    
    [ 9671.766107] Device created on /dev/chardev
    # Information about creating the /dev/chardev character device during module loading.
    
    [16754.225471] Device created on /dev/chardev
    # Information about creating the /dev/chardev character device secondarily (possibly after a reboot or another event).
    ```
10. Review Events Related to the chardev Character Device in the System Log:
    ```bash
    current_user@current_user:~/develop/kernel/character_driver_for_tracking_reads$ sudo journalctl --since "1 hour ago"
    | grep "chardev"
    
    Nov 29 20:46:36 current_user sudo[15878]: current_user : TTY=pts/0 ;
    PWD=/home/current_user/develop/kernel/character_driver_for_tracking_reads ; USER=root ;
    COMMAND=/usr/sbin/insmod chardev.ko
    # Record of the command to load the chardev.ko module using insmod.
    
    Nov 29 20:46:36 current_user kernel: Device created on /dev/chardev
    # Information about creating the /dev/chardev character device during module loading.
    
    Nov 29 20:49:03 current_user sudo[15895]: current_user : TTY=pts/0 ;
    PWD=/home/current_user/develop/kernel/character_driver_for_tracking_reads ; USER=root ;
    COMMAND=/usr/bin/cat /dev/chardev
    # Record of the command to read from the /dev/chardev character device using the cat command.
    
    Nov 29 20:56:48 current_user sudo[15925]: current_user : TTY=pts/0 ;
    PWD=/home/current_user/develop/kernel/character_driver_for_tracking_reads ; USER=root ;
    COMMAND=/usr/sbin/rmmod chardev
    # Record of the command to unload the chardev module using rmmod.
    ```
These steps assume that your system is set up for Linux kernel development, and you have the necessary header files and 
kernel configuration. Ensure that you have the required packages for Linux kernel development installed on your system.





*Создание символьного драйвера Linux, которsq сообщает, сколько раз происходило считывание из файла.*

**Шаги в Ubuntu 23.10**

Краткое описание:
Проект реализует символьный драйвер chardev, который подсчитывает количество считываний из файла. Пользователь может 
проверить зарегистрированные символьные устройства с помощью команды cat /proc/devices. Запись в устройство не 
поддерживается, и пользователю сообщается о недопустимости данной операции. Проект обеспечивает безопасное 
взаимодействие с данными, предотвращая состояние гонки при параллельных обращениях.

Детали проекта:

Используется атомарная инструкция сравнения с обменом (CAS) для обеспечения индивидуального доступа к общим ресурсам, 
предотвращая состояние гонки.
В файле /proc/devices отображаются зарегистрированные символьные устройства.
Символьный драйвер chardev регистрируется с ядром и создает устройство с именем /dev/chardev.
При открытии файла устройства увеличивается счетчик и выводится сообщение.
Запись в устройство не поддерживается, и происходит обработка таких попыток с уведомлением пользователей о 
недопустимости операции.
При закрытии файла устройства уменьшается счетчик использования, разрешая следующие обращения.
Замечания:

Проект реализован в многопоточной среде с использованием атомарных операций для предотвращения состояния гонки.
Данные, считываемые в буфер, просто считываются, и проект не предоставляет дополнительной обработки для этих данных.
Запись в устройство не поддерживается, что делает проект "только для чтения".

Для запуска кода, вам нужно выполнить следующие шаги:
1. Компиляция:
    Запустите make, чтобы скомпилировать ваш символьный драйвер. Это создаст объектный файл chardev.o.
    ```bash
	current_user@current_user:~/develop/kernel/character_driver_for_tracking_reads$ make
	make -C /lib/modules/6.5.0-13-generic/build M=/home/current_user/develop/kernel/character_driver_for_tracking_reads
    modules
	make[1]: вход в каталог «/usr/src/linux-headers-6.5.0-13-generic»
	warning: the compiler differs from the one used to build the kernel
	  The kernel was built by: aarch64-linux-gnu-gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
	  You are using:           gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
	  CC [M]  /home/current_user/develop/kernel/character_driver_for_tracking_reads/chardev.o
	  MODPOST /home/current_user/develop/kernel/character_driver_for_tracking_reads/Module.symvers
	  CC [M]  /home/current_user/develop/kernel/character_driver_for_tracking_reads/chardev.mod.o
	  LD [M]  /home/current_user/develop/kernel/character_driver_for_tracking_reads/chardev.ko
	  BTF [M] /home/current_user/develop/kernel/character_driver_for_tracking_reads/chardev.ko
	Skipping BTF generation for /home/current_user/develop/kernel/character_driver_for_tracking_reads/chardev.ko due to 
   unavailability of vmlinux
	make[1]: выход из каталога «/usr/src/linux-headers-6.5.0-13-generic»
    ```
2. Получение информации о ядерном модуле chardev.ko
	```bash
	current_user@current_user:~/develop/kernel/character_driver_for_tracking_reads$ modinfo chardev.ko
	filename:       /home/current_user/develop/kernel/character_driver_for_tracking_reads/chardev.ko
	license:        GPL
	srcversion:     214036C6E3CC6648710F82F
	depends:        
	name:           chardev
	vermagic:       6.5.0-13-generic SMP preempt mod_unload modversions aarch64
	```
	
3. Убеждаемся, что модуль с именем "chardev" не загружен:
	```bash
	current_user@current_user:~/develop/kernel/character_driver_for_tracking_reads$ sudo lsmod | grep chardev
	```
4. После успешной компиляции загружаем модуль в ядро:
    ```bash
    sudo insmod chardev.ko
    ```
5. Проверка результатов:
    После успешной загрузки модуля, вы можете проверить, что символьное устройство было создано и получило мажорный 
    номер. Также, вы можете использовать команду cat /proc/devices для просмотра списка зарегистрированных символьных 
    устройств.
	```bash
	current_user@current_user:~/develop/kernel/character_driver_for_tracking_reads$ cat /proc/devices
	# Секция символьных устройств:
	Character devices:
	  1 mem                   # Устройство памяти
	  4 /dev/vc/0             # Виртуальная консоль
	  4 tty                   # Терминальные устройства
	  4 ttyS                  # Серийные терминальные устройства
	  5 /dev/tty              # Терминальные устройства
	  5 /dev/console          # Системная консоль
	  5 /dev/ptmx             # Псевдотерминал мастер
	  5 ttyprintk             # Вывод сообщений в терминал ядра
	  7 vcs                   # Виртуальная консоль в памяти
	  10 misc                 # Различные устройства
	  13 input                # Входные устройства
	  21 sg                   # Универсальные SCSI-устройства
	  29 fb                   # Устройства кадрового буфера
	  81 video4linux          # Устройства Video4Linux
	  89 i2c                  # I2C-устройства
	 108 ppp                  # Устройства PPP (Point-to-Point Protocol)
	 116 alsa                 # Устройства ALSA (Advanced Linux Sound Architecture)
	 128 ptm                  # Псевдотерминал мастер
	 136 pts                  # Псевдотерминалы (слейвы)
	 180 usb                  # Устройства USB
	 189 usb_device           # Устройства USB
	 204 ttyMAX               # Пользовательское терминальное устройство
	 207 ttymxc               # Пользовательское терминальное устройство
	 226 drm                  # Устройства управления прямым доступом к рендерингу
	 234 nvme-generic         # Универсальные NVMe-устройства
	 235 nvme                 # NVMe-устройства
	 236 rpmb                 # Устройства блока Replay Protected Memory Block
	 237 ttyDBC               # Пользовательское терминальное устройство
	 238 wwan_port            # Устройства беспроводной связи WWAN
	 239 ttyOWL               # Пользовательское терминальное устройство
	 240 ttyMSM               # Пользовательское терминальное устройство
	 241 ttyAML               # Пользовательское терминальное устройство
	 242 bsg                  # Устройства блока Scatter Gather
	 243 watchdog             # Устройства слежения за состоянием системы (watchdog)
	 244 remoteproc           # Устройства удаленной обработки
	 245 ptp                  # Устройства Precision Time Protocol (PTP)
	 246 pps                  # Устройства Pulse Per Second (PPS)
	 247 rtc                  # Устройства часов реального времени (RTC)
	 248 dma_heap             # Устройства кучи прямого доступа (DMA heap)
	 249 dax                  # Устройства прямого доступа (DAX)
	 250 dimmctl              # Устройства управления DIMM
	 251 ndctl                # Устройства управления NVDIMM
	 252 tpm                  # Устройства модуля доверенной загрузки (Trusted Platform Module)
	 253 ttyMV                # Пользовательское терминальное устройство
	 254 gpiochip             # Устройства GPIO
	 261 accel                # Устройства акселерометра
	 509 chardev              # Пользовательское символьное устройство (Ваше устройство)
	 510 media                # Устройства мультимедиа
	 511 hidraw               # Устройства HID raw input

	# Секция блочных устройств:
	Block devices:
	  7 loop                  # Петлевые устройства
	  8 sd                    # SCSI-дисковые устройства
	  9 md                    # Устройства с несколькими дисками (MD)
	 11 sr                    # SCSI-устройства CD-ROM
	 65 sd                    # SCSI-дисковые устройства
	 66 sd                    # SCSI-дисковые устройства
	 67 sd                    # SCSI-дисковые устройства
	 68 sd                    # SCSI-дисковые устройства
	 69 sd                    # SCSI-дисковые устройства
	 70 sd                    # SCSI-дисковые устройства
	 71 sd                    # SCSI-дисковые устройства
	128 sd                    # SCSI-дисковые устройства
	129 sd                    # SCSI-дисковые устройства
	130 sd                    # SCSI-дисковые устройства
	131 sd                    # SCSI-дисковые устройства
	132 sd                    # SCSI-дисковые устройства
	133 sd                    # SCSI-дисковые устройства
	134 sd                    # SCSI-дисковые устройства
	135 sd                    # SCSI-дисковые устройства
	179 mmc                   # MMC/SD-карточные устройства
	252 device-mapper         # Устройства отображения дисков
	253 virtblk               # Виртуальные блочные устройства
	254 mdp                   # Устройства MediaTek Display Port
	259 blkext                # Устройства блочного расширения
	```

6. Взаимодействие с символьным устройством:
    Мы можете взаимодействовать с нашим символьным устройством через файл /dev/chardev. Например, мы можем
    воспользоваться командой sudo cat /dev/chardev для считывания данных.
	```bash
	current_user@current_user:~/develop/kernel/character_driver_for_tracking_reads$ sudo cat /dev/chardev
	I already told you 0 times Hello world!
	# Прочитанное сообщение из символьного устройства. Каждый раз при чтении увеличивается счетчик.
	```
7. Убеждаемся, что модуль chardev загружен в ядро.
	```bash
	current_user@current_user:~/develop/kernel/character_driver_for_tracking_reads$ sudo lsmod | grep chardev
	chardev                16384  0
	```
	
8. Выгрузка модуля:
    После завершения тестирования и использования вашего символьного драйвера, выгрузите его из ядра.
    ```bash
    current_user@current_user:~/develop/kernel/character_driver_for_tracking_reads$ sudo rmmod chardev
    ```
9. Просматриваем сообщения относящиеся к символьному устройству chardev в системном журнале.
	```bash
	current_user@current_user:~/develop/kernel/character_driver_for_tracking_reads$ sudo dmesg | grep chardev

	[ 9671.763564] chardev: loading out-of-tree module taints kernel.
	# Загрузка модуля chardev. Сообщение указывает на то, что модуль загружен извне и приводит к "заражению" ядра.

	[ 9671.763624] chardev: module verification failed: signature and/or required key missing - tainting kernel
	# Проверка модуля завершилась неудачно, так как отсутствует подпись или необходимый ключ, что также приводит к 
	# "заражению" ядра.

	[ 9671.766107] Device created on /dev/chardev
	# Информация о создании символьного устройства /dev/chardev при загрузке модуля.

	[16754.225471] Device created on /dev/chardev
	# Информация о создании символьного устройства /dev/chardev вторичным образом (возможно, после перезагрузки или 
	# другого события).
	```
10. Просматриваем события, связанные с символьным устройством chardev в системном журнале.
	```bash
	current_user@current_user:~/develop/kernel/character_driver_for_tracking_reads$ sudo journalctl --since "1 hour ago"
    | grep "chardev"
	
	ноя 29 20:46:36 current_user sudo[15878]: current_user : TTY=pts/0 ; 
    PWD=/home/current_user/develop/kernel/character_driver_for_tracking_reads ; USER=root ; 
    COMMAND=/usr/sbin/insmod chardev.ko
	# Запись о команде загрузки модуля chardev.ko с использованием insmod.

	ноя 29 20:46:36 current_user kernel: Device created on /dev/chardev
	# Информация о создании символьного устройства /dev/chardev при загрузке модуля.

	ноя 29 20:49:03 current_user sudo[15895]: current_user : TTY=pts/0 ; 
    PWD=/home/current_user/develop/kernel/character_driver_for_tracking_reads ; USER=root ; 
    COMMAND=/usr/bin/cat /dev/chardev
	# Запись о команде чтения из символьного устройства /dev/chardev с использованием команды cat.

	ноя 29 20:56:48 current_user sudo[15925]: current_user : TTY=pts/0 ; 
    PWD=/home/current_user/develop/kernel/character_driver_for_tracking_reads ; USER=root ; 
    COMMAND=/usr/sbin/rmmod chardev
	# Запись о команде выгрузки модуля chardev с использованием rmmod.
	```
Эти шаги предполагают, что ваша система настроена для разработки ядра Linux, и у вас есть необходимые заголовочные файлы
и конфигурация ядра. Убедитесь, что у вас установлены необходимые пакеты для разработки ядра Linux на вашей системе.

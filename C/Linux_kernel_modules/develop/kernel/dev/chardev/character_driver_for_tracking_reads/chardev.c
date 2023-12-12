// chardev.c: создаёт символьное устройство, которое сообщает, сколько раз происходило считывание из файла.

#include "chardev.h"

// Старший номер, присвоенный драйверу устройства.
static int major;

// msg, которое устройство будет выдавать при запросе.
static char msg[BUF_LEN + 1];

// Объявление внешней переменной указателя на структуру класса (struct class).
static struct class *cls;

// Инициализация структуры файловых операций для устройства.
struct file_operations chardev_fops = {
		.read = device_read,    // Указатель на функцию чтения.
		.write = device_write,  // Указатель на функцию записи.
		.open = device_open,    // Указатель на функцию открытия файла устройства.
		.release = device_release,  // Указатель на функцию закрытия файла устройства.
};


// Инициализация модуля ядра при загрузке.
static int __init chardev_init(void)
{
	// Регистрация символьного устройства в ядре Linux.
	major = register_chrdev(0, DEVICE_NAME, &chardev_fops);

	// Проверка успешности регистрации символьного устройства.
	if (major < 0)
	{
		pr_alert("Registering char device failed with %d\n", major);
		return major;
	}

	// Вывод информационного сообщения о присвоенном старшем номере символьного устройства.
	pr_info("I was assigned major number %d.\n", major);

	// Создание класса символьного устройства в /sys/class.
	// Проверка версии ядра Linux.
#if LINUX_VERSION_CODE >= KERNEL_VERSION(6, 4, 0)
	// Используется class_create без привязки к модулю для версий ядра 6.4.0 и выше.
    cls = class_create(DEVICE_NAME);
#else
	// Используется class_create с привязкой к текущему модулю для более старых версий ядра.
	cls = class_create(THIS_MODULE, DEVICE_NAME);
#endif

	// Создание символьного устройства в /dev.
	device_create(cls, NULL, MKDEV(major, 0), NULL, DEVICE_NAME);

	// Вывод информации о созданном символьном устройстве.
	pr_info("Device created on /dev/%s\n", DEVICE_NAME);

	return SUCCESS;
}


// Выход из модуля ядра при выгрузке.
static void __exit chardev_exit(void)
{
	// Уничтожение созданного устройства с использованием major и minor номеров.
	device_destroy(cls, MKDEV(major, 0));

	// Уничтожение созданного класса устройства.
	class_destroy(cls);

	// Отмена регистрации символьного устройства.
	unregister_chrdev(major, DEVICE_NAME);
}

// Методы.

// Вызывается, когда процесс пытается открыть файл устройства, например "sudo cat /dev/chardev".
static int device_open(struct inode *inode, struct file *file)
{
	static int counter = 0;

	/* Попытка атомарного изменения состояния устройства на CDEV_EXCLUSIVE_OPEN.
	 * Этот фрагмент кода использует атомарную операцию atomic_cmpxchg для изменения состояния устройства. Если текущее
	 * состояние устройства (already_open) равно CDEV_NOT_USED (то есть устройство не открыто), то оно атомарно
	 * изменяется на CDEV_EXCLUSIVE_OPEN (устройство открыто). Если операция успешна (устройство не было открыто), то
	 * возвращается -EBUSY в качестве ошибки, чтобы указать, что устройство уже открыто.
	*/
	if (atomic_cmpxchg(&already_open, CDEV_NOT_USED, CDEV_EXCLUSIVE_OPEN))
		return -EBUSY;  // Возврат ошибки, если устройство уже открыто.

	// Формирование сообщения с использованием счетчика и увеличение его значения.
	sprintf(msg, "I already told you %d times Hello world!\n", counter++);

	try_module_get(THIS_MODULE);  // Увеличение счетчика использования модуля.

	return SUCCESS;
}


// Вызывается, когда процесс закрывает файл устройства.
static int device_release(struct inode *inode, struct file *file)
{
	// Установка состояния устройства на CDEV_NOT_USED, что означает, что устройство больше не открыто.
	atomic_set(&already_open, CDEV_NOT_USED);

	// Декрементирует счетчик использования модуля. Если этот счетчик достигнет нуля (то есть модуль больше не
	// используется), модуль может быть выгружен.
	module_put(THIS_MODULE);

	return SUCCESS;
}


// Вызывается, когда процесс, который уже открыл файл устройства, пытается из него считать.
static ssize_t device_read(struct file *filp, char __user *buffer, size_t length, loff_t *offset)
{
	// Количество байт, обычно записываемых в буфер.
	int bytes_read = 0;

	// Указатель на сообщение, которое будет выдано при запросе.
	const char *msg_ptr = msg;

	// Если мы достигли конца сообщения.
	if (!*(msg_ptr + *offset))
	{
		*offset = 0; // Сброс смещения.
		return 0;    // Обозначение конца файла.
	}

	// Установка указателя на начало сообщения, с учетом текущего смещения.
	msg_ptr += *offset;

	// Помещение данных в буфер.
	while (length && *msg_ptr)
	{
		// Буфер находится в пользовательском сегменте данных, а не в сегменте ядра, поэтому присваивание "*" не
		// сработает. Тут нужно использовать put_user, которая копирует данные из сегмента ядра в пользовательский
		// сегмент.

		put_user(*(msg_ptr++), buffer++);   // Копирование данных из ядра в пользовательский буфер.
		length--;                           // Уменьшение оставшейся длины буфера.
		bytes_read++;                       // Увеличение счётчика прочитанных байт.
	}

	*offset += bytes_read; // Обновление смещения на количество прочитанных байт.

	// Возврат количества байт, помещённых в буфер.
	return bytes_read;
}


// Вызывается, когда процесс производит запись в файл устройства: echo "hi" > /dev/hello
static ssize_t device_write(struct file *filp, const char __user *buff, size_t len, loff_t *off)
{
	pr_alert("Sorry, this operation is not supported.\n");
	return -EINVAL;
}


// Инициализация модуля ядра при загрузке.
module_init(chardev_init);

// Выход из модуля ядра при выгрузке.
module_exit(chardev_exit);


MODULE_LICENSE("GPL");  // Установка лицензии модуля ядра.
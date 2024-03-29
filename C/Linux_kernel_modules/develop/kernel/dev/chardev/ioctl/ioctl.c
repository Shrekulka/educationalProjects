#include "ioctl.h"

// Статическая переменная для хранения основного номера устройства (major number).
static unsigned int test_ioctl_major = 0;

// Статическая переменная, предполагаемое количество устройств (может быть изменено по необходимости).
static unsigned int num_of_dev = 1;

// Структура cdev, представляющая зарегистрированное устройство.
static struct cdev test_ioctl_cdev;

// Статическая переменная, предполагаемое значение ioctl_num (по нашему запросу).
static int ioctl_num = 0;


// Функция test_ioctl_ioctl, которая будет обрабатывать IOCTL-команды.
// Принимает указатель на файл, код команды и аргументы IOCTL.
static long test_ioctl_ioctl(struct file *filp, unsigned int cmd, unsigned long arg)
{
	// Получение указателя на структуру данных устройства из private_data файла.
	struct test_ioctl_data *ioctl_data = filp->private_data;
	int retval = 0;         // Переменная для возвращаемого значения функции.
	unsigned char val;      // Переменная для хранения значения из структуры данных.
	struct ioctl_arg data;  // Структура для хранения данных от пользователя.

	// Инициализация структуры данных нулями.
	memset(&data, 0, sizeof(data));

	// Обработка различных IOCTL-команд с использованием switch.
	switch (cmd)
	{
		// 1. Обработка IOCTL-команды для установки данных от пользователя в структуру data.
		case IOCTL_VALSET:

			// 1. Проверка успешности копирования данных из пространства пользователя в ядро.
			if (copy_from_user(&data, (int __user *)arg, sizeof(data)))
			{
				retval = -EFAULT; // В случае ошибки копирования устанавливается код ошибки.
				goto done; // Переход к завершающему коду.
			}
			pr_alert("IOCTL set val:%x .\n", data.val);

			write_lock(&ioctl_data->lock);   // Захват блокировки записи.

			ioctl_data->val = data.val;      // Запись значения в структуру данных.

			write_unlock(&ioctl_data->lock); // Освобождение блокировки записи.

			break;

		// 2. Обработка IOCTL-команды для получения значения из устройства.
		case IOCTL_VALGET:
			read_lock(&ioctl_data->lock);   // Захват блокировки чтения.

			val = ioctl_data->val;          // Чтение значения из структуры данных.

			read_unlock(&ioctl_data->lock); // Освобождение блокировки чтения.

			data.val = val;                 // Запись значения в структуру для передачи обратно пользователю.

			// 2. Проверка успешности копирования данных из ядра в пространство пользователя.
			if (copy_to_user((int __user *)arg, &data, sizeof(data)))
			{
				retval = -EFAULT;  // В случае ошибки копирования устанавливается код ошибки.
				goto done;         // Переход к завершающему коду.
			}
			break;

		// 3. Обработка IOCTL-команды для получения числового значения из ядра.
		case IOCTL_VALGET_NUM:
			// Копирование значения ioctl_num в пространство пользователя.
			retval = __put_user(ioctl_num, (int __user *)arg);
			break;

		// 4. Обработка IOCTL-команды для установки числового значения из пространства пользователя в ядро.
		case IOCTL_VALSET_NUM:
			// Установка нового значения ioctl_num из пространства пользователя.
			ioctl_num = arg;
			break;

		// 5. В случае неизвестной IOCTL-команды устанавливается код ошибки.
		default:
			retval = -ENOTTY;
	}

// Метка done используется для обозначения точки выхода из функции. После завершения обработки IOCTL-команд и выполнения
// необходимых операций, управление переходит на эту метку, и функция возвращает значение retval.
done:
	return retval;
}

// Функция test_ioctl_read, предназначенная для чтения данных из устройства в пространство пользователя.
// Принимает указатель на файл, буфер для данных пользователя, количество байт для чтения и текущую позицию в файле.
static ssize_t test_ioctl_read(struct file *filp, char __user *buf, size_t count, loff_t *f_pos)
{
	// Получение указателя на структуру данных устройства из private_data файла.
	struct test_ioctl_data *ioctl_data = filp->private_data;

	unsigned char val; // Переменная для хранения значения из структуры данных.
	int retval;        // Переменная для возвращаемого значения функции.
	int i = 0;         // Переменная для использования в цикле.

	read_lock(&ioctl_data->lock);    // Захват блокировки чтения.
	val = ioctl_data->val;           // Чтение значения из структуры данных устройства.
	read_unlock(&ioctl_data->lock);  // Освобождение блокировки чтения.

	// Цикл для копирования значения в буфер пользователя.
	for (; i < count; i++)
	{
		// Проверка успешности копирования значения val в пространство пользователя.
		if (copy_to_user(&buf[i], &val, 1))
		{
			retval = -EFAULT; // В случае ошибки копирования устанавливается код ошибки.
			goto out;         // Переход к завершающему коду.
		}
	}
	retval = count; // Успешное завершение, возвращается количество скопированных байт.

// Метка out используется для обозначения точки выхода из функции. После выполнения всех операций и завершения функции,
// управление переходит на эту метку, и функция возвращает значение retval.
out:
	return retval;
}

// Функция test_ioctl_close, отвечающая за закрытие файла/устройства.
// Принимает указатель на inode и указатель на файл.
static int test_ioctl_close(struct inode *inode, struct file *filp)
{
	pr_alert("%s call.\n", __func__);

	// Проверка наличия указателя на private_data у файла.
	if (filp->private_data)
	{
		kfree(filp->private_data); // Освобождение памяти, выделенной для private_data.
		filp->private_data = NULL; // Установка private_data в NULL для избежания ошибок использования освобожденной памяти.
	}

	return 0; // Успешное завершение функции.
}

// Функция test_ioctl_open, отвечающая за открытие файла/устройства.
// Принимает указатель на inode и указатель на файл.
static int test_ioctl_open(struct inode *inode, struct file *filp)
{
	struct test_ioctl_data *ioctl_data; // Указатель на структуру данных устройства.

	pr_alert("%s call.\n", __func__);

	ioctl_data = kmalloc(sizeof(struct test_ioctl_data), GFP_KERNEL); // Выделение памяти для структуры данных.

	// Проверка успешности выделения памяти для структуры данных устройства.
	if (ioctl_data == NULL)
		return -ENOMEM; // В случае ошибки выделения памяти возвращается код ошибки ENOMEM.

	rwlock_init(&ioctl_data->lock);   // Инициализация блокировки чтения/записи.
	ioctl_data->val = 0xFF;           // Инициализация значения в структуре данных устройства.
	filp->private_data = ioctl_data;  // Присвоение private_data файлу.

	return 0; // Успешное завершение функции.
}

// Эта структура инициализирует операции с файлом для нашего драйвера.
static const struct file_operations fops = {
	.owner = THIS_MODULE,               // Указание модулю владельца данной структуры file_operations.
	.open = test_ioctl_open,            // Указание функции открытия файла.
	.release = test_ioctl_close,        // Указание функции закрытия файла.
	.read = test_ioctl_read,            // Указание функции чтения данных из файла.
	.unlocked_ioctl = test_ioctl_ioctl, // Указание функции обработки неблокирующих IOCTL-команд.
};

/**
 * ioctl_init - Инициализация драйвера при загрузке модуля.
 *
 * Эта функция выделяет ресурсы, регистрирует символьное устройство в системе и выполняет все необходимые
 * инициализационные шаги при загрузке модуля.
 *
 * Возвращаемые значения:
 *  0 в случае успешной инициализации, -1 в случае ошибки.
 */
static int ioctl_init(void)
{
	dev_t dev;               // Идентификатор устройства (состоит из младшего и старшего номеров).
	int alloc_ret = -1;      // Результат функции выделения региона устройства (номера устройства).
	int cdev_ret = -1;       // Результат функции добавления символьного устройства в ядро.

	// Выделение региона устройства с динамическим выделением номера устройства.
	alloc_ret = alloc_chrdev_region(&dev, 0, num_of_dev, DRIVER_NAME);

	// Переход к обработке ошибки, если выделение региона устройства завершилось неудачно.
	if (alloc_ret)
		goto error;

	test_ioctl_major = MAJOR(dev); // Получение основного номера устройства.

	// Инициализация структуры символьного устройства с указанием операций файла.
	cdev_init(&test_ioctl_cdev, &fops);

	// Добавление символьного устройства в систему.
	cdev_ret = cdev_add(&test_ioctl_cdev, dev, num_of_dev);

	// Переход к обработке ошибки, если добавление символьного устройства завершилось неудачно.
	if (cdev_ret)
		goto error;

	pr_alert("%s driver(major: %d) installed.\n", DRIVER_NAME, test_ioctl_major);

	return 0; // Успешное завершение функции.

error:

	// Отмена добавления символьного устройства, если ошибка произошла после этапа добавления.
	if (cdev_ret == 0)
		cdev_del(&test_ioctl_cdev);

	// Отмена выделения региона устройства, если ошибка произошла после этапа выделения.
	if (alloc_ret == 0)
		unregister_chrdev_region(dev, num_of_dev);

	return -1; // Возвращение кода ошибки.
}

/**
 * ioctl_exit - Завершение работы драйвера при выгрузке модуля.
 *
 * Эта функция освобождает ресурсы, удаляет символьное устройство из системы и выполняет все необходимые действия при
 * завершении работы модуля.
 */
static void ioctl_exit(void)
{
	// Создание идентификатора устройства с использованием основного номера и минорного номера 0.
	dev_t dev = MKDEV(test_ioctl_major, 0);

	// Удаление символьного устройства из системы.
	cdev_del(&test_ioctl_cdev);

	// Отмена выделения региона устройства.
	unregister_chrdev_region(dev, num_of_dev);

	pr_alert("%s driver removed.\n", DRIVER_NAME);
}

module_init(ioctl_init);   // Указание функции инициализации при загрузке модуля.
module_exit(ioctl_exit);   // Указание функции завершения при выгрузке модуля.

MODULE_LICENSE("GPL");                            // Указание лицензии для модуля.
MODULE_DESCRIPTION("This is test_ioctl module");  // Описание модуля.

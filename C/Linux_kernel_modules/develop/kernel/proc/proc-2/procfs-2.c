#include "procfs-2.h"

// Объявление статической структуры для представления файла /proc.
static struct proc_dir_entry *our_proc_file;

// Объявление статического символьного буфера для хранения данных.
static char procfs_buffer[PROCFS_MAX_SIZE];

// Объявление переменной для хранения размера буфера.
static unsigned long procfs_buffer_size = 0;

// Определение функции для чтения файла /proc.
static ssize_t procfile_read(struct file *filePointer, char __user *buffer, size_t buffer_length, loff_t *offset)
{
	// Инициализация строки символов.
	char s[13] = "HelloWorld!\n";

	// Получение размера строки.
	int len = sizeof(s);

	// Инициализация возвращаемого значения.
	ssize_t ret = len;

	// Проверка условий считывания данных из /proc.
	if (*offset >= len || copy_to_user(buffer, s, len))
	{
		pr_info("copy_to_user failed\n");
		// Установка результата в 0 в случае ошибки.
		ret = 0;
	}
	else
	{
		pr_info("procfile read %s\n", filePointer->f_path.dentry->d_name.name);
		// Увеличение смещения на размер считанных данных.
		*offset += len;
	}
	// Возвращение результата считывания.
	return ret;
}

// Определение функции для записи в файл /proc.
static ssize_t procfile_write(struct file *file, const char __user *buff, size_t len, loff_t *off)
{
	// Установка размера буфера.
	procfs_buffer_size = len;

	// Проверка и усечение размера буфера.
	if (procfs_buffer_size > PROCFS_MAX_SIZE)
		procfs_buffer_size = PROCFS_MAX_SIZE;

	// Копирование данных из пространства пользователя в пространство ядра.
	if (copy_from_user(procfs_buffer, buff, procfs_buffer_size))
		// Возвращение ошибки в случае неудачи копирования данных.
		return -EFAULT;

	// Установка нулевого символа в конце данных.
	procfs_buffer[procfs_buffer_size & (PROCFS_MAX_SIZE - 1)] = '\0';

	pr_info("procfile write %s\n", procfs_buffer);
	// Возвращение размера записанных данных.
	return procfs_buffer_size;
}

// Определение структуры операций с файлом, совместимой с версиями ядра.
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

// Определение функции инициализации модуля ядра.
static int __init procfs2_init(void)
{
	// Создание файла /proc/buffer1k с правами доступа 0644 и связывание его с операциями proc_file_fops.
	our_proc_file = proc_create(PROCFS_NAME, 0644, NULL, &proc_file_fops);

	// Обработка ошибки при создании файла /proc/buffer1k.
	if (NULL == our_proc_file)
	{
		// Удаление файла /proc/buffer1k в случае ошибки.
		proc_remove(our_proc_file);

		// Вывод предупреждения об ошибке.
		pr_alert("Error: Could not initialize /proc/%s\n", PROCFS_NAME);

		// Возвращение кода ошибки.
		return -ENOMEM;
	}

	// Вывод информации о создании файла /proc/buffer1k.
	pr_info("/proc/%s created\n", PROCFS_NAME);

	// Возвращение успешного результата инициализации.
	return 0;
}

// Определение функции выхода из модуля ядра.
static void __exit procfs2_exit(void)
{
	// Удаление файла /proc/buffer1k.
	proc_remove(our_proc_file);

	pr_info("/proc/%s removed\n", PROCFS_NAME);
}

// Регистрация функций инициализации и выхода из модуля
module_init(procfs2_init);
module_exit(procfs2_exit);

// Указание лицензии GPL для модуля ядра.
MODULE_LICENSE("GPL");

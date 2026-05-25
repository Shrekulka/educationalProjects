// procfs-1.h и procfs-1.c – данный код демонстрирует создание, чтение и удаление файла /proc/helloworld с использованием
// файловой системы /proc в ядре Linux.
#include "procfs-1.h"

// Структура для представления файла в /proc
static struct proc_dir_entry *our_proc_file;

// Функция чтения из файла /proc/helloworld
static ssize_t procfile_read(struct file *filePointer, char __user *buffer, size_t buffer_length, loff_t *offset)
{
	char s[13] = "HelloWorld!\n";  // Строка для вывода

	int len = sizeof(s);  // Длина строки

	ssize_t ret = len;  // Инициализация возвращаемого значения

	// Проверка, не превышено ли смещение или не произошла ли ошибка при копировании в буфер пользователя
	if (*offset >= len || copy_to_user(buffer, s, len))
	{
		pr_info("copy_to_user failed\n");
		ret = 0;  // Установка возвращаемого значения в 0
	}
	else
	{
		pr_info("procfile read %s\n", filePointer->f_path.dentry->d_name.name);
		*offset += len;  // Увеличение смещения
	}

	return ret;  // Возвращение значения
}

#ifdef HAVE_PROC_OPS
// Определение структуры proc_ops для ядер версии 5.6.0 и новее
static const struct proc_ops proc_file_fops = {
    .proc_read = procfile_read,  // Указание функции чтения
};
#else
// Определение структуры file_operations для ядер версии старше 5.6.0
static const struct file_operations proc_file_fops = {
		.read = procfile_read,  // Указание функции чтения
};
#endif

// Инициализация модуля
static int __init procfs1_init(void)
{
	// Создание файла /proc/helloworld
	our_proc_file = proc_create(procfs_name, 0644, NULL, &proc_file_fops);

	// Проверка успешности создания файла
	if (NULL == our_proc_file)
	{
		proc_remove(our_proc_file);  // Удаление файла в случае ошибки
		pr_alert("Error: Could not initialize /proc/%s\n", procfs_name);
		return -ENOMEM;  // Возвращение ошибки нехватки памяти
	}

	pr_info("/proc/%s created\n", procfs_name);
	return 0;  // Возвращение успешного завершения
}

// Выход из модуля
static void __exit procfs1_exit(void)
{
	proc_remove(our_proc_file);  // Удаление файла /proc/helloworld
	pr_info("/proc/%s removed\n", procfs_name);
}

// Регистрация функций инициализации и выхода из модуля
module_init(procfs1_init);
module_exit(procfs1_exit);

MODULE_LICENSE("GPL");  // Указание лицензии модуля

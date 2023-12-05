#include "procfs-3.h"

// Глобальная переменная, представляющая файл в /proc.
static struct proc_dir_entry *our_proc_file;

// Буфер для хранения данных, читаемых и записываемых в /proc файл.
static char procfs_buffer[PROCFS_MAX_SIZE];

// Размер буфера, используемый для отслеживания количества байт в буфере.
static unsigned long procfs_buffer_size = 0;

/* Функция чтения данных из /proc файла.
 * - struct file *filp: указатель на структуру файла, представляющую открытый /proc файл.
 * - char __user *buffer: указатель на буфер в пространстве пользователя, в который будут записаны данные.
 * - size_t length: размер буфера, в который можно записать данные.
 * - loff_t *offset: указатель на переменную, хранящую смещение в файле. */
static ssize_t procfs_read(struct file *filp, char __user *buffer, size_t length, loff_t *offset)
{
	static int finished = 0; // Инициализация флага, указывающего, завершено ли чтение.

	// Проверка, был ли уже завершен вывод.
	if (finished)
	{
		pr_debug("procfs_read: END\n");
		finished = 0; // Сброс флага завершения чтения.
		return 0;     // Возвращение 0, так как чтение завершено.
	}

	finished = 1;    // Установка флага завершения чтения.

	// Копирование данных из ядерного буфера (procfs_buffer) в пространство пользователя, представленное буфером (buffer).
	// Аргументы:
	// - buffer: Указатель на буфер в пространстве пользователя, в который будут скопированы данные.
	// - procfs_buffer: Указатель на ядерный буфер, из которого будут скопированы данные.
	// - procfs_buffer_size: Размер данных, который нужно скопировать.

	// Если копирование данных не удалось (например, из-за ошибки доступа к памяти),
	// то функция возвращает код ошибки -EFAULT, указывающий на ошибку копирования данных.
	if (copy_to_user(buffer, procfs_buffer, procfs_buffer_size))
		return -EFAULT;

	pr_debug("procfs_read: read %lu bytes\n", procfs_buffer_size);
	return procfs_buffer_size; // Возвращение количества прочитанных байт.
}

/* Функция записи данных в /proc файл.
 * Аргументы функции:
 * - struct file *file: указатель на структуру файла, представляющую открытый /proc файл.
 * - const char __user *buffer: указатель на буфер в пространстве пользователя, из которого будут считаны данные для записи.
 * - size_t len: размер буфера с данными для записи.
 * - loff_t *off: указатель на переменную, хранящую смещение в файле.*/
static ssize_t procfs_write(struct file *file, const char __user *buffer, size_t len, loff_t *off)
{
	// Проверка, превышает ли размер данных для записи максимально допустимый размер.
	if (len > PROCFS_MAX_SIZE)
		procfs_buffer_size = PROCFS_MAX_SIZE;
	else
		procfs_buffer_size = len;

	// Копирование данных из пространства пользователя в ядерное пространство.
	// Аргументы:
	// - procfs_buffer: Указатель на ядерный буфер, в который будут скопированы данные.
	// - buffer: Указатель на буфер в пространстве пользователя, из которого будут скопированы данные.
	// - procfs_buffer_size: Размер данных, который нужно скопировать.

	// Если копирование данных не удалось (например, из-за ошибки доступа к памяти),
	// то функция возвращает код ошибки -EFAULT, указывающий на ошибку копирования данных.
	if (copy_from_user(procfs_buffer, buffer, procfs_buffer_size))
		return -EFAULT;

pr_debug("procfs_write: write %lu bytes\n", procfs_buffer_size);
	return procfs_buffer_size; // Возвращение количества записанных байт.
}

// Функция открытия /proc файла.
// Аргументы функции:
// - struct inode *inode: указатель на структуру inode, представляющую файловый узел в системе файлов.
// - struct file *file: указатель на структуру file, представляющую открытый файл.
static int procfs_open(struct inode *inode, struct file *file)
{
	// Увеличение счетчика ссылок на модуль, представляющий текущий ядреный модуль.
	try_module_get(THIS_MODULE);

	// Возвращение 0, что означает успешное открытие файла.
	return 0;
}

// Функция закрытия /proc файла.
// Аргументы функции:
// - struct inode *inode: указатель на структуру inode, представляющую файловый узел в системе файлов.
// - struct file *file: указатель на структуру file, представляющую открытый файл.
static int procfs_close(struct inode *inode, struct file *file)
{
	// Уменьшение счетчика ссылок на модуль, представляющий текущий ядреный модуль.
	module_put(THIS_MODULE);

	// Возвращение 0, что означает успешное закрытие файла.
	return 0;
}

#ifdef HAVE_PROC_OPS
// Используем структуру proc_ops, если ядро 5.6.0 или более новое и поддерживает новые proc_ops.
static struct proc_ops file_ops_4_our_proc_file = {
    .proc_read = procfs_read,     // Функция чтения данных из /proc файла.
    .proc_write = procfs_write,   // Функция записи данных в /proc файл.
    .proc_open = procfs_open,      // Функция открытия /proc файла.
    .proc_release = procfs_close,  // Функция закрытия /proc файла.
};
#else
// В противном случае, если ядро 5.6.0 или более новое не поддерживает новые proc_ops, используем  file_operations.
static const struct file_operations file_ops_4_our_proc_file = {
		.read = procfs_read,     // Функция чтения данных из /proc файла.
		.write = procfs_write,   // Функция записи данных в /proc файл.
		.open = procfs_open,      // Функция открытия /proc файла.
		.release = procfs_close,  // Функция закрытия /proc файла.
};
#endif

// Инициализация модуля при загрузке.
static int __init procfs3_init(void)
{
	// Создание /proc файла с указанными параметрами и набором операций file_ops_4_our_proc_file.
	our_proc_file = proc_create(
			PROCFS_ENTRY_FILENAME,    // Имя создаваемого /proc файла.
			0644,                    // Права доступа к /proc файлу (восьмеричное представление).
			NULL,                    // Родительская директория (в данном случае, используется корневая директория).
			&file_ops_4_our_proc_file // Набор операций, определенных в file_ops_4_our_proc_file.
	);


	// Проверка успешности создания /proc файла.
	if (our_proc_file == NULL)
	{
		// В случае ошибки, удаляем созданный /proc файл и выводим сообщение об ошибке в журнал ядра.
		remove_proc_entry(PROCFS_ENTRY_FILENAME, NULL);
		pr_debug("Error: Could not initialize /proc/%s\n", PROCFS_ENTRY_FILENAME);
		return -ENOMEM;  // Возвращаем ошибку нехватки памяти.
	}

	// Установка размера /proc файла в 80 байт.
	proc_set_size(our_proc_file, 80);

	// Установка прав доступа для /proc файла.
	proc_set_user(our_proc_file, GLOBAL_ROOT_UID, GLOBAL_ROOT_GID);

	// Вывод в журнал ядра сообщения о успешном создании /proc файла.
	pr_debug("/proc/%s created\n", PROCFS_ENTRY_FILENAME);

	return 0;  // Возвращаем успешное выполнение.
}

// Выходная функция модуля, вызываемая при выгрузке модуля ядра.
static void __exit procfs3_exit(void)
{
	// Удаление /proc файла при выгрузке модуля.
	remove_proc_entry(PROCFS_ENTRY_FILENAME, NULL);
	pr_debug("/proc/%s removed\n", PROCFS_ENTRY_FILENAME);
}


module_init(procfs3_init); // Определение функции инициализации модуля, вызываемой при загрузке модуля ядра.
module_exit(procfs3_exit); // Определение функции выгрузки модуля, вызываемой при выгрузке модуля ядра.

MODULE_LICENSE("GPL"); // Указание лицензии для модуля.

// procfs-4.h и procfs-4.c - создание "файла" в /proc
// Эта программа задействует для управления файлом /proc библиотеку seq_file.
#include "procfs-4.h"

/* Эта функция вызывается в начале последовательности.
 * То есть, когда:
 *   - первый раз считывается файл /proc
 *   - после завершения функции (в конце последовательности)
 */
static void *my_seq_start(struct seq_file *s, loff_t *pos)
{
	// Статическая переменная для хранения значения счетчика
	static unsigned long counter = 0;

	/* Начинаем новую последовательность? */
	if (*pos == 0)
	{
		// Да => возвращается ненулевое значение для начала последовательности
		return &counter;
	}
	// Нет => это конец последовательности, возвращается NULL для завершения считывания
	*pos = 0;
	return NULL;
}

// Эта функция вызывается после начала последовательности.
// Ее вызов повторяется до возвращения значения NULL (затем последовательность завершается).
static void *my_seq_next(struct seq_file *s, void *v, loff_t *pos)
{
	// Приведение указателя к типу unsigned long
	unsigned long *tmp_v = (unsigned long *)v;

	// Увеличение счетчика
	(*tmp_v)++;

	// Увеличение положения в последовательности
	(*pos)++;

	return NULL;
}


// Эта функция вызывается в конце последовательности.
static void my_seq_stop(struct seq_file *s, void *v)
{
	// Делать нечего, используем в start() статическое значение.
}

/* Эта функция вызывается для каждого «шага» последовательности. */
static int my_seq_show(struct seq_file *s, void *v)
{
	// Приведение указателя v к типу loff_t, чтобы получить доступ к значению положения в последовательности
	loff_t *spos = (loff_t *)v;

	// Вывод значения шага в буфер последовательности
	seq_printf(s, "%Ld\n", *spos);

	// Возвращение 0, чтобы указать успешное выполнение
	return 0;
}

// Эта структура формирует "функцию" для управления последовательностью.
static struct seq_operations my_seq_ops = {
		.start = my_seq_start,  // Обработчик начала последовательности
		.next = my_seq_next,    // Обработчик перехода к следующему шагу
		.stop = my_seq_stop,    // Обработчик завершения последовательности
		.show = my_seq_show,    // Обработчик вывода данных шага в буфер
};

// Эта функция вызывается при открытии файла /proc.
static int my_open(struct inode *inode, struct file *file)
{
	// Использование seq_open для открытия файла и передачи управления операциям последовательности
	return seq_open(file, &my_seq_ops);
};

// Используем структуру proc_ops, если ядро 5.6.0 или более новое и поддерживает новые proc_ops.
#ifdef HAVE_PROC_OPS
static const struct proc_ops my_file_ops = {
    .proc_open = my_open,        // Обработчик открытия файла
    .proc_read = seq_read,       // Обработчик чтения из файла
    .proc_lseek = seq_lseek,     // Обработчик установки позиции чтения/записи
    .proc_release = seq_release, // Обработчик закрытия файла
};
// В противном случае, если ядро 5.6.0 или более новое не поддерживает новые proc_ops, используем  file_operations.
#else
static const struct file_operations my_file_ops = {
		.open = my_open,        // Обработчик открытия файла
		.read = seq_read,       // Обработчик чтения из файла
		.llseek = seq_lseek,    // Обработчик установки позиции чтения/записи
		.release = seq_release, // Обработчик закрытия файла
};
#endif


// Функция инициализации модуля
static int __init procfs4_init(void)
{
	// Объявление указателя на структуру proc_dir_entry для работы с файловой системой /proc
	struct proc_dir_entry *entry;

	// Создание файла /proc с заданными операциями
	entry = proc_create(PROC_NAME, 0, NULL, &my_file_ops);

	// Проверка на успешное создание файла /proc
	if (entry == NULL)
	{
		// В случае ошибки удаление созданной записи
		remove_proc_entry(PROC_NAME, NULL);
		pr_debug("Error: Could not initialize /proc/%s\n", PROC_NAME);
		// Возврат ошибки нехватки памяти
		return -ENOMEM;
	}
	return 0; // Возврат успешного выполнения
}

// Функция выхода из модуля
static void __exit procfs4_exit(void)
{
	// Удаление файла /proc при выходе из модуля
	remove_proc_entry(PROC_NAME, NULL);
	pr_debug("/proc/%s removed\n", PROC_NAME);
}


module_init(procfs4_init); // Макрос указывающий на функцию инициализации модуля
module_exit(procfs4_exit); // Макрос указывающий на функцию выхода из модуля

MODULE_LICENSE("GPL"); // Лицензия модуля

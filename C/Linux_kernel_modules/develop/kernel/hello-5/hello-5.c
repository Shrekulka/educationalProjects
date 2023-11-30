/* Модуль ядра Linux поддерживает передачу аргументов командной строки при его
 * загрузке. Эти аргументы, указанные после команды загрузки модуля (например,
 * insmod), могут влиять на конфигурацию и параметры модуля. Для передачи
 * значений переменных, включая массивы, используется макрос module_param_array.
 * Этот макрос позволяет модулю принимать массивы данных, предоставляемые
 * пользователем при загрузке модуля.
*/
#include <linux/init.h>
#include <linux/module.h>
#include <linux/moduleparam.h>
#include <linux/kernel.h>

// Информация о модуле
MODULE_LICENSE("GPL");
MODULE_AUTHOR("shrekulka");
MODULE_DESCRIPTION("Pass command line arguments to a kernel module");


// Определяем переменные myshort, myint, mylong, mystring, myintarray и arr_argc
static short int myshort = 1;
static int myint = 420;
static long int mylong = 9999;
static char *mystring = "blah";
static int myintarray[2] = {420, 420};
static int arr_argc = 0;

/*
 * В загружаемых модулях ядра Linux вы можете передавать аргументы командной
 * строки используя макрос module_param().
 * Этот макрос module_param настраивает передачу значения из аргумента командной
 * строки. Он принимает три аргумента: имя переменной (my_variable), её тип
 * (int), и разрешения для соответствующего файла в sysfs (в данном случае, 0
 * означает, что файл не будет создан).
 * Разрешения могут принимать следующие значения:
 * S_IRUGO (0444): Позволяет читать значение переменной из файла в sysfs.
 * S_IWUSR (0200): Позволяет изменять значение переменной из файла в sysfs.
 * S_IRUGO | S_IWUSR (0644): Комбинация прав на чтение и запись.
 * S_IWUSR | S_IWGRP | S_IWOTH (0222): Позволяет любому пользователю записывать
 * значение.
 */

// Добавляем переменные myshort, myint, mylong в sysfs с разрешениями для чтения
// и записи
module_param(myshort, short, S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP);
module_param(myint, int, S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH);
module_param(mylong, long, S_IRUSR);

// Добавляем переменные mystring, myintarray в sysfs без разрешений для чтения и
// записи
module_param(mystring, charp, 0000);

/* Для массивов:
 * module_param_array(name, type, num, perm);
 * Первым аргументом идёт имя параметра (в данном случае массива).
 * Второй аргумент – это тип элементов массива.
 * Третий – это указатель на переменную, которая будет хранить количество элементов
 * массива, инициализированных пользователем при загрузке модуля.
 * Четвёртый аргумент – это биты разрешения.
 */
module_param_array(myintarray, int, &arr_argc, 0000);


// Добавляем описания для переменных myshort, myint, mylong, mystring, myintarray
MODULE_PARM_DESC(myshort, "A short integer");
MODULE_PARM_DESC(myint, "An integer");
MODULE_PARM_DESC(mylong, "A long integer");
MODULE_PARM_DESC(mystring, "A character string");
MODULE_PARM_DESC(myintarray, "An array of integers");


// Определяем функцию инициализации модуля
static int __init hello_5_init(void)
{
    int i;

    pr_info("Hello, world 5\n=============\n");
    pr_info("myshort is a short integer: %hd\n", myshort);
    pr_info("myint is an integer: %d\n", myint);
    pr_info("mylong is a long integer: %ld\n", mylong);
    pr_info("mystring is a string: %s\n", mystring);

    for (i = 0; i < ARRAY_SIZE(myintarray); i++)
	{
        pr_info("myintarray[%d] = %d\n", i, myintarray[i]);
	}
    pr_info("got %d arguments for myintarray.\n", arr_argc);

    return 0;
}

// Определяем функцию выгрузки модуля
static void __exit hello_5_exit(void)
{
    pr_info("Goodbye, world 5\n");
}

module_init(hello_5_init);
module_exit(hello_5_exit);
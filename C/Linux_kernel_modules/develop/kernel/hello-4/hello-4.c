// Передача аргументов командной строки модулю ядра

#include <linux/init.h>
#include <linux/module.h>
#include <linux/moduleparam.h>

// Объявление переменной, которая будет принимать значение из аргумента командной строки
static int my_variable = 15;

/*
 * В загружаемых модулях ядра Linux вы можете передавать аргументы командной строки используя макрос module_param().
 * Этот макрос module_param настраивает передачу значения из аргумента командной строки. Он принимает три аргумента: имя
 * переменной (my_variable), её тип (int), и разрешения для соответствующего файла в sysfs (в данном случае, 0 означает,
 * что файл не будет создан).
 * Разрешения могут принимать следующие значения:
 * S_IRUGO (0444): Позволяет читать значение переменной из файла в sysfs.
 * S_IWUSR (0200): Позволяет изменять значение переменной из файла в sysfs.
 * S_IRUGO | S_IWUSR (0644): Комбинация прав на чтение и запись.
 * S_IWUSR | S_IWGRP | S_IWOTH (0222): Позволяет любому пользователю записывать значение.
 */
module_param(my_variable, int, 0);

// Функция инициализации модуля
static int __init my_init_function(void) 
{
    pr_info("My module is loaded! my_variable=%d\n", my_variable);
    return 0;
}

// Функция выхода из модуля
static void __exit my_exit_function(void) 
{
    pr_info("My module is unloaded!\n");
}

// Регистрация функций инициализации и выхода
module_init(my_init_function);
module_exit(my_exit_function);

// Информация о модуле
MODULE_LICENSE("GPL");
MODULE_AUTHOR("shrekulka");
MODULE_DESCRIPTION("Pass command line arguments to a kernel module");


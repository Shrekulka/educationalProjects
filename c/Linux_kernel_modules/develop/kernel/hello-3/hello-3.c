// hello-3.c – демонстрация макросов __initdata, __init и __exit, а также документирование модуля.

#include <linux/init.h>   // Необходим для макросов
#include <linux/kernel.h> // Необходим для pr_info()
#include <linux/module.h> // Необходим для всех модулей


MODULE_LICENSE("GPL");                 // Указание на лицензию модуля
MODULE_AUTHOR("shrekulka");            // Указание автора модуля
MODULE_DESCRIPTION("A sample driver"); // Описание модуля
MODULE_VERSION("1.0");                 // Добавление информации о версии модуля


// Инициализация переменной с атрибутом __initdata
static int hello3_data __initdata = 3;


// Функция, вызываемая при загрузке модуля.
static int __init hello_3_init(void)
{
	pr_info("Hello, world %d\n", hello3_data);
	return 0;
}

// Функция, вызываемая при выгрузке модуля.
static void __exit hello_3_exit(void)
{
	pr_info("Goodbye, world 3\n");
}

module_init (hello_3_init); // Указание функции инициализации модуля
module_exit(hello_3_exit);   // Указание функции выхода из модуля

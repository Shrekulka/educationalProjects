// hello-2.c – демонстрация макросов module_init() и module_exit().
// Этот вариант предпочтительнее использования init_module() и cleanup_module().

#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>

// Определение функции, вызываемой при загрузке модуля.
static int __init hello_2_init(void)
{
    pr_info("Hello, world №2\n");
    return 0;  
}

// Определение функции, вызываемой при выгрузке модуля.
static void __exit hello_2_exit(void)
{
    pr_info(KERN_INFO "Goodbye, world №2\n");
}

// Регистрация функций инициализации и выгрузки модуля.
module_init(hello_2_init);
module_exit(hello_2_exit);


// Указание лицензии модуля.
MODULE_LICENSE("GPL");

// Указание автора модуля.
MODULE_AUTHOR("Your Name");

// Указание описания модуля.
MODULE_DESCRIPTION("A simple example Linux module.");

// Указание версии модуля.
MODULE_VERSION("0.1");


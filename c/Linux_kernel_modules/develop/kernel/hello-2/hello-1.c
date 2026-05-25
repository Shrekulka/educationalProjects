// hello-1.c – простейший модуль ядра.
#include <linux/kernel.h> /* необходим для pr_info() */
#include <linux/module.h> /* необходим для всех модулей */

// Функция, вызываемая при загрузке модуля.
int init_module(void)
{
    pr_info("Hello world 1.\n");
    return 0;
}

// Функция, вызываемая при выгрузке модуля.
void cleanup_module(void)
{
    pr_info("Goodbye world 1.\n");
}


MODULE_LICENSE("GPL"); // Указываем лицензию модуля.


// hello-1.c – простейший модуль ядра.

#include <linux/kernel.h> /* необходим для pr_info() */
#include <linux/module.h> /* необходим для всех модулей */

int init_module(void)
{
    pr_info("Hello world 1.\n");
    // Если вернётся не 0, значит, init_module провалилась; модули загрузить не получится.
    return 0;
}

void cleanup_module(void)
{
    pr_info("Goodbye world 1.\n");
}

MODULE_LICENSE("GPL"); // Указываем лицензию модуля.


// hello-sysfs.h и hello-sysfs.c - пример использования sysfs

#include "hello-sysfs.h"

// Объявление переменной mymodule как объекта kobject для представления нашего модуля в системе файловых атрибутов
// (sysfs) ядра Linux.
static struct kobject *mymodule;

// Переменная, которую нужно будет изменять.
static int myvariable = 0;

// Функция для отображения значения переменной sysfs.
static ssize_t myvariable_show(struct kobject *kobj, struct kobj_attribute *attr, char *buf)
{
	// Используется функция sprintf для записи значения переменной в буфер.
	return sprintf(buf, "%d\n", myvariable);
}

// Функция для изменения значения переменной sysfs.
static ssize_t myvariable_store(struct kobject *kobj, struct kobj_attribute *attr, char *buf, size_t count)
{
	// Используется функция sscanf для считывания значения из буфера и сохранения в переменную.
	sscanf(buf, "%du", &myvariable);
	// Возвращается количество считанных байт, в данном случае, count.
	return count;
}


// В данном случае, создается атрибут myvariable_attribute, который связывает переменную myvariable с функциями для
// чтения (myvariable_show) и записи (myvariable_store).
// __ATTR - это макрос, который создает структуру kobj_attribute с нужными параметрами, такими как имя атрибута
// (myvariable), права доступа (0660), функция для чтения (myvariable_show) и функция для записи (myvariable_store).
static struct kobj_attribute myvariable_attribute = __ATTR(myvariable, 0660, myvariable_show, (void *)myvariable_store);


// Функция инициализации модуля.
static int __init mymodule_init(void)
{
	// Переменная для отслеживания и обработки ошибок
	int error = 0;

	// Вывод информации о инициализации модуля в системный лог.
	pr_info("mymodule: initialised\n");

	// Создание и добавление объекта kobject с именем "mymodule" к ядровому kobject.
	mymodule = kobject_create_and_add("mymodule", kernel_kobj);

	// В случае ошибки, возвращается код ошибки ENOMEM.
	if (!mymodule)
		return -ENOMEM;

	// Создание файла sysfs для переменной myvariable в директории /sys/kernel/mymodule.
	error = sysfs_create_file(mymodule, &myvariable_attribute.attr);

	// Вывод сообщения об ошибке в случае неудачи создания файла sysfs.
	if (error)
		pr_info("failed to create the myvariable file in /sys/kernel/mymodule\n");

	return error; // Возвращение кода ошибки или успеха.
}

// Функция выхода из модуля.
static void __exit mymodule_exit(void)
{
	// Вывод информации об успешном выходе из модуля в системный лог.
	pr_info("mymodule: Exit success\n");

	// Освобождение ресурсов, связанных с объектом kobject.
	kobject_put(mymodule);
}

// Регистрация функций инициализации и выхода из модуля.
module_init(mymodule_init);
module_exit(mymodule_exit);


MODULE_LICENSE("GPL"); // Указание лицензии модуля (GPL).

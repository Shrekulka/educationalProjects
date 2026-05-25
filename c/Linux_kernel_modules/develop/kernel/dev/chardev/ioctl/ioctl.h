// Заголовочный комментарий с указанием информации об авторе и дате создания файла.
// Created by Shrekulka on 07.12.2023.
//


#pragma once

#ifndef IOCTL_IOCTL_H
#define IOCTL_IOCTL_H

// Включение необходимых заголовочных файлов ядра Linux.
#include <linux/cdev.h>
#include <linux/fs.h>
#include <linux/init.h>
#include <linux/ioctl.h>
#include <linux/module.h>
#include <linux/slab.h>
#include <linux/uaccess.h>


// Магическое число используется для идентификации IOCTL-команд и помогает ядру отличать запросы разных устройств или драйверов.
#define IOC_MAGIC '\x66'

// Макрос для определения IOCTL-команды с передачей данных (struct ioctl_arg) от пользователя к ядру.
#define IOCTL_VALSET _IOW(IOC_MAGIC, 0, struct ioctl_arg)

// Макрос для определения IOCTL-команды с передачей данных (struct ioctl_arg) от ядра к пользователю.
#define IOCTL_VALGET _IOR(IOC_MAGIC, 1, struct ioctl_arg)

// Макрос для определения IOCTL-команды с передачей целочисленного значения от ядра к пользователю.
#define IOCTL_VALGET_NUM _IOR(IOC_MAGIC, 2, int)

// Макрос для определения IOCTL-команды с передачей целочисленного значения от пользователя к ядру.
#define IOCTL_VALSET_NUM _IOW(IOC_MAGIC, 3, int)

// Максимальный номер IOCTL-команды.
#define IOCTL_VAL_MAXNR 3

// Имя драйвера, которое будет использоваться для идентификации устройства в системе.
#define DRIVER_NAME "ioctltest"

// Определение структуры для передачи аргументов в IOCTL-вызовах.
struct ioctl_arg
{
	unsigned int val;   // Поле для передачи беззнакового целочисленного значения.
};

// Определение структуры для данных, используемых в устройстве.
struct test_ioctl_data
{
	unsigned char val;  // Поле для хранения беззнакового символа.
	rwlock_t lock;      // Структура для реализации блокировки чтения/записи.
};

// Объявление функции test_ioctl_ioctl, которая будет обрабатывать IOCTL-команды.
// Принимает указатель на файл, код команды и аргументы IOCTL.
static long test_ioctl_ioctl(struct file *filp, unsigned int cmd, unsigned long arg);

// Объявление функции test_ioctl_read, предназначенной для чтения данных из устройства в пространство пользователя.
// Принимает указатель на файл, буфер для данных пользователя, количество байт для чтения и текущую позицию в файле.
static ssize_t test_ioctl_read(struct file *filp, char __user *buf, size_t count, loff_t *f_pos);

// Объявление функции test_ioctl_close, отвечающей за закрытие файла/устройства.
// Принимает указатель на inode и указатель на файл.
static int test_ioctl_close(struct inode *inode, struct file *filp);

// Объявление функции test_ioctl_open, отвечающей за открытие файла/устройства.
// Принимает указатель на inode и указатель на файл.
static int test_ioctl_open(struct inode *inode, struct file *filp);

#endif //IOCTL_IOCTL_H

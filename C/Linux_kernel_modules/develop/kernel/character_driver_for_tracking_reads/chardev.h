// Created by Shrekulka on 29.11.2023.
//

#pragma once

#ifndef CHARACTER_DRIVER_FOR_TRACKING_READS_CHARDEV_H
#define CHARACTER_DRIVER_FOR_TRACKING_READS_CHARDEV_H

#include <linux/atomic.h>
#include <linux/cdev.h>
#include <linux/delay.h>
#include <linux/device.h>
#include <linux/fs.h>
#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/printk.h>
#include <linux/types.h>
#include <linux/uaccess.h>
#include <linux/version.h>


// Макрос для успешного завершения функций.
#define SUCCESS 0

// Имя устройства, как оно показано в /proc/devices.
#define DEVICE_NAME "chardev"

// Максимальная длина сообщения устройства.
#define BUF_LEN 80

// Перечисление для состояний открытия устройства.
enum
{
	CDEV_NOT_USED = 0,
	CDEV_EXCLUSIVE_OPEN = 1,
};

// Устройство открыто? Используется для предотвращения множественных обращений к устройству.
static atomic_t already_open = ATOMIC_INIT(CDEV_NOT_USED);

// Указатель на структуру файловых операций.
extern struct file_operations chardev_fops;

// Функция открытия файла устройства.
static int device_open(struct inode*, struct file*);

// Функция закрытия файла устройства.
static int device_release(struct inode*, struct file*);

// Функция чтения из файла устройства.
static ssize_t device_read(struct file*, char __user *, size_t, loff_t *);

// Функция записи в файл устройства.
static ssize_t device_write(struct file*, const char __user *, size_t, loff_t *);

#endif // CHARACTER_DRIVER_FOR_TRACKING_READS_CHARDEV_H
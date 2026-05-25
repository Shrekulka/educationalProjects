//
// Created by Shrekulka on 01.12.2023.
//

#pragma once

#ifndef PROC_2_PROCFS_2_H
#define PROC_2_PROCFS_2_H

#include <linux/kernel.h>  // Заголовочный файл для работы с функциями ядра.
#include <linux/module.h>  // Заголовочный файл для модулей ядра.
#include <linux/proc_fs.h>  // Заголовочный файл для работы с файловой системой /proc.
#include <linux/uaccess.h>  // Заголовочный файл для функции copy_from_user.
#include <linux/version.h>  // Заголовочный файл для получения версии ядра.

#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 6, 0)
#define HAVE_PROC_OPS  // Определение макроса, если версия ядра 5.6.0 и новее.
#endif

#define PROCFS_MAX_SIZE 1024  // Максимальный размер файла /proc.
#define PROCFS_NAME "buffer1k"  // Имя файла /proc.

// Эта функция вызывается при считывании файла /proc.
static ssize_t procfile_read(struct file *filePointer, char __user *buffer, size_t buffer_length, loff_t *offset);

// Эта функция вызывается при записи файла /proc.
static ssize_t procfile_write(struct file *file, const char __user *buff, size_t len, loff_t *off);

#endif //PROC_2_PROCFS_2_H

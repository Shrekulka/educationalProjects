// Created by Shrekulka on 30.11.2023.
//

// Защита от повторного включения заголовочного файла
#pragma once

#ifndef PROC_1_PROCFS1_H
#define PROC_1_PROCFS1_H

// Включение необходимых заголовочных файлов для ядра Linux
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/proc_fs.h>
#include <linux/uaccess.h>
#include <linux/version.h>

// Проверка версии ядра для определения необходимости использования proc_ops
#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 6, 0)
#define HAVE_PROC_OPS
#endif

// Имя файла в /proc, в данном случае "helloworld"
#define procfs_name "helloworld"

static ssize_t procfile_read(struct file *filePointer, char __user *buffer, size_t buffer_length, loff_t *offset);

#endif //PROC_1_PROCFS1_H

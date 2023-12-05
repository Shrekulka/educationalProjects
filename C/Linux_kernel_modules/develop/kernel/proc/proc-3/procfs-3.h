//
// Created by Shrekulka on 03.12.2023.
//

#pragma once

#ifndef PROCFS_3_PROCFS_3_H
#define PROCFS_3_PROCFS_3_H

#include <linux/kernel.h>       // Ядро Linux: базовые определения ядра
#include <linux/module.h>       // Ядро Linux: макросы для определения модуля
#include <linux/proc_fs.h>      // Ядро Linux: функции для работы с /proc
#include <linux/sched.h>        // Ядро Linux: определения для работы с процессами
#include <linux/uaccess.h>      // Ядро Linux: функции для работы с пользовательским пространством
#include <linux/version.h>      // Ядро Linux: определение версии ядра

#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 6, 0)
#define HAVE_PROC_OPS                     // Проверка версии ядра для использования proc_ops
#endif

#define PROCFS_MAX_SIZE 2048              // Максимальный размер буфера /proc
#define PROCFS_ENTRY_FILENAME "buffer2k"  // Имя файла /proc

// Объявление функции чтения /proc файла
static ssize_t procfs_read(struct file *filp, char __user *buffer, size_t length, loff_t *offset);

// Объявление функции записи в /proc файл
static ssize_t procfs_write(struct file *file, const char __user *buffer, size_t len, loff_t *off);

// Объявление функции открытия /proc файла
static int procfs_open(struct inode *inode, struct file *file);

// Объявление функции закрытия /proc файла
static int procfs_close(struct inode *inode, struct file *file);

#endif //PROCFS_3_PROCFS_3_H

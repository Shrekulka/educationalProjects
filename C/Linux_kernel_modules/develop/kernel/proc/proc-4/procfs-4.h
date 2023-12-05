// Created by Shrekulka on 04.12.2023.
//

#pragma once

#ifndef PROC_4_PROCFS_4_H
#define PROC_4_PROCFS_4_H

#include <linux/kernel.h>   // Для работы с ядром.
#include <linux/module.h>   // Для модулей.
#include <linux/proc_fs.h>  // Для использования procfs
#include <linux/seq_file.h> // Для seq_file
#include <linux/version.h>  // Для использования макроса LINUX_VERSION_CODE

// Проверка версии ядра для определения поддержки proc_ops
#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 6, 0)
#define HAVE_PROC_OPS
#endif

// Имя файла в /proc
#define PROC_NAME "iter"

// Прототипы функций, определения которых находятся в procfs-4.c

// Эта функция вызывается в начале последовательности.
// То есть, когда:
//   - первый раз считывается файл /proc
//   - после завершения функции (в конце последовательности)
static void *my_seq_start(struct seq_file *s, loff_t *pos);

// Эта функция вызывается после начала последовательности.
// Ее вызов повторяется до возвращения значения NULL (затем последовательность завершается).
static void *my_seq_next(struct seq_file *s, void *v, loff_t *pos);

// Эта функция вызывается в конце последовательности.
static void my_seq_stop(struct seq_file *s, void *v);

// Эта функция вызывается для каждого «шага» последовательности.
static int my_seq_show(struct seq_file *s, void *v);

// Эта функция вызывается при открытии файла /proc.
static int my_open(struct inode *inode, struct file *file);

#endif //PROC_4_PROCFS_4_H

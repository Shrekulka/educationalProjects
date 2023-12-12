//
// Created by Shrekulka on 07.12.2023.
//

#pragma once

#ifndef HELLO_SYSFS_HELLO_SYSFS_H
#define HELLO_SYSFS_HELLO_SYSFS_H

#include <linux/fs.h>
#include <linux/init.h>
#include <linux/kobject.h>
#include <linux/module.h>
#include <linux/string.h>
#include <linux/sysfs.h>

// Объявление функции для отображения значения переменной sysfs.
static ssize_t myvariable_show(struct kobject *kobj, struct kobj_attribute *attr, char *buf);

// Объявление функции для сохранения значения переменной в sysfs.
static ssize_t myvariable_store(struct kobject *kobj, struct kobj_attribute *attr, char *buf, size_t count);


#endif //HELLO_SYSFS_HELLO_SYSFS_H

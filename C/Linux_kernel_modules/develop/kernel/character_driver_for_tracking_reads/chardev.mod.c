#include <linux/module.h>
#define INCLUDE_VERMAGIC
#include <linux/build-salt.h>
#include <linux/elfnote-lto.h>
#include <linux/export-internal.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

#ifdef CONFIG_UNWINDER_ORC
#include <asm/orc_header.h>
ORC_HEADER;
#endif

BUILD_SALT;
BUILD_LTO_INFO;

MODULE_INFO(vermagic, VERMAGIC_STRING);
MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(".gnu.linkonce.this_module") = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

#ifdef CONFIG_RETPOLINE
MODULE_INFO(retpoline, "Y");
#endif



static const char ____versions[]
__used __section("__versions") =
	"\x14\x00\x00\x00\x96\x04\x50\x4d"
	"module_put\0\0"
	"\x10\x00\x00\x00\x7e\x3a\x2c\x12"
	"_printk\0"
	"\x1c\x00\x00\x00\xec\x89\x9e\x29"
	"__register_chrdev\0\0\0"
	"\x18\x00\x00\x00\x5d\x06\x73\x07"
	"class_create\0\0\0\0"
	"\x18\x00\x00\x00\x13\x87\x09\x50"
	"device_create\0\0\0"
	"\x18\x00\x00\x00\xdf\x99\xaa\x11"
	"device_destroy\0\0"
	"\x18\x00\x00\x00\xb9\x53\x3c\xcd"
	"class_destroy\0\0\0"
	"\x1c\x00\x00\x00\xc0\xfb\xc3\x6b"
	"__unregister_chrdev\0"
	"\x1c\x00\x00\x00\xef\x6d\x5c\xa6"
	"alt_cb_patch_nops\0\0\0"
	"\x10\x00\x00\x00\xfd\xf9\x3f\x3c"
	"sprintf\0"
	"\x18\x00\x00\x00\x2f\x8c\x1e\xbc"
	"try_module_get\0\0"
	"\x18\x00\x00\x00\x9b\xef\xd9\xc4"
	"system_cpucaps\0\0"
	"\x24\x00\x00\x00\x52\x3f\x0a\x4b"
	"gic_nonsecure_priorities\0\0\0\0"
	"\x18\x00\x00\x00\xe7\xb3\x5d\x08"
	"module_layout\0\0\0"
	"\x00\x00\x00\x00\x00\x00\x00\x00";

MODULE_INFO(depends, "");


MODULE_INFO(srcversion, "214036C6E3CC6648710F82F");

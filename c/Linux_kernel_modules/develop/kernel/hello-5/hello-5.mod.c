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
	"\x10\x00\x00\x00\x7e\x3a\x2c\x12"
	"_printk\0"
	"\x18\x00\x00\x00\x51\x1d\xcd\xaf"
	"param_ops_int\0\0\0"
	"\x18\x00\x00\x00\x24\x1c\xf9\xce"
	"param_array_ops\0"
	"\x18\x00\x00\x00\x75\x6f\x0a\xb3"
	"param_ops_charp\0"
	"\x18\x00\x00\x00\x4b\x74\x7a\x2b"
	"param_ops_long\0\0"
	"\x18\x00\x00\x00\xd9\xdf\x6f\x34"
	"param_ops_short\0"
	"\x18\x00\x00\x00\xe7\xb3\x5d\x08"
	"module_layout\0\0\0"
	"\x00\x00\x00\x00\x00\x00\x00\x00";

MODULE_INFO(depends, "");


MODULE_INFO(srcversion, "1364F2CAEE85112C5F2EE04");

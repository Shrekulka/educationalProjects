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
	"\x14\x00\x00\x00\x43\x0e\xc3\xfb"
	"proc_create\0"
	"\x1c\x00\x00\x00\x09\x27\x98\xad"
	"remove_proc_entry\0\0\0"
	"\x1c\x00\x00\x00\x65\x62\xf5\x2c"
	"__dynamic_pr_debug\0\0"
	"\x14\x00\x00\x00\xbe\xa6\x30\x2f"
	"seq_open\0\0\0\0"
	"\x14\x00\x00\x00\x0b\x85\x90\x80"
	"seq_printf\0\0"
	"\x14\x00\x00\x00\x0d\x27\xa6\x91"
	"seq_read\0\0\0\0"
	"\x14\x00\x00\x00\xf5\x0a\x95\x12"
	"seq_lseek\0\0\0"
	"\x14\x00\x00\x00\xcf\x1c\x64\x34"
	"seq_release\0"
	"\x18\x00\x00\x00\xe7\xb3\x5d\x08"
	"module_layout\0\0\0"
	"\x00\x00\x00\x00\x00\x00\x00\x00";

MODULE_INFO(depends, "");


MODULE_INFO(srcversion, "EBDB5A613BF353AE315D828");

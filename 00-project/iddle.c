#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Hugo Rodrigues");
MODULE_DESCRIPTION("A simple Linux kernel module that prints a message when loaded and unloaded.");
MODULE_VERSION("1.0");

static int __init iddle_init(void)
{
    printk(KERN_INFO "Iddle module loaded: Hello, Kernel!\n");
    return 0;
}

static void __exit iddle_exit(void)
{
    printk(KERN_INFO "Iddle module unloaded: Goodbye, Kernel!\n");
}

module_init(iddle_init);
module_exit(iddle_exit);
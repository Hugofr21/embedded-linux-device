# Makefile
obj-m := iddle.o  # module name and source file             

all:
	$(MAKE) -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules  # build the module using the kernel's build system
clean:
	$(MAKE) -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean # clean the build files


test: # test the module
	cat /proc/iddle > iddle_test.txt
	sudo insmod iddle.ko
	dmesg | tail -n 10
	sudo rmmod iddle
	dmesg | tail -n 10

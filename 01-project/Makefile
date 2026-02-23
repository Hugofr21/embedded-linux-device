# -------------------------------------------------
# Makefile do mini‑projeto
# -------------------------------------------------
obj-m := myproc.o                     # nome do módulo (gera myproc.ko)

# ----- Construção padrão -------------------------------------------------
all:
	$(MAKE) -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

# ----- Limpeza -----------------------------------------------------------
clean:
	$(MAKE) -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
	@rm -f *.mod.c *.order *.symvers

# ----- Teste automatizado ------------------------------------------------
#  1) compila (alvo implícito “all” já está presente)
#  2) carrega o módulo (insmod)
#  3) lê o proc‑file e grava em test.txt
#  4) descarrega o módulo (rmmod)
#  5) exibe o conteúdo de test.txt
#
#  O alvo precisa ser executado como root (sudo), por isso usamos sudo
#  dentro das receitas.
test:
	sudo $(MAKE) all
	sudo insmod myproc.ko
	sudo cat /proc/myproc > test.txt
	sudo rmmod myproc
	@echo "=== Conteúdo lido de /proc/myproc ==="
	@cat test.txt

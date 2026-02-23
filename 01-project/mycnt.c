/* SPDX-License-Identifier: GPL-2.0-or-later */
/*
 * myproc.c – exemplo de criação de um arquivo em /proc usando seq_file.
 * Cada leitura devolve a mensagem fixa e demonstra a estrutura mínima
 * de um módulo de caractere /proc.
 */

#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/proc_fs.h>
#include <linux/seq_file.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Hugo Rodrigues");
MODULE_DESCRIPTION("Example of a module that creates a file in /proc using seq_file.");
MODULE_VERSION("1.0");

/* ------------------------------------------------------------------
 *  Função que gera o conteúdo que será entregue ao usuário.
 *  Usa a API seq_file (“seq_printf”) que cuida de buffers internos.
 * ------------------------------------------------------------------ */
static int myproc_show(struct seq_file *m, void *v)
{
    seq_printf(m, "Hello from the proc file system!\n");
    return 0;
}

/* ------------------------------------------------------------------
 *  “open” do arquivo – associa a função `myproc_show` ao seq_file.
 * ------------------------------------------------------------------ */
static int myproc_open(struct inode *inode, struct file *file)
{
    return single_open(file, myproc_show, NULL);
}

/* ------------------------------------------------------------------
 *  Operações suportadas por /proc/myproc.
 *  O kernel chamará estas funções quando o usuário abrir/ler/etc.
 * ------------------------------------------------------------------ */
static const struct proc_ops myproc_fops = {
    .proc_open = myproc_open,
    .proc_read = seq_read,
    .proc_lseek = seq_lseek,
    .proc_release = single_release,
};

/* ------------------------------------------------------------------
 *  Inicialização do módulo – cria o arquivo em /proc.
 *  O terceiro parâmetro “NULL” indica que queremos que o arquivo fique
 *  na raiz de /proc (não dentro de sub‑diretório).
 *  Permissões 0444 → leitura para todos.
 * ------------------------------------------------------------------ */
static int __init myproc_init(void)
{
    if (!proc_create("myproc", 0444, NULL, &myproc_fops))
    {
        pr_err("myproc: falha ao criar /proc/myproc\n");
        return -ENOMEM;
    }

    pr_info("myproc: módulo carregado – /proc/myproc criado\n");
    return 0;
}

/* ------------------------------------------------------------------
 *  Finalização do módulo – remove o arquivo de /proc.
 * ------------------------------------------------------------------ */
static void __exit myproc_exit(void)
{
    remove_proc_entry("myproc", NULL);
    pr_info("myproc: módulo descarregado – /proc/myproc removido\n");
}

module_init(myproc_init);
module_exit(myproc_exit);

#include <net/sock.h>
#include <bcc/proto.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Hugo Rodrigues");
MODULE_DESCRIPTION("eBPF program to trace TCP sendmsg calls.");
MODULE_VERSION("1.0");

int trace_tcp_sendmsg(struct pt_regs *ctx, struct sock *sk)
{
    u16 sport = 0, dport = 0;
    u32 saddr = 0, daddr = 0;

    bpf_probe_read_kernel(&sport, sizeof(sport), &sk->__sk_common.skc_num);
    bpf_probe_read_kernel(&dport, sizeof(dport), &sk->__sk_common.skc_dport);
    bpf_probe_read_kernel(&saddr, sizeof(saddr), &sk->__sk_common.skc_rcv_saddr);
    bpf_probe_read_kernel(&daddr, sizeof(daddr), &sk->__sk_common.skc_daddr);

    dport = ntohs(dport);

    bpf_trace_printk("TCP Tx | Src: %u SrcPort: %d\\n", saddr, sport);
    bpf_trace_printk("TCP Tx | Dst: %u DstPort: %d\\n", daddr, dport);

    return 0;
}

module_init(trace_tcp_sendmsg);
module_exit(trace_tcp_sendmsg);
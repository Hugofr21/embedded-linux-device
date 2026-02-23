from bcc import BPF
import socket
import struct

def int_to_ip(ip_int):
    return socket.inet_ntoa(struct.pack("<I", ip_int))

b = BPF(src_file="network.c")
b.attach_kprobe(event="tcp_sendmsg", fn_name="trace_tcp_sendmsg")

print("Rastreamento da função tcp_sendmsg inicializado. Pressione Ctrl+C para finalizar.")

try:
    while True:
        (task, pid, cpu, flags, ts, msg) = b.trace_fields()
        msg_str = msg.decode('utf-8')
        if "Src:" in msg_str or "Dst:" in msg_str:
            parts = msg_str.split()
            try:
                ip_int = int(parts[3])
                port = int(parts[5])
                direction = "Origem" if "Src:" in msg_str else "Destino"
                print(f"[{direction}] IP: {int_to_ip(ip_int)} | Porta: {port}")
            except (IndexError, ValueError):
                pass
except KeyboardInterrupt:
    print("\nDesanexando sondas e finalizando execução...")
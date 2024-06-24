import socket
import threading
import time

def handle_packet(server_socket, expected_payload, addr_count_map, valid_packet_count, lock):
    while True:
        data, addr = server_socket.recvfrom(1024)
        addr_str = f"{addr[0]}:{addr[1]}"

        with lock:
            if data == expected_payload:
                valid_packet_count[0] += 1

                if addr_str in addr_count_map:
                    addr_count_map[addr_str] += 1
                else:
                    addr_count_map[addr_str] = 1
            else:
                print(f"接收到来自 {addr} 的无效负载，内容为 {data.decode('utf-8')}")

def print_counts(addr_count_map, valid_packet_count, lock):
    while True:
        time.sleep(5)
        with lock:
            count_1 = sum(1 for count in addr_count_map.values() if count == 1)
            count_2 = sum(1 for count in addr_count_map.values() if count == 2)
            count_3 = sum(1 for count in addr_count_map.values() if count == 3)
            print(f"有效负载计数: {valid_packet_count[0]}")
            print(f"值为1的数量: {count_1}, 值为2的数量: {count_2}, 值为3的数量: {count_3}")

def start_udp_server(host, port, expected_payload):
    # 创建一个UDP套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 20 * 1024 * 1024)  # 20 MB
    server_socket.bind((host, port))
    print(f"UDP服务器正在监听 {host}:{port}")

    valid_packet_count = [0]  # 初始化计数器
    addr_count_map = {}  # 初始化地址计数字典
    lock = threading.Lock()

    threading.Thread(target=print_counts, args=(addr_count_map, valid_packet_count, lock), daemon=True).start()

    for _ in range(2):
        threading.Thread(target=handle_packet, args=(server_socket, expected_payload, addr_count_map, valid_packet_count, lock), daemon=True).start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 10086      
    EXPECTED_PAYLOAD = b'X' * 36  # 期望的负载内容为36个字符 'X'

    start_udp_server(HOST, PORT, EXPECTED_PAYLOAD)

import socket
import time
import sys

def udp_flood(src_port, dst_ip, dst_port, rounds, sleep_time):
    for i in range(rounds):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(('', src_port))  # 绑定源端口
            sock.sendto(b"X" * 36, (dst_ip, dst_port))
            print(f"Round {i+1}: Sent packet from source port {src_port} to {dst_ip}:{dst_port}")
            sock.close()
            if i < rounds - 1:  # 如果不是最后一轮，就休眠
                time.sleep(sleep_time)
        except Exception as e:
            print(f"Round {i+1}: Error sending packet - {e}")

if __name__ == "__main__":
    src_port = 12345  # 源端口
    dst_ip = "47.96.121.125"
    dst_port = 11111
    rounds = 2  # 发送轮数
    sleep_time = int(sys.argv[1]) if len(sys.argv) > 1 else 1  # 如果有提供命令行参数，则使用该参数作为休眠时间

    udp_flood(src_port, dst_ip, dst_port, rounds, sleep_time)

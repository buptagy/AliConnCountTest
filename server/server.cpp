#include <iostream>
#include <thread>
#include <mutex>
#include <map>
#include <chrono>
#include <cstring>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define BUFFER_SIZE 1024

std::mutex mtx;
std::map<std::string, int> addr_count_map;
int valid_packet_count = 0;
const std::string EXPECTED_PAYLOAD(36, 'X');

void handle_packet(int server_socket) {
    char buffer[BUFFER_SIZE];
    struct sockaddr_in client_addr;
    socklen_t addr_len = sizeof(client_addr);

    while (true) {
        memset(buffer, 0, BUFFER_SIZE);
        int recv_len = recvfrom(server_socket, buffer, BUFFER_SIZE, 0, (struct sockaddr*)&client_addr, &addr_len);
        std::string data(buffer, recv_len);
        std::string addr_str(inet_ntoa(client_addr.sin_addr));
        addr_str += ":" + std::to_string(ntohs(client_addr.sin_port));

        std::lock_guard<std::mutex> lock(mtx);
        if (data == EXPECTED_PAYLOAD) {
            valid_packet_count++;
            addr_count_map[addr_str]++;
            std::cout << "Valid payload count: " << valid_packet_count << std::endl;
            std::cout << "Count for addr " << addr_str << ": " << addr_count_map[addr_str] << std::endl;
        } else {
            std::cout << "Received invalid payload from " << addr_str << ", content: " << data << std::endl;
        }
    }
}

void print_counts() {
    while (true) {
        std::this_thread::sleep_for(std::chrono::seconds(5));
        std::lock_guard<std::mutex> lock(mtx);
        int count_1 = 0, count_2 = 0, count_3 = 0;
        for (auto& pair : addr_count_map) {
            if (pair.second == 1) count_1++;
            else if (pair.second == 2) count_2++;
            else if (pair.second == 3) count_3++;
        }
        std::cout << "Count of 1: " << count_1 << ", Count of 2: " << count_2 << ", Count of 3: " << count_3 << std::endl;
    }
}

int main() {
    int server_socket;
    struct sockaddr_in server_addr;

    server_socket = socket(AF_INET, SOCK_DGRAM, 0);
    const int RCVBUF_SIZE = 20 * 1024 * 1024; // 20MB
	int rcvbuf = RCVBUF_SIZE;
	if (setsockopt(server_socket, SOL_SOCKET, SO_RCVBUF, &rcvbuf, sizeof(rcvbuf)) < 0) {
    	std::cerr << "Set socket option failed." << std::endl;
    	return -1;
	}
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(10086);
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);

    if (bind(server_socket, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        std::cerr << "Bind socket failed." << std::endl;
        return -1;
    }

    std::cout << "UDP server is listening on 0.0.0.0:10086" << std::endl;

    std::thread print_thread(print_counts);
    std::thread handle_thread1(handle_packet, server_socket);
    std::thread handle_thread2(handle_packet, server_socket);

    print_thread.join();
    handle_thread1.join();
    handle_thread2.join();

    return 0;
}

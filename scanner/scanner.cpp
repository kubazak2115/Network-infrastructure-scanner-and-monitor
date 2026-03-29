#include <iostream>
#include <string>
#include <vector>
#include <thread>
#include <mutex>
#include <cstdlib>
#include <cstring>
#include <sstream>

#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "ws2_32.lib")

std::mutex output_mutex;

struct HostResult {
    std::string ip;
    bool alive;
    std::vector<int> open_ports;
};

bool check_port(const std::string& ip, int port) {
    SOCKET sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == INVALID_SOCKET) return false;

    DWORD timeout = 1000; // 1 second
    setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, (char*)&timeout, sizeof(timeout));
    setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO, (char*)&timeout, sizeof(timeout));

    sockaddr_in addr{};
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    inet_pton(AF_INET, ip.c_str(), &addr.sin_addr);

    bool open = connect(sock, (struct sockaddr*)&addr, sizeof(addr)) == 0;
    closesocket(sock);
    return open;
}

bool ping_host(const std::string& ip) {
    // std::string cmd = "ping -n 1 -w 1000 " + ip + " > nul 2>&1";
    // return system(cmd.c_str()) == 0;
    return check_port(ip, 22);
}

void scan_host(const std::string& ip, const std::vector<int>& ports, std::vector<HostResult>& results) {
    HostResult result;
    result.ip = ip;
    result.alive = ping_host(ip);
    
    if (result.alive) {
        for (int port : ports) {
            if(check_port(ip, port)) {
                result.open_ports.push_back(port);
            }
        }
    }

    std::lock_guard<std::mutex> lock(output_mutex);
    results.push_back(result);

    std::cout << ip << " | " << (result.alive ? "UP" : "DOWN");
    if (!result.open_ports.empty()){
        std::cout << " | ports: ";
        for (int p : result.open_ports) {
            std::cout << p << " ";
        }
    }
    std::cout << std::endl;
}

std::vector<std::string> generate_subnet(const std::string& base, int start, int end) {
    std::vector<std::string> ips;
    for (int i = start; i <= end; i++) {
        ips.push_back(base + std::to_string(i));
    }
    return ips;
}

void print_json(const std::vector<HostResult>& results) {
    std::cout << "\n[";
    for (size_t i = 0; i < results.size(); i++) {
        const auto& r = results[i];
        std::cout << "{ \"ip\": \"" << r.ip << "\", \"alive\": " << (r.alive ? "true" : "false") << ", \"open_ports\": [";
        for (size_t j = 0; j < r.open_ports.size(); j++) {
            std::cout << r.open_ports[j];
            if (j < r.open_ports.size() - 1) std::cout << ", ";
        }
        std::cout << "] }";
        if (i < results.size() - 1) std::cout << ", ";
    }
    std::cout << "]\n";
}

int main(int argc, char* argv[]){
    WSADATA wsa;
    WSAStartup(MAKEWORD(2, 2), &wsa);

    std::string subnet = "10.0.1.";
    int start = 1, end = 254;

    if (argc >= 2) subnet = argv[1];
    if (argc >= 4) {
        start = std::stoi(argv[2]);
        end = std::stoi(argv[3]);
    }

    std::vector<int> ports = {22, 80, 443, 8080, 5000};
    std::vector<std::string> ips = generate_subnet(subnet, start, end);
    std::vector<HostResult> results;

    std::cout << "Scanning subnet: " << subnet << " from " << start << " to " << end << std::endl;

    std::vector<std::thread> threads;
    for (const auto& ip : ips) {
        threads.emplace_back(scan_host, ip, ports, std::ref(results));
    }
    for (auto& t : threads) {
        t.join();
    }

    print_json(results);
    
    WSACleanup();
    return 0;
}
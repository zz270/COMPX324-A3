import socket
import sys

def send_requests(server_host, server_port, request_file_path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_host, server_port))
        with open(request_file_path, 'r') as request_file:
            for line in request_file:
                request = format_request(line.strip())
                if request:
                    client_socket.sendall(request.encode('utf-8'))
                    response = client_socket.recv(1024).decode('utf-8')
                    print(f"{line.strip()}: {response}")
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
            
def format_request(request_line):
    parts = request_line.split(' ')
    if len(parts) < 2:
        print(f"Invalid request format: {request_line}")
        return None
    command = parts[0]
    key = parts[1]
    value = ' '.join(parts[2:]) if len(parts) > 2 else ''

    message_size = 7 + len(key) + len(value)
    if message_size > 999:
        print(f"Request size exceeds limit: {request_line}")
        return None

    return f"{message_size:03d} {command[0]} {key} {value}"

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <server_host> <server_port> <request_file_path>")
        sys.exit(1)
    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    request_file_path = sys.argv[3]
    send_requests(server_host, server_port, request_file_path)
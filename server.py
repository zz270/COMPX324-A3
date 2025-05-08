import threading
import socket
import time

tuple_space = {}
operation_counts = {"R": 0, "G": 0, "P": 0, "ERR": 0}
error_counts = {"R": 0, "G": 0, "P": 0}
client_count = 0

def handle_client(client_socket):
    global tuple_space, operation_counts, error_counts, client_count
    with client_socket:
        while True:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                break
            response = process_request(request)
            client_socket.sendall(response.encode('utf-8'))

def process_request(request):
    global operation_counts, error_counts
    command = request[3]
    key = request[5:request.find(' ') if ' ' in request else len(request)]
    value = request[request.find(' ') + 1:] if ' ' in request else ''

     if command == 'R':
        return read(key)
    elif command == 'G':
        return get(key)
    elif command == 'P':
        return put(key, value)
    else:
        operation_counts["ERR"] += 1
        return "024 ERR invalid command"

def read(key):
    global operation_counts, error_counts
    value = tuple_space.get(key)
    if value:
        response_size = 11 + len(key) + len(value)
        return f"0{response_size:02d} OK ({key}, {value}) read"
    else:
        operation_counts["ERR"] += 1
        error_counts["R"] += 1
        return "024 ERR k does not exist" 

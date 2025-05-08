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

def get(key):
    global operation_counts, error_counts
    value = tuple_space.pop(key, None)
    if value:
        response_size = 12 + len(key) + len(value)
        return f"0{response_size:02d} OK ({key}, {value}) removed"
    else:
        operation_counts["ERR"] += 1
        error_counts["G"] += 1
        return "024 ERR k does not exist"


def put(key, value):
    global operation_counts, error_counts
    if key in tuple_space:
        operation_counts["ERR"] += 1
        error_counts["P"] += 1
        return "024 ERR k already exists"
    else:
        tuple_space[key] = value
        response_size = 11 + len(key) + len(value)
        return f"0{response_size:02d} OK ({key}, {value}) added"
    
def print_summary():
    global tuple_space, operation_counts, error_counts, client_count
    while True:
        time.sleep(10)
        tuple_count = len(tuple_space)
        total_tuple_size = sum(len(key) + len(value) for key, value in tuple_space.items())
        average_tuple_size = total_tuple_size / tuple_count if tuple_count > 0 else 0
        average_key_size = sum(len(key) for key in tuple_space.keys()) / tuple_count if tuple_count > 0 else 0
        average_value_size = sum(len(value) for value in tuple_space.values()) / tuple_count if tuple_count > 0 else 0

        print(f"Tuple space summary:")
        print(f"Number of tuples: {tuple_count}")
        print(f"Average tuple size: {average_tuple_size}")
        print(f"Average key size: {average_key_size}")
        print(f"Average value size: {average_value_size}")
        print(f"Total number of clients: {client_count}")
        print(f"Total number of operations: {sum(operation_counts.values())}")
        print(f"Total READs: {operation_counts['R']}")
        print(f"Total GETs: {operation_counts['G']}")
        print(f"Total PUTs: {operation_counts['P']}")
        print(f"Total errors: {operation_counts['ERR']}")

    
def start_server(port):
    global client_count
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen()
        print(f"Server started on port {port}")

        summary_thread = threading.Thread(target=print_summary)
        summary_thread.daemon = True
        summary_thread.start()

        while True:
            client_socket, _ = server_socket.accept()
            client_count += 1
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()

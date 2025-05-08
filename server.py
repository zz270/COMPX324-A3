import threading
import socket
import time

tuple_space = {}
operation_counts = {"R": 0, "G": 0, "P": 0, "ERR": 0}
error_counts = {"R": 0, "G": 0, "P": 0}
client_count = 0
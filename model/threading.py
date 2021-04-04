import threading
from queue import Queue
from model.tcp.tcp import connect_scan

queue = Queue
open_ports = []

# https://www.youtube.com/watch?v=FGdiSJakIS4

# def threading(threads):
#     # for i in range(500):
#     # thread = threading.Thread(target=chose_function)
#     # thread.start()
#     pass
#
# def fill_queue(port_list):
#     for port in port_list:
#         queue.put(port)
#
#
# def worker():
#     while not queue.empty():
#         port = queue.get()
#         if connect_scan(port):
#             print(f"port {port} - open")
#             open_ports.append(port)
#
# thread_list = []
#
# for t in range(10):
#     thread = threading.Thread(target=worker)
#     thread_list.append(thread)
#
# for thread in thread_list:
#     thread.start()
#
# for thread in thread_list:
#     thread.join()
# # import threading
# from threading import Thread, Lock
# from queue import Queue
# import time
# import socket
#
# N_THREADS = 200
# print_lock = Lock()
# queue = Queue
# open_ports = []
#
#
# def scan_thread():
#     global q
#     while True:
#         # get the port number from the queue
#         worker = q.get()
#         # scan that port number
#         port_scan(worker)
#         # tells the queue that the scanning for that port
#         # is done
#         q.task_done()
#
#
# def main(host, ports):
#     global q
#     for t in range(N_THREADS):
#         # for each thread, start it
#         t = Thread(target=scan_thread)
#         # when we set daemon to true, that thread will end when the main thread ends
#         t.daemon = True
#         # start the daemon thread
#         t.start()
#     for worker in ports:
#         # for each port, put that port into the queue
#         # to start scanning
#         q.put(worker)
#     # wait the threads ( port scanners ) to finish
#     q.join()
#
#
#
# # https://www.youtube.com/watch?v=FGdiSJakIS4
# #
# # def threading(threads):
# #     while True:
# #         worker = Queue.get()
# #
# #     # for i in range(500):
# #     # thread = threading.Thread(target=chose_function)
# #     # thread.start()
# #     pass
# #
# #
# # def fill_queue(port_list):
# #     for port in port_list:
# #         queue.put(port)
# #
# #
# # def worker():
# #     while not queue.empty():
# #         port = queue.get()
# #         if connect_scan(port):
# #             print(f"port {port} - open")
# #             open_ports.append(port)
# #
# #
# # thread_list = []
# #
# # for t in range(10):
# #     thread = threading.Thread(target=worker)
# #     thread_list.append(thread)
# #
# # for thread in thread_list:
# #     thread.start()
# #
# # for thread in thread_list:
# #     thread.join()

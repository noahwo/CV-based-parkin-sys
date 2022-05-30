"""
Server side 
"""
from socket import *
import time
import threading

def start_monitor():
    thread_monitor = threading.Thread(target=monitor)
    thread_monitor.start()
    
def monitor():
    while True:
        tcp_server = socket(AF_INET, SOCK_STREAM)

        # default as localhost
        ip = ""
        port = 1989
        tcp_server.bind((ip, port))

        # .listen
        tcp_server.listen(128)  # maximum connections
        # accept new connections(sockets) and store
        client_socket, client_addr = tcp_server.accept()
        print("\nClient "+str(client_addr).split("'")[1]+":"+str(port)+" connected")
        try:
            while True:
                from_client_msg = client_socket.recv(4096).decode("utf-8")
                if from_client_msg == "exit":
                    break
                if not (len(from_client_msg) == 0 or from_client_msg.isspace()):
                    print("PLot:", from_client_msg)
                time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                time_note = "\n\t------" + time_now + "\n"
                send_data = client_socket.send(
                    ("车辆 " +plate_+" 已进入"+ time_note).encode("utf-8")
                )
        except KeyboardInterrupt:
            print("Socket closed by keyboard interrupt!")
        except BrokenPipeError:
            print("Socket closed by client!")
        except Exception as e:
            print("Socket closed by error: " + e)
        finally:
            client_socket.close()

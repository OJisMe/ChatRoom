# socket allows connections between machines
# select offers i/o capabilities to manipulate sockets
import socket, select

header_length = 10
ip = ""
port = 1111

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# allows reconnection to a port
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((ip, port))
server_socket.listen()

# track all client and server sockets
sockets_list = []

# maps a human friendly name to each client socket using user data
clients = {}

def receive_message(client_socket: socket):
    try:
        # message_header states how long the message is
        message_header = client_socket.recv(header_length)
        if len(message_header) == 0:



    except:
        pass



if __name__=='__main__':
    print(int("09804"))
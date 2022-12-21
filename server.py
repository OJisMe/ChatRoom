# socket allows connections between machines
# select offers i/o capabilities to manipulate sockets
import select
import socket

HEADER_LENGTH = 10
ip = ""
port = 1111

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# allows reconnection to a port
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((ip, port))
server_socket.listen()

# track all client and server sockets
socket_list = []

# key- client socket value- user data
clients = {}


def receive_message(client_socket: socket):
    try:
        # message_header states how long the message is
        message_header = client_socket.recv(HEADER_LENGTH)

        # no header -> false
        if len(message_header) == 0:
            return False

        # read the given length
        message_length = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}

    except:
        return False


while True:

    # select sockets to read in
    read_sockets, _, exception_sockets = select.select(socket_list, [], socket_list)

    for notified_socket in read_sockets:
        # handle new connections
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            # user stores the first received data which will be the sockets username
            user = receive_message(client_socket)
            # if client socket has a message add the socket to the socket list, if not continuew
            if user is False:
                continue
            socket_list.append(client_socket)

            clients[client_socket] = user
            print(f"Accepted new connection from {client_address[0]}:{client_address[1]}"
                  f" username:{user['data'].decode('utf-9')}")
        else:
            message = receive_message(notified_socket)
            if message is False:
                print(f"closed connection from {clients[notified_socket]['data'].decode('utf=8')}")
                socket_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_sockets:
        socket_list.remove(notified_socket)
        del clients[notified_socket]

import sys
import socket
import threading


class Server:
    __sock = 0
    __clients = []

    def __init__(self, host, port, backlog, buffer):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.buffer = buffer

    def create(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.bind((self.host, self.port))
        return self

    def client_thread(self, conn, addr):
        print('Connected client:', addr)
        with conn:
            while True:
                message = conn.recv(self.buffer)
                if message.decode() == '':
                    break
                sys.stdout.write(message.decode())
                for client, address in self.__clients:
                    if address != addr:
                        result = f'{addr} >> {message.decode().strip()}\n'.encode()
                        client.send(result)
            self.__clients.remove((conn, addr))

    def run(self):
        self.__sock.listen(self.backlog)
        while True:
            client, address = self.__sock.accept()
            client.send(b'Welcome to the chat!\n')
            self.__clients.append((client, address))
            thread = threading.Thread(target=self.client_thread, args=(client, address))
            thread.start()


if __name__ == '__main__':
    server = Server('192.168.0.8', 8888, 5, 4096)
    server.create()
    server.run()

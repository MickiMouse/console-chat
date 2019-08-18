import sys
import socket
import threading


class Client:
    __sock = 0

    def __init__(self, ip, port, bufsize):
        self.__ip = ip
        self.__port = port
        self.bufsize = bufsize

    def connect(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.connect((self.__ip, self.__port))
        return self.__sock

    def receive_messages(self):
        with self.__sock as sock:
            while True:
                message = sock.recv(self.bufsize)
                sys.stdout.write(message.decode())

    def run(self):
        with self.connect() as sock:
            while True:
                try:
                    thread = threading.Thread(target=self.receive_messages)
                    thread.start()
                    message = sys.stdin.readline()
                    sock.send(message.encode())
                except KeyboardInterrupt:
                    break

    def disconnect(self):
        self.__sock.close()


if __name__ == '__main__':
    client = Client('192.168.0.8', 8888, 4096)
    client.run()

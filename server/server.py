import socket
import subprocess
import setup


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # to reuse the same port
    server.bind(('192.168.1.207', 5000))
    server.listen(3)
    print('Server is working...')
    while True:
        client_socket, address = server.accept()
        print(address)
        data = client_socket.recv(1024).decode('utf-8')
        HDRS = get_response(data)
        client_socket.send(HDRS)
        if len(setup.data_list) != 0:
            for i in range(len(setup.data_list)):
                client_socket.send(setup.data_list[i])
    client_socket.shutdown(socket.SHUT_WR)
    server.close()
    print('Server is closing...')


def get_response(request_data):
    HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    HDRS_404 = 'HTTP/1.1 404 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'

    path = request_data.split(' ')[1]
    if path == ' ':
        setup.data_list = []
        return (HDRS_404 + 'Page not found.').encode('utf-8')
    try:
        with open('data' + path + '.txt', 'rb') as file:
            setup.data_list = file.read().splitlines()
        return HDRS.encode('utf-8')
    except FileNotFoundError:
        setup.data_list = []
        return (HDRS_404 + 'Page not found.').encode('utf-8')


if __name__ == '__main__':
    setup.init()
    start_server()

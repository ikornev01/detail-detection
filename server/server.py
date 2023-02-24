import socket
import sys
import os

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.1.181', 5000))
    server.listen(3)
    print('Server is working...')
    while True:
        client_socket, address = server.accept()
        data = client_socket.recv(1024).decode('utf-8')
        print()
        print(data)
        answer = get_response(data)
        client_socket.send(answer)
        client_socket.shutdown(socket.SHUT_WR)

    server.close()
    print('Server is closing...')
    
def get_response(request_data):
    HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    HDRS_404 = 'HTTP/1.1 404 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    response = ''
    path = request_data.split(' ')[1]
    if path == '/':
        return (HDRS_404 + 'Page not found.').encode('utf-8')
    try:
        with open('data' + path, 'rb') as file:
            response = file.read()
        return HDRS.encode('utf-8') + response
    except FileNotFoundError:
        return (HDRS_404 + 'Page not found.').encode('utf-8')



if __name__ == '__main__':
    start_server()
    

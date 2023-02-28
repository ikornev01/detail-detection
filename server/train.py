import socket
import subprocess
import setup


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # to reuse the same port
    server.bind(('192.168.1.207', 5000))
    server.listen(3)
    print('Server started...')
    try:
        while True:
            client_socket, address = server.accept()
            # print(address)
            data = client_socket.recv(1024).decode('utf-8')
            HDRS = get_response(data)
            client_socket.send(HDRS)
            if len(setup.data_list) != 0:
                for i in range(len(setup.data_list)):
                    client_socket.send(setup.data_list[i])
    except KeyboardInterrupt:
        client_socket.shutdown(socket.SHUT_WR)
    server.close()
    print('\nServer closed...')


def run_detection():  # subprocess call
    cmd = "cd ../raspberry_pi/ && python3 detect.py --model detail.tflite"
    p1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    out, err = p1.communicate()
    print('\noutput: {0}'.format(out))
    print('error: {0}'.format(err))
    if p1.returncode == 0:
        print('command success')
        return 0
    else:
        print('command failed')
        return 1

def get_response(request_data):
    HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    HDRS_404 = 'HTTP/1.1 404 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'

    path = request_data.split(' ')[1]
    if path == '/':
        return (HDRS_404 + 'Page not found.').encode('utf-8')
    if path == '/detail':
        res = run_detection()
        print(res)
    try:
        with open('data' + path + '.txt', 'rb') as file:
            setup.data_list = file.read().splitlines()
        return HDRS.encode('utf-8')
    except FileNotFoundError:
        return (HDRS_404 + 'Page not found.').encode('utf-8')


if __name__ == '__main__':
    setup.init()
    start_server()


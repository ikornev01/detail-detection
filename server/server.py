import socket
import subprocess
import setup  # global variables to save data after object detection


def start_server():  # to start server, bind connection and show the answer on webpage
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # to reuse the same port
    server.bind(('192.168.1.226', 5000))  # raspberry pi adress. Use Ethernet connection
    server.listen(3)  # max number of devices sending requests to server
    print('Server started...')
    try:
        while True:
            print('\nServer is working...')
            client_socket, address = server.accept()
            print(address)
            data = client_socket.recv(1024).decode('utf-8')
            setup.init()
            HDRS = get_response(data)
            client_socket.send(HDRS)
            if len(setup.data_list) != 0:
                for i in range(len(setup.data_list)):  # to send data line by line 
                    client_socket.send(setup.data_list[i] + '\n'.encode('utf-8'))
            client_socket.shutdown(socket.SHUT_WR)
    except KeyboardInterrupt:
        server.close()
    print('\nServer is closed...')


def run_detection():  # subprocess call. Server gets a request than handles it calling subprocess to detect the detail
    cmd = ". ~/tflite/bin/activate && cd detail-detection/raspberry_pi/ && python detect.py --model details.tflite"
    p1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    out, err = p1.communicate()
    # print('output: {0}'.format(out))
    print('error: {0}'.format(err))
    if p1.returncode == 0:
        print('command success')
        return 0
    else:
        print('command failed')
        return 1


def get_response(request_data):  # to form the answer 
    HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    HDRS_404 = 'HTTP/1.1 404 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'

    path = request_data.split(' ')[1]  # parses user's request
    if path == '/':
        return (HDRS_404 + 'Page not found.').encode('utf-8')
    if path == '/detail':
        run_detection()  # to start detection
    try:
        with open('detail-detection/server/data' + path + '.txt', 'rb') as file:  # to read data of detected object
            setup.data_list = file.read().splitlines()
        return HDRS.encode('utf-8')
    except FileNotFoundError:
        return (HDRS_404 + 'Data not found.').encode('utf-8')


if __name__ == '__main__':
    start_server()


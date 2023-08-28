import logging
import selectors
import socket
import sys
from random import randrange
import platform
import json
import psutil
import glob
import os
from datetime import datetime as dt


HOST, PORT = '', 8000
LIST_RESPONSE = ['Hello', 'hi', 'Привет!']

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))


def handle_request() -> bytes:
    """Получить случайное значение из списка фраз"""
    request_data = LIST_RESPONSE[randrange(len(LIST_RESPONSE))]
    response = request_data + '\n'
    return response.encode('utf-8')


def get_time() -> bytes:
    """Получить текущую дату в формате UTC"""
    request_data = dt.utcnow()
    response = str(request_data) + '\n'
    return response.encode('utf-8')


def get_info_os() -> bytes:
    """Получить информацию о системе и интерпритаторе"""
    try:
        info_system = {}
        info_system['platform'] = platform.system()
        info_system['platform-release'] = platform.release()
        info_system['platform-version'] = platform.version()
        info_system['architecture'] = platform.machine()
        info_system['hostname'] = socket.gethostname()
        info_system['ip-address'] = socket.gethostbyname(socket.gethostname())
        info_system['processor'] = platform.processor()
        info_system['ram'] = str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        info_system['interpreter'] = platform.python_version()
        response = f'{info_system}' + '\n'
        return response.encode('utf-8')
    except Exception as e:
        logger.info(e)


def search_file(request_data) -> bytes:
    """Поиск файла по шаблону и возврат информации о файле"""
    request_list = request_data.split()
    name = request_list[1]
    path = request_list[2]
    list_file = glob.glob(f'{path}/{name}*.*')
    if len(list_file) > 1:
        try:
            response = str(len(list_file)) + '\n'
            return response.encode('utf-8')
        except Exception as e:
            logger.info(e)
    elif len(list_file) == 1:
        try:
            path_file = list_file[0]
            info_file = {}
            info_file['file_name'] = os.path.basename(path_file)
            info_file['file_date'] = dt.fromtimestamp(os.path.getctime(path_file)).strftime('%Y-%m-%d')
            info_file['file_size'] = os.path.getsize(path_file)
            response = f'{info_file}' + '\n'
            return response.encode('utf-8')
        except Exception as e:
            logger.info(e)
    else:
        return 'File not found \n'.encode('utf-8')


def new_connection(selector: selectors.BaseSelector, sock: socket.socket):
    """Регистрация нового подключения"""
    new_conn, address = sock.accept()
    logger.info('accepted new_conn from %s', address)
    new_conn.setblocking(False)
    selector.register(new_conn, selectors.EVENT_READ, read_callback)


def read_callback(selector: selectors.BaseSelector, sock:socket.socket):
    "Обработка подключения"
    data = sock.recv(1024)
    if data:
        request = data.decode()[:-2]
        request_data = data.decode()[:4]
        if request_data == 'quit':
            logger.info('closing connection %s', sock)
            selector.unregister(sock)
            sock.close()
            return
        if request_data == 'time':
            response = get_time()
        elif request_data == 'info':
            response = get_info_os()
        elif request_data == 'find':
            response = search_file(request)
        else:
            response = handle_request()
        sock.send(response)
    else:
        logger.info('closing connection %s', sock)
        selector.unregister(sock)
        sock.close()


def run_iteration(selector: selectors.BaseSelector):
    events = selector.select()
    for key, mask in events:
        callback = key.data
        callback(selector, key.fileobj)


def serve_forever():
    """
    Метод запускает сервер на постоянное прослушивание новых сообщений
    """
    with selectors.SelectSelector() as selector:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            server_socket.bind((HOST, PORT))
            server_socket.listen()
            server_socket.setblocking(False)
            logger.info('Server started on port %s', PORT)

            selector.register(server_socket, selectors.EVENT_READ, new_connection)

            while True:
                run_iteration(selector)


if __name__ == '__main__':
    serve_forever()

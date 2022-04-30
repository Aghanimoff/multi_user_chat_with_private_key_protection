import socket  # Библиотека для работы с сокетами
import threading  # Библиотека для работы с потоками


def send_all(data):
    """
    Функция отправляет данные всем пользователям
    """

    for user in users:
        user.send(data)  # Отправляет данные всем пользователям.
        # У сервера нет задачи читать данные, поэтому они ретранслируются без изменений


def listen_user(user_socket):
    """
    Функция 'слушает' пользователя.
    Блокирующий метод .recv()
    """
    while True:
        data = user_socket.recv(2048)  # Блокирующая функция, принимает данные от пользователя
        print(f'Сообщение {data}')
        send_all(data)


def start_server():
    """
    Основная функция сервера.
    Её задача - принимать новых пользователей
    И создавать для них новый поток
    Блокирующий метод accept()
    """
    while True:
        user_socket, address = server.accept()  # принимает подключения, блокирующая функция
        print(f'Новый пользователь: {user_socket}')
        print(f'Новый адрес: {address}')
        users.append(user_socket)  # Добавляет сокет пользователя
        listen_accepted_user = threading.Thread(target=listen_user, args=(user_socket,))  # Задаёт параметры потока
        listen_accepted_user.start()  # Запускат новый поток


if __name__ == '__main__':

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, )  # определяет тип подключения
    server.bind(('localhost', 4044))  # биндит сервер по протоколу TCP/IP
    server.listen(5)  # Разрешает входящие подключения

    print('Сервер начал принимать подключения...')
    users = []  # Создаёт пустой список пользователей

    start_server()  # Запускает сервер

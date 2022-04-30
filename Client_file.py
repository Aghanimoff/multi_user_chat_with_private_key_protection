import socket  # Библиотека для работы с сокетами
from threading import Thread  # Библиотека для работы с потоками
from datetime import datetime  # Используется для указания времени
from os import system  # Отправляет команды в Shell, из которой исполняется код

from cryptography.fernet import Fernet, InvalidToken  # Криптографический модуль, AES и ошибка
from cryptography.exceptions import InvalidSignature  # Отлов ошибки


def load_key():
    """
    Загружаем ключ 'crypto.key' из текущего каталога
    """
    return open('crypto.key', 'rb').read()


def encrypt(data, key1):
    """
    Функция принимает байт-данные и возвращает зашифрованные по ключу
    """
    return Fernet(key1).encrypt(data)


def decrypt(data, key1):
    """
    Функция принимает зашифрованные данные и возвращает расшифрованные по ключу
    """
    try:
        return Fernet(key1).decrypt(data)

    # Отлов ошибок неправильных ключей
    except InvalidSignature:
        pass
    except InvalidToken:
        pass

    return '...Это сообщение отправлено под другим ключём шифрования...'.encode('utf-8')


def listen_server():
    """
    Функция принимает данные с сервера. Блокирующий метод .recv()
    """
    chat = f'session start as {MyName} at {datetime.now()}\n=========================\n'
    while True:
        data = decrypt(client.recv(2048), key1)  # принимает данные с сервера
        chat += f'{data.decode("utf - 8")}\n'  # обновляет переменную str с историей чата для этого потока
        system('cls')  # команда для cmd - очистка консоли
        print(chat + '=========================\n===Введите сообщение: ===\n')


def send_server():
    """
    Функция отправляет данные на сервер. Блокирующая функция input()
    """
    listen_thread = Thread(target=listen_server)  # создаёт поток для отлова данных с сервера
    listen_thread.start()  # запускает поток
    while True:
        message = (MyName + ': ' + input('=========================\n===Введите сообщение: ===\n')).encode('utf-8')  # Создаёт данные (ввод), кодировка в utf-8
        try:
            encrypted_message = encrypt(message, key1)  # зашифровывает данные
            try:
                client.send(encrypted_message)  # отправляет данные на сервер

            except TypeError:
                # отлов ошибки некорректного формата ключа
                print('Некорректный формат ключа. Проверьте файл crypto.key')
                return

        except ValueError:
            # отлов ошибки некорректного состава ключа
            print('Ключ Fernet должен состоять из 32 байтов в кодировке base64')
            return


if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM, )  # определяет тип подключения
    client.connect(('localhost', 4044))  # определяет IP адресного пространства и порт подключения

    key1 = load_key()  # загрузка ключа шифрования из файла

    MyName = input('Введите своё имя: ')
    send_server()

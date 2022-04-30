from cryptography.fernet import Fernet  # Криптографический модуль, метод шифрования - AES, на симметричных ключах


def write_key():
    """
    Функция генерирует ключ симметричный ключ шифрования
    И сохраняет его в файл
    """
    key = Fernet.generate_key()
    with open('crypto.key', 'wb') as key_file:
        key_file.write(key)


if __name__ == "__main__":
    write_key()

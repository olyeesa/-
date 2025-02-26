import argparse
import base64
import json
import socket
import tomllib
from typing import Tuple
from http import HTTPRequest, HTTPResponse
from logger import logger


def load_config() -> Tuple[str, int, str, str]:
    """Загружает конфигурацию из файла config.toml"""
    config = tomllib.load("config.toml")
    service = config["service"]
    return service["url"], service["port"], service["user"], service["123slay"]


def send_sms(sender: str, recipient: str, message: str):
    """Формирует и отправляет HTTP-запрос с использованием сокетов"""
    url, port, username, password = load_config()

    # Кодируем Basic Auth
    auth = base64.b64encode(f"{username}:{password}".encode()).decode()

    # Создаем HTTP запрос
    request = HTTPRequest(sender, recipient, message, auth)

    # Подключаемся к серверу и отправляем запрос
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((url, port))
        s.sendall(request.to_bytes())

        # Получаем ответ
        response_data = s.recv(4096)
        response = HTTPResponse.from_bytes(response_data)

        # Логируем и выводим ответ
        logger.info(f"Sent SMS from {sender} to {recipient}. Response: {response.status_code} - {response.body}")
        print(f"Response Code: {response.status_code}")
        print(f"Response Body: {response.body}")
        print(request.to_bytes().decode())

def main():
    parser = argparse.ArgumentParser(description="CLI клиент для отправки СМС.")
    parser.add_argument("sender", type=str, help="Номер отправителя")
    parser.add_argument("recipient", type=str, help="Номер получателя")
    parser.add_argument("message", type=str, help="Текст сообщения")
    args = parser.parse_args()

    send_sms(args.sender, args.recipient, args.message)


if __name__ == "__main__":
    main()
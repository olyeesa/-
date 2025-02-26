import json
from typing import Self


class HTTPRequest:
    def __init__(self, sender: str, recipient: str, message: str, auth: str):
        self.sender = sender
        self.recipient = recipient
        self.message = message
        self.auth = auth

    def to_bytes(self) -> bytes:
        """Формирует HTTP-запрос в байтах"""
        body = json.dumps({
            "sender": self.sender,
            "recipient": self.recipient,
            "message": self.message
        })

        # ВАЖНО: Должен быть именно `/send_sms`, без `/` в конце
        request_line = "POST /send_sms HTTP/1.1\r\n"

        headers = (
            f"Host: localhost:4010\r\n"
            f"Authorization: Basic {self.auth}\r\n"
            f"Content-Type: application/json\r\n"
            f"Content-Length: {len(body)}\r\n"
            f"Connection: close\r\n\r\n"
        )

        return (request_line + headers).encode() + body.encode()

class HTTPResponse:
    """Класс для обработки HTTP-ответа"""

    def __init__(self, status_code: int, body: str):
        self.status_code = status_code
        self.body = body

    def to_bytes(self) -> bytes:
        """Конвертирует объект в HTTP-ответ в формате байтов"""
        response = f"HTTP/1.1 {self.status_code} OK\r\n\r\n{self.body}"
        return response.encode()

    @classmethod
    def from_bytes(cls, binary_data: bytes) -> Self:
        """Создает объект HTTPResponse из байтов"""
        response_str = binary_data.decode()
        lines = response_str.split("\r\n")
        status_code = int(lines[0].split(" ")[1])
        body = "\n".join(lines[lines.index("") + 1:])
        return cls(status_code, body)
from PySide6.QtCore import QIODevice
from PySide6.QtNetwork import QHttpPart, QNetworkRequest


class HttpPart(QHttpPart):
    def __init__(self, *other: QHttpPart,
                 body: bytes | str = None,
                 body_device: QIODevice = None,
                 headers: list[tuple[QNetworkRequest.KnownHeaders | str, str]] = None,
                 ):
        super().__init__(*other)
        self.__body_device: QIODevice = None

        for (key, value) in headers:
            if isinstance(key, str):
                self.setRawHeader(key.encode(), value.encode())
            else:
                self.setHeader(key, value.encode())

        if body is not None:
            self.setBody(body if isinstance(body, bytes) else f'{body}'.encode())

        if body_device:
            self.__body_device = body_device
            self.setBodyDevice(body_device)

    def bodyDevice(self) -> QIODevice | None:
        return self.__body_device

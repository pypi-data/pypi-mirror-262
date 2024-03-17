from PySide6.QtNetwork import QNetworkRequest


class NetworkRequest(QNetworkRequest):
    def setHeader(self, header: QNetworkRequest.KnownHeaders | str, value: object) -> None:
        if isinstance(header, str):
            super().setRawHeader(header.encode(), f'{value}'.encode())
            return
        super().setHeader(header, value)

    def header(self, header: QNetworkRequest.KnownHeaders | str) -> object:
        if isinstance(header, str):
            return super().rawHeader(header.encode()).data().decode()
        return super().header(header)

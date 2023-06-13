"""Задача этого клиента подключиться к облаку и получать файлы.
    client.move(remote_path_from="dir1/file1", remote_path_to="dir2/file1")
    client.move(remote_path_from="dir2", remote_path_to="dir3")

    client.download_sync(remote_path="dir1/file1", local_path="~/Downloads/file1")
    client.download_sync(remote_path="dir1/dir2/", local_path="~/Downloads/dir2/")

    client.upload_sync(remote_path="dir1/file1", local_path="~/Documents/file1")
    client.upload_sync(remote_path="dir1/dir2/", local_path="~/Documents/dir2/")

    # Load resource
    kwargs = {
     'remote_path': "dir1/file1",
     'local_path':  "~/Downloads/file1",
     'callback':    callback
    }
    client.download_async(**kwargs)

    kwargs = {
     'remote_path': "dir1/dir2/",
     'local_path':  "~/Downloads/dir2/",
     'callback':    callback
    }
    client.download_async(**kwargs)

    # Upload resource
    kwargs = {
     'remote_path': "dir1/file1",
     'local_path':  "~/Downloads/file1",
     'callback':    callback
    }
    client.upload_async(**kwargs)

    kwargs = {
     'remote_path': "dir1/dir2/",
     'local_path':  "~/Downloads/dir2/",
     'callback':    callback
    }
    client.upload_async(**kwargs)
"""

import urllib3
from webdav3.client import Client
from webdav3.exceptions import ResponseErrorCode

from yandex import logger as logging
from yandex.clients.baseclient import BaseClient
from yandex.errors import ClientConnectionError
from yandex.resources import PNG_TRASH
from yandex.schemas import File
from yandex.settings import ya_settings

urllib3.disable_warnings()


class WebDAVClient(BaseClient):
    """WebDAVClient."""

    def __init__(self):
        self.client = self._init_client()

    def _init_client(self) -> Client:
        """_init_client.

        Returns:
            Client:

        Raises:
            ClientConnectionError: если не удалось подключиться
        """
        client = Client(ya_settings.credentials)
        client.verify = False  # To not check SSL certificates (Default = True)

        try:
            client.free()
        except ResponseErrorCode:
            raise ClientConnectionError(f"Can't connect to {ya_settings.server}")

        logging.info(f"Connected to {ya_settings.server}")
        return client

    def __repr__(self) -> str:
        """__repr__.

        Returns:
            str:
        """
        return f"<WebDAVClient: {ya_settings.server}>"

    def files(self, folder: str, is_recursive: bool = False) -> File:
        """Генерирует файлы из принимаемой папки.

        Args:
            folder (str): folder
            is_recursive (bool): рекурсивный поиск файлов по вложенным папкам

        Yields:
            File:
        """
        for file in self.client.list(folder, get_info=True):
            if file.get("isdir") and is_recursive:
                # TODO это надо проверить
                yield from self.files(file)
            yield File(**file)

    def delete_file(self, file: File):
        try:
            self.client.move(remote_path_from=file.path, remote_path_to=PNG_TRASH)
        # TODO найти ошибку и подставить сюда
        except Exception as err:
            logging.error(f"Error while move {file.name}: {err}")
            return False
        else:
            logging.info(f"File: {file.name} moved to {PNG_TRASH}")
            return True

    def download_file(self, file: File):
        self.client.download_sync(
            remote_path=file.path,
            local_path="~/Downloads/file1",
        )

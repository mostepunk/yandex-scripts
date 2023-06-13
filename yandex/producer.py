"""Продьюсер.

Генерирует задания для воркеров.
"""

import re

from yandex import logger as logging
from yandex.clients import BaseClient
from yandex.resources import (CONVERT, DELETE, HEIC_EXT, NEXTCLOUD_FILENAME,
                              PNG_EXT, RENAME, RENAME_DELETE)
from yandex.schemas import File


class Producer:
    """Producer."""

    def __init__(self, dav: BaseClient, db: BaseClient):
        self.dav = dav
        self.db = db

    def start(self, folder: str):
        """start.

        Args:
            folder (str): folder
        """
        logging.info(f"Scanning {folder}")
        for file in self.dav.files(folder):

            if self.is_png(file.name):
                self.delete(file)
                continue

            if self.is_rename(file.name) and self.is_heic(file.name):
                self.rename_and_convert(file)
                continue

            if self.is_rename(file.name):
                self.rename(file)
                continue

            if self.is_heic(file.name):
                self.convert(file)
                continue

    def rename_and_convert(self, file: File):
        logging.info(f"Rename and convert: {file.name}")
        self.save_to_db(file, RENAME_DELETE)

    def rename(self, file: File):
        """rename.

        Args:
            file (File): file
        """
        logging.info(f"Rename: {file.name}")
        self.save_to_db(file, RENAME)

    def convert(self, file: File):
        """convert.

        Args:
            file (File): file
        """
        logging.info(f"Convert: {file.name}")
        self.save_to_db(file, CONVERT)

    def delete(self, file: File):
        """for_or_del.

        Args:
            file (File): file
        """
        logging.info(f"Delete: {file.name}")
        self.save_to_db(file, DELETE)

    def save_to_db(self, file: File, task: str):
        self.db.add_task(file, task)

    def is_rename(self, filename: str) -> bool:
        """is_rename.

        Args:
            filename (str): filename

        Returns:
            bool:
        """
        if re.search(NEXTCLOUD_FILENAME, filename):
            return False
        return True

    def is_png(self, filename: str) -> bool:
        """is_png.

        Args:
            filename (str): filename

        Returns:
            bool:
        """
        if re.search(PNG_EXT, filename):
            return True
        return False

    def is_heic(self, filename: str) -> bool:
        """is_heic.

        Args:
            filename (str): filename

        Returns:
            bool:
        """
        # if re.search(NEXTCLOUD_FILENAME, filename) and re.search(HEIC_EXT, filename):
        if re.search(HEIC_EXT, filename):
            return True
        return False

    def __repr__(self) -> str:
        """Returns a string representation of class instance.

        Args:

        Returns:
            str:
        """
        return f"<Producer. DAVClient: {self.dav}, DBClient: {self.db}>"

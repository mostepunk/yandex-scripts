"""Переименовыватель файлов.

Может переименовать файл двумя способами:
    1. Если это яндексовское имя, то тут проще всего. Заменить пробелы на _ и убрать дефисы.
    2. Если это другое имя:
        - скачать файл
        - найти дату в exif данных
        - переименовать файл
        - загрузить его в облако
"""

import contextlib
import re
from datetime import datetime

import PIL.Image
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import UnidentifiedImageError
from pillow_heif import register_heif_opener

from yandex import logger as logging
from yandex.clients import BaseClient
from yandex.resources import YANDEX_FILENAME
from yandex.schemas import File

register_heif_opener()

# TODO: привести этот код к порядку и сделать его в ООП


class Renamer:
    def __init__(self, dav: BaseClient, file: File):
        self.dav = dav
        self.file = file

    def rename(self):
        if re.search(YANDEX_FILENAME, self.file.name):
            return self.rename_yandex(self.file.name)
        return self.download_and_rename()

    def update_file(self, new_filename: str):
        try:
            self.dav.rename(self.file, new_filename)
        except Exception as err:
            logging.error(f"Error renaming {self.file.name}: {err}")
            return False
        else:
            return new_filename

    def rename_yandex(self, old_name: str) -> str:
        """Заменить яндексовское имя 2023-01-06 19-36-07.JPG
        на нормальное, к которому я уже приывык 20230106_193607.JPG
        """
        return old_name.replace(" ", "_").replace("-", "")

    def extract_exif(self, file_path: str) -> dict:
        """Извлечь метадату из файла фотографии."""
        try:
            img = PIL.Image.open(file_path)
            return img.getexif()
        except UnidentifiedImageError:
            parser = createParser(file_path)
            metadata = extractMetadata(parser)
            if metadata is None:
                return None
            meta = metadata.exportDictionary()

            with contextlib.suppress(ValueError):
                meta[306] = metadata.get("creation_date").strftime("%Y:%m:%d %H:%M:%S")
            return meta

    def generate_filename(self, file_path: str):
        """Сгенерировать новое имя файла."""
        exif_data = self.extract_exif(file_path)

        if not exif_data:
            logging.warning(f"{file_path} No exif data")
            return file_path

        logging.info(f"{file_path} Exif Data: {exif_data}")

        try:
            # 2023:01:06 19:32:57
            date = datetime.strptime(exif_data[306], "%Y:%m:%d %H:%M:%S")
            logging.info(f"Found date: {date}")
            return date.strftime("%Y%m%d_%H%M%S")
        except KeyError:
            logging.warning(f"--> ERROR: Exif data is strange. return {self.file.name}")
            return self.file.name

    def download_and_rename(self):
        """Переименовать файл исходя из даты съемки.

        Она как правило лежит в exif данных под ключом 306,
        По крайней мере так они мне попадались.
        """
        downloaded_file_path = self.dav.download_file(self.file)
        new_file_name = self.generate_filename(downloaded_file_path)
        logging.info(f"New name for file {self.file.name}: {new_file_name}")
        return new_file_name


def rename_worker(file: File, dav: BaseClient):
    r = Renamer(dav, file)
    new_filename = r.rename()
    return r.update_file(new_filename)

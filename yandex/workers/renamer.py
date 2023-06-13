"""Переименовыватель файлов.

Может переименовать файл двумя способами:
    1. Если это яндексовское имя, то тут проще всего. Заменить пробелы на _ и убрать дефисы.
    2. Если это другое имя:
        - скачать файл
        - найти дату в exif данных
        - переименовать файл
        - загрузить его в облако
"""

import pathlib as pl
import re
from datetime import datetime

import PIL.Image
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import UnidentifiedImageError
from pillow_heif import register_heif_opener

from yandex import logger as logging
from yandex.clients import BaseClient
from yandex.schemas import File

register_heif_opener()


heic = ".HEIC"
heic_ext = r"\.(HEIC|heic)$"

# 2023-01-06 19-36-07.JPG
yandex_filename = r"\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}\.\w+"
# yandex_filename = r"\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}\.(HEIC|JPG|heic|jpg)"

# IMG_5555.heic
iphone_filename = r"IMG_\d+\.\w+"
# iphone_filename = r"IMG_\d+\.(HEIC|heic)"

# 20230106_193257.HEIC
nextcloud_filename = r"\d{8}_\d{6}\.\w+"
# 20230106_193257
nextcloud_date = r"\d{8}_\d{6}"
# nextcloud_filename = r"\d{8}_\d{6}\.(HEIC|JPG|heic|jpg)"
log_file = r"\d{4}-\d{2}-\d{2}.log"


# TODO: привести этот код к порядку и сделать его в ООП


class Renamer:
    def __init__(self, dav: BaseClient, file: File):
        self.dav = dav
        self.file = file

    def rename(self):
        if re.search(yandex_filename, self.file.name):
            return self.rename_yandex(self.file.name)
        return self.rename_file(self.file)

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

    def extract_exif(self):
        """Извлечь метадату из файла фотографии."""
        try:
            img = PIL.Image.open(self.file.path)
            return img.getexif()
        except UnidentifiedImageError:
            parser = createParser(self.file.path)
            metadata = extractMetadata(parser)
            if metadata is None:
                return None
            meta = metadata.exportDictionary()
            try:
                meta[306] = metadata.get("creation_date").strftime("%Y:%m:%d %H:%M:%S")
            except ValueError:
                pass
            return meta

    def generate_filename(self):
        """Сгенерировать новое имя файла."""
        logging.info(f"=== {self.file.name}:")
        exif_data = self.extract_exif()

        if not exif_data:
            logging.info(f"--> WARN: {self.file.name} No exif data")
            return self.file.name

        logging.info(f"{self.file.name} Exif Data: {exif_data}")

        try:
            # 2023:01:06 19:32:57
            date = datetime.strptime(exif_data[306], "%Y:%m:%d %H:%M:%S")
            logging.info(f"Found date: {date}")
            return date.strftime("%Y%m%d_%H%M%S") + self.file.suffix
        except KeyError:
            logging.warning(f"--> ERROR: Exif data is strange. return {self.file.name}")
            return self.file.name

    def rename_file(self):
        """Переименовать файл исходя из даты съемки.

        Она как правило лежит в exif данных под ключом 306,
        По крайней мере так они мне попадались.
        """
        downloaded_file = self.dav.download(self.file)
        target = pl.Path(file.parent / generate_filename(file))
        ff = self.generate_filename(downloaded_file)


def rename_worker(file: File, dav: BaseClient):
    logging.info(f"Rename {file.name} -> ")
    r = Renamer(dav, file)
    new_filename = r.rename()
    return r.update_file(new_filename)

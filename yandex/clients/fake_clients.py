from random import choice, randint

from yandex import logger as logging
from yandex.clients.baseclient import BaseClient
from yandex.resources import CONVERT, DELETE, PNG_TRASH, RENAME, RENAME_DELETE
from yandex.schemas import File


class FakeWebDAV(BaseClient):
    def __init__(self):
        self.client = "FakeWebDAV"
        logging.info("Imitate WebDAV client")

    def files(self, folder: str) -> File:
        for _ in range(randint(1, 20)):
            yield File(**self.fake_file(folder))

    def delete_file(self, file: File):
        logging.info(f"File: {file.name} moved to {PNG_TRASH}")
        return True

    def __repr__(self) -> str:
        """__repr__.

        Returns:
            str:
        """
        return "<FakeWebDAV>"

    def fake_file(self, folder: str) -> dict:
        filenames = [
            "20200531_174121.JPG",
            "20200531_174121.HEIC",
            "2020-05-30 17-00-00.HEIC",
            "2020-05-31 17-41-21.JPG",
            "2020-05-31 17-41-21.PNG",
            # "IMG_0511",
        ]
        filname = choice(filenames)
        path = f"{folder}/{filname}"
        return {
            "content_type": "image/jpeg",
            "created": "2023-05-24T20:33:48Z",
            "etag": "1d00b7dc3413a58a6729c1fa16f80eff",
            "isdir": "false",
            "modified": "Tue, 30 May 2023 15:12:24 GMT",
            "name": filname,
            "path": path,
            "size": "115226",
        }


class FakeDatabase(BaseClient):
    """Fake database.

    БД в которой будут храниься задания для воркеров.
    """

    def __init__(self):
        self.client = "FakeDatabase"
        self._files = []
        self._tasks = []
        logging.info("Imitate Database client")

    def files(self, folder: str):
        for file in self._files:
            yield file

    def add_task(self, file: File, task: str):
        self._tasks.append((file, task))

    @property
    def all_tasks(self):
        return self._tasks

    @property
    def rename_tasks(self):
        return [row for row in self._tasks if row[1] == RENAME]

    @property
    def convert_tasks(self):
        return [row for row in self._tasks if row[1] == CONVERT]

    @property
    def rename_convert_tasks(self):
        return [row for row in self._tasks if row[1] == RENAME_DELETE]

    @property
    def delete_tasks(self):
        return [row for row in self._tasks if row[1] == DELETE]

    def __repr__(self):
        return "<FakeDatabase>"

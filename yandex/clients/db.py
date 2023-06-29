from yandex.resources import CONVERT, DELETE, RENAME, RENAME_CONVERT
from yandex.schemas import File
from yandex.settings import db_settings


class Database:
    def __init__(self):
        self.db = db_settings.db_name

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
        return [row for row in self._tasks if row[1] == RENAME_CONVERT]

    @property
    def delete_tasks(self):
        return [row for row in self._tasks if row[1] == DELETE]

    def __repr__(self):
        return "<FakeDatabase>"

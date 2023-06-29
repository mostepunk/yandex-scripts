"""Главный консьюмер, который читает БД и раздает задания для воркеров."""

import time
from concurrent.futures import ThreadPoolExecutor

from yandex.clients import BaseClient
from yandex.settings import pool_settings
from yandex.workers import convert_worker, delete_worker, rename_worker


class Consumer:
    def __init__(self, db: BaseClient, dav: BaseClient):
        self.db = db
        self.dav = dav
        self.delete_pool = ThreadPoolExecutor(pool_settings.delete_pool_size)
        self.rename_pool = ThreadPoolExecutor(pool_settings.rename_pool_size)
        self.convert_pool = ThreadPoolExecutor(pool_settings.convert_pool_size)

    def start(self):
        self.delete()
        self.rename()
        self.convert()

    def rename(self):
        succsess = False
        for file, _ in self.db.rename_tasks:
            succsess = False
            while not succsess:
                answer = self.rename_pool.submit(rename_worker, file, self.dav)
                succsess = answer.result()
                if not succsess:
                    time.sleep(3)
                else:
                    break
        return succsess

    def convert(self):
        for file, _ in self.db.convert_tasks:
            succsess = False
            while not succsess:
                answer = self.convert_pool.submit(convert_worker, file, self.dav)
                succsess = answer.result()
                if not succsess:
                    time.sleep(3)

    def rename_convert(self):
        ...

    def delete(self):
        for file, _ in self.db.delete_tasks:
            succsess = False
            while not succsess:
                answer = self.delete_pool.submit(delete_worker, file, self.dav)
                succsess = answer.result()
                if not succsess:
                    time.sleep(3)

from yandex import logger as logging
from yandex.clients import BaseClient
from yandex.schemas import File


class DeleteWorker:
    def __init__(self):
        ...


def delete_worker(file: File, dav: BaseClient):
    try:
        dav.delete_file(file)
    except Exception as err:
        logging.error(f"Error on deleting {file.name}: {err}")
        return False
    else:
        return True

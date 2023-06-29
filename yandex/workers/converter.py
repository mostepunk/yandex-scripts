import os
import subprocess

from yandex import logger as logging
from yandex.clients import BaseClient
from yandex.schemas import File


def convert_file(src: str, dst: str):
    cmd = f'convert "{src}" -quality 100 -verbose "{dst}"'
    subprocess.check_output(cmd, shell=True, text=True)


def convert_worker(file: File, dav: BaseClient):
    src = dav.download_file(file)
    f, _ = os.path.splitext(src)
    dst = f + ".jpg"

    convert_file(src, dst)
    dav.delete_file(file)

    return True

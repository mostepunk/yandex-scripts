from yandex.clients import FakeDatabase, FakeWebDAV
from yandex.consumer import Consumer
from yandex.producer import Producer
from yandex.settings import app_settings


def main():
    db = FakeDatabase()
    dav = FakeWebDAV()

    p = Producer(dav=dav, db=db)
    p.start(app_settings.VOVA_PHOTOS)

    c = Consumer(db=db, dav=dav)
    c.start()


if __name__ == "__main__":
    main()

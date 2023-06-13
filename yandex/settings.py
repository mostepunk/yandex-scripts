"""Настройки для проекта."""

from pydantic import BaseSettings, SecretStr


class YandexSettings(BaseSettings):
    """YandexSettings."""

    server: str = "https://webdav.yandex.ru"
    login: str
    password: SecretStr

    @property
    def credentials(self) -> dict:
        """credentials.

        Returns:
            dict:
        """
        return {
            "webdav_hostname": self.server,
            "webdav_login": self.login,
            "webdav_password": self.password.get_secret_value(),
        }


class DatabaseSettings(BaseSettings):
    db_name: str = "ya.db"
    url: str = ""


class PoolSettings(BaseSettings):
    delete_pool_size: int = 4
    rename_pool_size: int = 4


ya_settings = YandexSettings()
db_settings = DatabaseSettings()
pool_settings = PoolSettings()

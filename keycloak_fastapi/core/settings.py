
"""
Settings Module.
"""

from functools import lru_cache
from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ValidationError, AnyHttpUrl

class DatabaseSettings(BaseSettings):
    """
    Database settings class.

    Attributes:
        url (str): Database URL.
        pool_size (int): Connection pool size.
        max_overflow (int): Max overflow.
        echo (bool): If True, print SQL statements. For debugging.
        pool_pre_ping (bool): If True, ping the database before each query.
        pool_recycle (int): Connection pool recycle time in seconds.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="POSTGRES_", case_sensitive=False
    )
    url: str = "sqlite+aiosqlite:///:memory:"
    pool_size: int = 8
    max_overflow: int = 16
    echo: bool = False
    pool_pre_ping: bool = False
    pool_recycle: int = 3600

class AuthSettings(BaseSettings):
    """
    Auth settings class.

    Attributes:
        server_url (str): Server URL.
        client_id (str): Client ID.
        realm_name (str): Realm name.
        client_secret (str): Client secret.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="KEYCLOAK_", case_sensitive=False
    )
    server_url: str = "http://0.0.0.0:8080"
    client_id: str = "open_id_client"
    realm_name: str = "keyauth"
    client_secret: str = "9m0qsBElC17Bj3A2cfI5xkl54Xsi1Ybo"


@lru_cache
def load_settings(settings_cls_name: str) -> BaseSettings:
    """
    Load settings.

    Args:
        settings_cls_name (str): Settings class name.

    Returns:
        BaseSettings: Settings class.
    """
    load_dotenv(find_dotenv())
    settings_cls = globals()[settings_cls_name]
    return settings_cls()

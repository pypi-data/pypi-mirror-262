from pydantic import BaseModel, RedisDsn


class CeleryConfig(BaseModel):
    CELERY_CONCURRENCY: int
    CELERY_PREFETCH_MULTIPLIER: int


class CeleryReadBeatConfig(BaseModel):
    """Represents configuration for celery-redbeat.

    By default, celery-redbeat will configure itself using celery settings,
    so use this class and override celery settings only if you are sure of implications.

    For avoiding config duplication ensure trying to reuse
    [`RedisConnection`][kyotsu.config.databases.models.RedisConnection] first, and specify REDIS_DB only.

    Attributes:
        REDIS_URL: URL to redis server used to store the schedule
        REDIS_DB:
        REDIS_USE_SSL:
        KEY_PREFIX:
        LOCK_KEY:
        LOCK_TIMEOUT:
    """

    REDIS_URL: RedisDsn | None
    REDIS_DB: int | None
    REDIS_USE_SSL: bool = False
    KEY_PREFIX: str = "redbeat"
    LOCK_KEY: str = "redbeat:lock"
    LOCK_TIMEOUT: int = 1500

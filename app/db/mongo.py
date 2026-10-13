import logging

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings
from app.models.notification import Notification

logger = logging.getLogger(__name__)

_client: AsyncIOMotorClient | None = None


async def init_mongo() -> None:
    global _client
    _client = AsyncIOMotorClient(settings.mongo_url)
    await init_beanie(
        database=_client[settings.mongo_db],
        document_models=[Notification],
    )
    logger.info("MongoDB conectado: %s/%s", settings.mongo_url, settings.mongo_db)


async def close_mongo() -> None:
    global _client
    if _client:
        _client.close()
        _client = None

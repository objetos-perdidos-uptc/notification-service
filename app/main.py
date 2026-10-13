import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import eureka
from app.config import settings
from app.db.mongo import close_mongo, init_mongo
from app.routers import notifications

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("notification-service")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Arrancando %s en puerto %s", settings.app_name, settings.port)
    await init_mongo()
    await eureka.register()
    hb_task = asyncio.create_task(eureka.heartbeat_loop())
    yield
    logger.info("Apagando %s...", settings.app_name)
    hb_task.cancel()
    try:
        await hb_task
    except asyncio.CancelledError:
        pass
    await eureka.deregister()
    await close_mongo()


app = FastAPI(
    title="Notification Service",
    version="0.1.0",
    description="Notificaciones para usuarios y alertas de fraude.",
    lifespan=lifespan,
)

app.include_router(notifications.router)


@app.get("/health", tags=["infra"])
async def health() -> dict:
    return {"status": "UP", "service": settings.app_name, "port": settings.port}


@app.get("/", tags=["infra"])
async def root() -> dict:
    return {"service": settings.app_name, "docs": "/docs"}

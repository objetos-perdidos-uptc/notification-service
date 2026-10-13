import asyncio
import logging
from typing import Optional

import httpx

from app.config import settings

logger = logging.getLogger(__name__)
APP_NAME = settings.app_name.upper()
_instance_id: Optional[str] = None


def _payload() -> dict:
    host, port = settings.host_name, settings.port
    return {
        "instance": {
            "instanceId": f"{host}:{APP_NAME.lower()}:{port}",
            "hostName": host,
            "app": APP_NAME,
            "ipAddr": settings.ip_addr,
            "status": "UP",
            "port": {"$": port, "@enabled": "true"},
            "dataCenterInfo": {
                "@class": "com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo",
                "name": "MyOwn",
            },
            "leaseInfo": {"renewalIntervalInSecs": 30, "durationInSecs": 90},
            "homePageUrl": f"http://{host}:{port}/",
            "statusPageUrl": f"http://{host}:{port}/health",
            "healthCheckUrl": f"http://{host}:{port}/health",
            "vipAddress": APP_NAME.lower(),
        }
    }


async def register() -> None:
    global _instance_id
    url = f"{settings.eureka_url}/apps/{APP_NAME}"
    payload = _payload()
    _instance_id = payload["instance"]["instanceId"]
    for intento in range(1, 11):
        try:
            async with httpx.AsyncClient(timeout=5.0) as c:
                r = await c.post(url, json=payload, headers={"Content-Type": "application/json"})
                if r.status_code in (200, 204):
                    logger.info("Eureka: registrado como %s", _instance_id)
                    return
        except (httpx.ConnectError, httpx.TimeoutException) as e:
            logger.warning("Eureka no disponible (%s): %s", intento, e)
        await asyncio.sleep(5)
    logger.error("Eureka: no se pudo registrar")


async def heartbeat_loop() -> None:
    if not _instance_id:
        return
    url = f"{settings.eureka_url}/apps/{APP_NAME}/{_instance_id}"
    while True:
        try:
            async with httpx.AsyncClient(timeout=5.0) as c:
                await c.put(url)
        except Exception:  # noqa: BLE001
            pass
        await asyncio.sleep(30)


async def deregister() -> None:
    if not _instance_id:
        return
    url = f"{settings.eureka_url}/apps/{APP_NAME}/{_instance_id}"
    try:
        async with httpx.AsyncClient(timeout=5.0) as c:
            await c.delete(url)
    except Exception:  # noqa: BLE001
        pass

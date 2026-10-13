from beanie import PydanticObjectId

from app.models.notification import Notification
from app.schemas.notification_dto import NotificationCreate, NotificationType


async def create_notification(payload: NotificationCreate) -> Notification:
    notif = Notification(**payload.model_dump())
    await notif.insert()
    return notif


async def list_for_user(user_id: int, unread_only: bool = False) -> list[Notification]:
    query = {"userId": user_id}
    if unread_only:
        query["isRead"] = False
    return await Notification.find(query).sort("-dateTime").to_list()


def _parse_id(notif_id: str) -> PydanticObjectId:
    """Convierte el string a ObjectId o lanza ValueError si no es válido."""
    try:
        return PydanticObjectId(notif_id)
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"ID de notificación inválido: {notif_id}") from e


async def mark_as_read(notif_id: str, user_id: int) -> Notification:
    oid = _parse_id(notif_id)
    notif = await Notification.get(oid)
    if not notif:
        raise LookupError("Notificación no encontrada")
    if notif.userId != user_id:
        raise PermissionError("No es tu notificación")
    if not notif.isRead:
        notif.isRead = True
        await notif.save()
    return notif


async def list_fraud_alerts(limit: int = 100) -> list[Notification]:
    """HU-17: alertas de fraude para el admin."""
    return (
        await Notification.find(Notification.type == NotificationType.FRAUD_ALERT)
        .sort("-dateTime")
        .limit(limit)
        .to_list()
    )

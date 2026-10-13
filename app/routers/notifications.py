import logging

from fastapi import APIRouter, Depends, HTTPException, Query

from app.dependencies import current_user_id, require_admin
from app.models.notification import Notification
from app.schemas.notification_dto import NotificationCreate, NotificationOut
from app.services import notification_service as svc

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/notifications", tags=["notifications"])


def _out(n: Notification) -> NotificationOut:
    return NotificationOut(
        id=str(n.id),
        userId=n.userId,
        type=n.type,
        message=n.message,
        refReportId=n.refReportId,
        dateTime=n.dateTime,
        isRead=n.isRead,
    )


@router.post("", status_code=201, response_model=NotificationOut)
async def create(payload: NotificationCreate) -> NotificationOut:
    notif = await svc.create_notification(payload)
    logger.info("Notificación creada para user=%s tipo=%s", notif.userId, notif.type)
    return _out(notif)


@router.get("/me", response_model=list[NotificationOut])
async def my_notifications(
    unread: bool = Query(False),
    user_id: int = Depends(current_user_id),
) -> list[NotificationOut]:
    items = await svc.list_for_user(user_id, unread_only=unread)
    return [_out(n) for n in items]


@router.patch("/{notif_id}/read", response_model=NotificationOut)
async def mark_read(
    notif_id: str,
    user_id: int = Depends(current_user_id),
) -> NotificationOut:
    try:
        notif = await svc.mark_as_read(notif_id, user_id)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except LookupError as e:
        raise HTTPException(404, str(e))
    except PermissionError as e:
        raise HTTPException(403, str(e))
    return _out(notif)


@router.get("/admin/alerts", response_model=list[NotificationOut])
async def admin_alerts(
    limit: int = Query(100, ge=1, le=500),
    _admin: str = Depends(require_admin),
) -> list[NotificationOut]:
    items = await svc.list_fraud_alerts(limit=limit)
    return [_out(n) for n in items]

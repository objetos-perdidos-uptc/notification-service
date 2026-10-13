from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class NotificationType(str, Enum):
    HIGH_MATCH = "HIGH_MATCH"
    CLAIM = "CLAIM"
    FRAUD_ALERT = "FRAUD_ALERT"
    EXPIRING_SOON = "EXPIRING_SOON"
    EXPIRED_INFO = "EXPIRED_INFO"


class NotificationCreate(BaseModel):
    """Lo que envían matching-service, claim-service o el cron de report."""
    userId: int
    type: NotificationType
    message: str
    refReportId: Optional[int] = None


class NotificationOut(BaseModel):
    """Lo que se devuelve al frontend."""
    id: str
    userId: int
    type: NotificationType
    message: str
    refReportId: Optional[int]
    dateTime: datetime
    isRead: bool

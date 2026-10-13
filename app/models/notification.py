from datetime import UTC, datetime
from typing import Optional

from beanie import Document
from pydantic import Field

from app.schemas.notification_dto import NotificationType


class Notification(Document):
    userId: int
    type: NotificationType
    message: str
    refReportId: Optional[int] = None
    dateTime: datetime = Field(default_factory=lambda: datetime.now(UTC))
    isRead: bool = False

    class Settings:
        name = "notifications"
        indexes = ["userId", "type", "isRead"]

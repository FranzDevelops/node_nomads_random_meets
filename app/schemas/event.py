from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventsSchema(BaseModel):
    id: int
    created_at: datetime
    name: Optional[str]
    description: Optional[str]
    date: Optional[datetime]
    organizer: Optional[str]
    organizer_user_id: Optional[int]
    notification_minutes: Optional[int]
    call_url: Optional[str]
    call_id: Optional[str]
    is_active: bool
    timezone: str
    start_time: datetime
    end_time: datetime

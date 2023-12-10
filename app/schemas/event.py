from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventSchema(BaseModel):
    name: Optional[str]
    description: Optional[str]
    date: Optional[str]
    organizer: Optional[str]
    notification_minutes: Optional[int]
    call_url: Optional[str]
    call_id: Optional[str]
    is_active: bool
    timezone: str
    start_time: str
    end_time: str
    is_one_on_one: bool
    def __json__(self):
        return self.id

class UserToEvent(BaseModel):
    user_id: str
    event_id: int
    is_confirmed: bool
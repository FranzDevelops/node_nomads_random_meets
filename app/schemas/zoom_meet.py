import time
from typing import Optional, List
from pydantic import BaseModel

class Recurrence(BaseModel):
    end_date_time: str
    end_times: int
    monthly_day: int
    monthly_week: int
    monthly_week_day: int
    repeat_interval: int
    type: int
    weekly_days: str

class Settings(BaseModel):
    # Define your settings fields here
    pass

class TrackingField(BaseModel):
    field: str
    value: str
    visible: Optional[bool] = True

class ZoomMeetingInput(BaseModel):
    # Define your input fields here
    agenda: str
    default_password: bool
    duration: int
    password: str
    pre_schedule: bool
    recurrence: Recurrence
    schedule_for: str
    settings: Settings
    start_time: str
    template_id: str
    timezone: str
    topic: str
    tracking_fields: List[TrackingField]
    type: int

class ZoomMeetingOutput(BaseModel):
    # Define your output fields here
    assistant_id: str
    host_email: str
    id: int
    registration_url: str
    agenda: str
    created_at: str
    duration: int
    h323_password: str
    join_url: str
    chat_join_url: str
    occurrences: List[dict]
    password: str
    pmi: str
    pre_schedule: bool
    recurrence: Recurrence
    settings: Settings
    start_time: str
    start_url: str
    timezone: str
    topic: str
    tracking_fields: List[TrackingField]
    type: int
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class UserSchema(BaseModel):
    id: str
    created_at: datetime
    name: str
    lastname: str
    gender: str
    about_me: Optional[str]
    picture_url: str
    banner_url: str
    residence_type_id: int
    curr_latitude: float
    curr_longitude: float
    language_id: Optional[int]
    is_active: bool
    email: EmailStr
    city: str
    country_id: str
    birth_country_id: str
    onboarding_completed: bool
    timezone: str
    fcm_tokens: List[str]
    user_job: Optional[str]

class UserId(BaseModel):
    id: str
    def __json__(self):
        return self.id

class UserPair(BaseModel):
    user_one: str
    user_two: str
    def __json__(self):
        return self.id
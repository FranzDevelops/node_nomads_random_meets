from typing import List, Dict, Union
from pydantic import BaseModel

class MeetingInvitee(BaseModel):
    email: str

class MeetingChat(BaseModel):
    enable: bool
    auto_add_invited_external_users: bool

class ZoomMeetingSettings(BaseModel):
    additional_data_center_regions: List[str]
    allow_multiple_devices: bool
    approval_type: int
    audio: str
    audio_conference_info: str
    auto_recording: str
    calendar_type: int
    close_registration: bool
    contact_email: str
    contact_name: str
    email_notification: bool
    encryption_type: str
    focus_mode: bool
    global_dial_in_countries: List[str]
    host_video: bool
    jbh_time: int
    join_before_host: bool
    meeting_authentication: bool
    meeting_invitees: List[MeetingInvitee]
    mute_upon_entry: bool
    participant_video: bool
    private_meeting: bool
    registrants_confirmation_email: bool
    registrants_email_notification: bool
    show_share_button: bool
    use_pmi: bool
    waiting_room: bool
    watermark: bool
    host_save_video_order: bool
    alternative_host_update_polls: bool
    internal_meeting: bool
    continuous_meeting_chat: MeetingChat
    participant_focused_meeting: bool
    push_change_to_calendar: bool

class ZoomMeeting(BaseModel):
    agenda: str
    default_password: bool
    duration: int
    password: str
    pre_schedule: bool
    schedule_for: str
    settings: ZoomMeetingSettings
    start_time: str
    timezone: str
    topic: str
    type: int
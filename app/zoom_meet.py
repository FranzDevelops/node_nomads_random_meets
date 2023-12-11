import requests
import json
from app.utils.zoom_token import get_access_token
from app.schemas.zoom_meeting import ZoomMeeting
from app.schemas.user import UserPair

def create_zoom_meet(email_one: str, email_two: str, start_time: str, timezone: str):

    host_email = "frivas@singularagency.co"
    
    url = "https://api.zoom.us/v2/users/me/meetings"

    data_payload = {
        "agenda": "One on One Meeting",
        "default_password": False,
        "duration": 30,
        "password": "",
        "pre_schedule": False,
        "schedule_for": host_email,
        "settings": {
            "additional_data_center_regions": [
                "*"
            ],
            "allow_multiple_devices": True,
            "approval_type": 0,
            "audio": "both",
            "audio_conference_info": "One on one meet",
            "auto_recording": "none",
            "calendar_type": 2,
            "close_registration": False,
            "contact_email": host_email,
            "contact_name": "Node Nomads Support",
            "email_notification": False,
            "encryption_type": "enhanced_encryption",
            "focus_mode": True,
            "global_dial_in_countries": [
                "US"
            ],
            "host_video": False,
            "jbh_time": 15,
            "join_before_host": True,
            "meeting_authentication": False,
            "meeting_invitees": [
                {
                    "email": "invite@example.com"
                },
                {
                    "email": "invite@example.com"
                }
            ],
            "mute_upon_entry": False,
            "participant_video": True,
            "private_meeting": False,
            "registrants_confirmation_email": True,
            "registrants_email_notification": True,
            "show_share_button": True,
            "use_pmi": False,
            "waiting_room": False,
            "watermark": False,
            "host_save_video_order": False,
            "alternative_host_update_polls": True,
            "internal_meeting": False,
            "continuous_meeting_chat": {
                "enable": False,
                "auto_add_invited_external_users": True
            },
            "participant_focused_meeting": True,
            "push_change_to_calendar": False
        },
        "start_time": "2022-03-25T07:32:55Z",
        "timezone": "America/Los_Angeles",
        "topic": "One on one meeting",
        "type": 2
    }

    obj = ZoomMeeting(**data_payload)
    data = obj.model_dump_json()
    access_token = get_access_token()
    headers = {"authorization": f"Bearer {access_token}"}

    try:
        json_data = json.dumps(data_payload)
    except json.JSONDecodeError as e:
        print(f"Error converting data to JSON: {e}")
        return None

    # response = requests.post(
    #     url,
    #     json=data_payload,
    #     headers=headers
    # )

    # print("Response Content:", response.text)

    # response.raise_for_status()
    # result = response.json()
    
    return ("meet_url", "meet_id")


if __name__ == "__main__":
    try:
        create_zoom_meet()
    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")
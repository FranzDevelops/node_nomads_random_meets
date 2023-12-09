from schemas.zoom_meet import *

async def create_zoom_meeting(input_data: ZoomMeetingInput) -> ZoomMeetingOutput:
    # Simulate a 2-second delay
    time.sleep(2)

    # Mock data for the response
    mock_response = {
        "assistant_id": "kFFvsJc-Q1OSxaJQLvaa_A",
        "host_email": "jchill@example.com",
        "id": 92674392836,
        "registration_url": "https://example.com/meeting/register/7ksAkRCoEpt1Jm0wa-E6lICLur9e7Lde5oW6",
        "agenda": "My Meeting",
        "created_at": "2022-03-25T07:29:29Z",
        "duration": 60,
        "h323_password": "123456",
        "join_url": "https://example.com/j/11111",
        "chat_join_url": "https://example.com/launch/jc/11111",
        "occurrences": [
            {
                "duration": 60,
                "occurrence_id": "1648194360000",
                "start_time": "2022-03-25T07:46:00Z",
                "status": "available"
            }
        ],
        "password": "123456",
        "pmi": "97891943927",
        "pre_schedule": False,
        "recurrence": {
            "end_date_time": "2022-04-02T15:59:00Z",
            "end_times": 7,
            "monthly_day": 1,
            "monthly_week": 1,
            "monthly_week_day": 1,
            "repeat_interval": 1,
            "type": 1,
            "weekly_days": "1"
        },
        "settings": {
            "allow_multiple_devices": True,
            "alternative_hosts": "jchill@example.com;thill@example.com",
            "alternative_hosts_email_notification": True,
            "alternative_host_update_polls": True,
            "approval_type": 0,
            "approved_or_denied_countries_or_regions": {
                "approved_list": ["CX"],
                "denied_list": ["CA"],
                "enable": True,
                "method": "approve"
            },
            "audio": "telephony",
            "audio_conference_info": "test",
            "authentication_domains": "example.com",
            "authentication_exception": [
                {
                    "email": "jchill@example.com",
                    "name": "Jill Chill",
                    "join_url": "https://example.com/s/11111"
                }
            ],
            "authentication_name": "Sign in to Zoom",
            "authentication_option": "signIn_D8cJuqWVQ623CI4Q8yQK0Q",
            "auto_recording": "cloud",
            "breakout_room": {
                "enable": True,
                "rooms": [
                    {
                        "name": "room1",
                        "participants": ["jchill@example.com"]
                    }
                ]
            },
            "calendar_type": 1,
            "close_registration": False,
            "contact_email": "jchill@example.com",
            "contact_name": "Jill Chill",
            "custom_keys": [
                {
                    "key": "key1",
                    "value": "value1"
                }
            ],
            "email_notification": True,
            "encryption_type": "enhanced_encryption",
            "focus_mode": True,
            "global_dial_in_countries": ["US"],
            "global_dial_in_numbers": [
                {
                    "city": "New York",
                    "country": "US",
                    "country_name": "US",
                    "number": "+1 1000200200",
                    "type": "toll"
                }
            ],
            "host_video": True,
            "jbh_time": 0,
            "join_before_host": True,
            "language_interpretation": {
                "enable": True,
                "interpreters": [
                    {
                        "email": "interpreter@example.com",
                        "languages": "US,FR"
                    }
                ]
            },
            "sign_language_interpretation": {
                "enable": True,
                "interpreters": [
                    {
                        "email": "interpreter@example.com",
                        "sign_language": "American"
                    }
                ]
            },
            "meeting_authentication": True,
            "mute_upon_entry": False,
            "participant_video": False,
            "private_meeting": False,
            "registrants_confirmation_email": True,
            "registrants_email_notification": True,
            "registration_type": 1,
            "show_share_button": True,
            "use_pmi": False,
            "waiting_room": False,
            "watermark": False,
            "host_save_video_order": True,
            "internal_meeting": False,
            "continuous_meeting_chat": {
                "enable": True,
                "auto_add_invited_external_users": True
            },
            "participant_focused_meeting": False,
            "push_change_to_calendar": False,
            "resources": [
                {
                    "resource_type": "whiteboard",
                    "resource_id": "X4Hy02w3QUOdskKofgb9Jg",
                    "permission_level": "editor"
                }
            ]
        },
        "start_time": "2022-03-25T07:29:29Z",
        "start_url": "https://example.com/s/11111",
        "timezone": "America/Los_Angeles",
        "topic": "My Meeting",
        "tracking_fields": [
            {
                "field": "field1",
                "value": "value1",
                "visible": True
            }
        ],
        "type": 2
    }

    # Convert the mock response to a Pydantic object
    response = ZoomMeetingOutput(**mock_response)

    return response

# Example usage:
input_data = {
    # Define your input data here
}
input_model = ZoomMeetingInput(**input_data)
output_model = create_zoom_meeting(input_model)
print(output_model.json())
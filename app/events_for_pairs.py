from .pair_users import pair_users
from app.schemas.user import UserId, UserPair
from app.schemas.event import EventSchema, UserToEvent
from app.zoom_meet import create_zoom_meet
from datetime import datetime, timedelta
from config.supabase import supabase
from pydantic import Json
import pytz

def create_pairs_events():
    users_pairs = pair_users()

    for user_pair in users_pairs:
        set_event(user_pair)


def set_user_to_event(user_pair: UserPair, event_id: int):
    user_one_id = user_pair.user_one
    user_two_id = user_pair.user_two
    users_to_event = []

    user_one_event = {
        "user_id": user_one_id,
        "event_id": event_id,
        "is_confirmed": False
    }

    user_two_event = {
        "user_id": user_two_id,
        "event_id": event_id,
        "is_confirmed": False
    }

    schema_one = UserToEvent(**user_one_event)
    schema_two = UserToEvent(**user_two_event)

    obj_one = dict(schema_one)
    obj_two = dict(schema_two)

    users_to_event.append(obj_one)
    users_to_event.append(obj_two)

    supabase.table('user_events').upsert(users_to_event).execute()
    

def set_event(user_pair: UserPair) -> bool:
    user_one_id = user_pair.user_one
    user_two_id = user_pair.user_two
    user_one_name = get_user_data(user_one_id, "name")
    user_two_name = get_user_data(user_two_id, "name")
    user_one_email = get_user_data(user_one_id, "email")
    user_two_email = get_user_data(user_two_id, "email")
    one_timezone = get_user_data(user_one_id, "timezone")
    time_dict = generate_timestamp(one_timezone)
    start_time = time_dict["start_time"]
    end_time = time_dict["end_time"]
    date = time_dict["date"]

    meet_url, meet_id = create_zoom_meet(user_one_email, user_two_email, start_time, one_timezone)

    new_event = {
        "name": f'{user_one_name} and {user_two_name} meet',
        "description": f'One on One meet for {user_one_name} and {user_two_name}',
        "date": date,
        "organizer": "Node Nomads",
        "notification_minutes": 15,
        "call_url": meet_url,
        "call_id": meet_id,
        "is_active": True,
        "timezone": one_timezone,
        "start_time": start_time,
        "end_time": end_time,
        "is_one_on_one": True
    }

    schema = EventSchema(**new_event)
    obj = dict(schema)

    print(obj)

    data, count = supabase.table('events').insert(obj).execute()

    event_id = data[1][0]['id']

    set_user_to_event(user_pair, event_id) 

    return True

def get_user_data(user_id: str, data: str):
    res = supabase.table('users').select(data).eq('id', user_id).execute()
    obj = res.model_dump()
    result = obj["data"][0][data]
    return result

def generate_timestamp(timezone):
    # Get the current date and time in the specified timezone
    now = datetime.now(pytz.timezone(timezone))
    # Calculate the timestamp for the upcoming day on the 15th at 12:00 pm
    upcoming_day = now.replace(day=15, hour=12, minute=0, second=0, microsecond=0) + timedelta(days=1)
    # Calculate the end time by adding 30 minutes to the start time
    end_time = upcoming_day + timedelta(minutes=30)
    # Format the timestamp as a string
    timestamp_string = upcoming_day.strftime('%Y-%m-%d %H:%M:%S %Z')
    # Format the date as a string in "yyyy-mm-dd" format
    date_string = upcoming_day.strftime('%Y-%m-%d')
    # Format the end time as a string
    end_time_string = end_time.strftime('%Y-%m-%d %H:%M:%S %Z')
    # Return the three pieces of information
    return {
        "start_time": timestamp_string,
        "end_time": end_time_string,
        "date": date_string
    }
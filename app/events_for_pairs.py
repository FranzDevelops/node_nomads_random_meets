from pair_users import pair_users
from app.schemas.user import UserId, UserPair
from app.schemas.event import EventSchema, UserToEvent
from datetime import datetime, timedelta
from config.supabase import supabase
from pydantic import Json
import pytz

def create_pairs_events(meet_url: str):
    users_pairs = pair_users()
    print(users_pairs)


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

    print(users_to_event)
    response = supabase.table('user_events').upsert(users_to_event).execute()

    return response
    

def set_event(user_pair: UserPair, meet_url: str, meet_id: str) -> EventSchema:
    user_one_id = user_pair.user_one
    user_two_id = user_pair.user_two
    user_one_name = get_user_data(user_one_id, "name")
    user_two_name = get_user_data(user_two_id, "name")
    one_timezone = get_user_data(user_one_id, "timezone")
    time_dict = generate_timestamp(one_timezone)
    start_time = time_dict["start_time"]
    end_time = time_dict["end_time"]
    date = time_dict["date"]

    new_event = {
        "name": "One on One",
        "description": f'One on One meet for {user_one_name} and {user_two_name}',
        "date": datetime.strptime(date, '%Y-%m-%d'),
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
    obj = schema.model_dump_json()

    data, count = supabase.table('events').insert(obj).execute()
    
    # if count[1] == None:
    #     raise Exception("Insert operation failed")

    return obj

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

print(set_user_to_event(UserPair(user_one='81f31cfa-4a5c-4363-9cf3-4abeab83612a', user_two='770e565d-421b-4354-9d21-f4e4ce1af725'), 1))

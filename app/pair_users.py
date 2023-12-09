import sys
sys.path.append("/home/neo/Documents/Projects/nodenomads_random_meets_api")

import random
from config.supabase import supabase
from app.schemas.user import UserId, UserPair
from typing import List, Union
from pydantic import Json
from itertools import combinations

def get_available_users() -> List[UserId]:
    # Fetch all users from 'users' table
    res = supabase.table('users').select("id").execute()
    obj = res.model_dump()
    result = obj["data"]
    # Create a list of UserId instances
    user_ids = [UserId(id=user["id"]) for user in result]
    return user_ids

def get_paired_users() -> List[UserPair]:
    # Fetch all pairs from 'users_pair_meets' table
    res = supabase.table('users_pair_meets').select("user_one", "user_two").execute()
    obj = res.model_dump()
    result = obj["data"]
    # Create a list of UserPair instances
    user_pairs = [UserPair(user_one=pair["user_one"], user_two=pair["user_two"]) for pair in result]
    return user_pairs

def get_unpaired_users(available_users: List[UserId], paired_users: List[UserPair]) -> List[UserPair]:
    new_pairs = []

    # Generate all possible combinations of pairs
    user_combinations = list(combinations(available_users, 2))

    # Keep track of users already paired
    paired_user_ids = set(pair.user_one for pair in paired_users) | set(pair.user_two for pair in paired_users)

    for user_id_1, user_id_2 in user_combinations:
        # Check if either user is already paired
        if user_id_1.id in paired_user_ids or user_id_2.id in paired_user_ids:
            continue

        # Create a new pair
        new_pairs.append(UserPair(user_one=user_id_1.id, user_two=user_id_2.id))
        paired_user_ids.add(user_id_1.id)
        paired_user_ids.add(user_id_2.id)

    # If the total number of users is odd, one user will have two new pairs
    if len(available_users) % 2 == 1:
        user_with_two_pairs = available_users[-1]  # Pick the last user in the list
        if user_with_two_pairs.id not in paired_user_ids:
            new_pairs.append(UserPair(user_one=user_with_two_pairs.id, user_two=available_users[0].id))

    return new_pairs

def delete_all_pair_meets():
    # Delete all records from 'users_pair_meets' table
    supabase.table('users_pair_meets').delete().execute()

def create_new_pair_meets(pairs: List[UserPair]):
    # Convert UserPair instances and tuples to dictionaries
    records = [dict(pair) for pair in pairs]

    print(records)
    supabase.table('users_pair_meets').upsert(records).execute()

def pair_users():
    available_users = get_available_users()
    paired_users = get_paired_users()

    unpaired_users = get_unpaired_users(available_users, paired_users)

    if not unpaired_users:
        # All users are already paired, delete all pairs and try again
        delete_all_pair_meets()
        pair_users()
    else:
        # Create new pairs and insert into 'users_pair_meets' table
        # diff = 0 if len(unpaired_users) % 2 == 0 else 1
        # new_pairs = [(unpaired_users[i], unpaired_users[i + 1]) for i in range(0, len(unpaired_users) - diff, 2)]
        create_new_pair_meets(unpaired_users)

pair_users()
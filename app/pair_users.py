import sys
import random
import math
from random import shuffle, sample
from config.supabase import supabase
from app.schemas.user import UserId, UserPair
from typing import List, Union
from pydantic import Json
from itertools import combinations
import aiohttp
import asyncio

async def get_available_users() -> List[UserId]:
    # Fetch all users from 'users' table
    res = await supabase.table('users').select("id").execute()
    obj = res.model_dump()
    result = obj["data"]
    # Create a list of UserId instances
    user_ids = [UserId(id=user["id"]) for user in result]
    return user_ids

async def get_paired_users() -> List[UserPair]:
    # Fetch all pairs from 'users_pair_meets' table
    res = await supabase.table('users_pair_meets').select("user_one", "user_two").execute()
    obj = res.model_dump()
    result = obj["data"]
    # Create a list of UserPair instances
    user_pairs = [UserPair(user_one=pair["user_one"], user_two=pair["user_two"]) for pair in result]
    return user_pairs

async def get_unpaired_users_deprecated(available_users: List[UserId], paired_users: List[UserPair]) -> List[UserPair]:
    new_pairs = []

    # Generate all possible combinations of pairs
    user_combinations = list(combinations(available_users, 2))

    # Create pairs without checking for existence
    all_pairs = [
        UserPair(user_one=user_id_1.id, user_two=user_id_2.id)
        for user_id_1, user_id_2 in user_combinations
    ]

    # Filter out existing pairs
    existing_pairs = set((pair.user_one, pair.user_two) for pair in paired_users)
    new_pairs = [pair for pair in all_pairs if (pair.user_one, pair.user_two) not in existing_pairs]

    # Determine the number of pairs to generate
    num_pairs_to_generate = (len(available_users) + 1) // 2

    # Randomly sample the desired number of new pairs
    selected_pairs = sample(new_pairs, num_pairs_to_generate)

    # Keep track of paired users in this function call
    paired_users_set = set()
    result_pairs = []

    # Ensure each user is paired only once in this function call
    for pair in selected_pairs:
        if pair.user_one not in paired_users_set:
            result_pairs.append(pair)
            paired_users_set.add(pair.user_one)

        if pair.user_two not in paired_users_set:
            result_pairs.append(pair)
            paired_users_set.add(pair.user_two)

    # If the total number of users is odd, one user will have two new pairs
    if len(available_users) % 2 == 1:
        user_with_two_pairs = available_users[-1]  # Pick the last user in the list
        remaining_users = [user for user in available_users if user != user_with_two_pairs]
        user_for_second_pair = sample(remaining_users, 1)[0]
        additional_pair = UserPair(user_one=user_with_two_pairs.id, user_two=user_for_second_pair.id)
        result_pairs.append(additional_pair)

    return result_pairs

async def get_unpaired_users(available_users: List[UserId], paired_users: List[UserPair]) -> List[UserPair]:
    # Check if the total number of users is odd
    is_odd_total_users = len(available_users) % 2 == 1

    # Shuffle the list of available users to ensure randomness
    shuffled_users = sample(available_users, len(available_users))

    # Initialize lists to track paired users and generated pairs
    paired_users_set = set()
    generated_pairs = []

    # Generate pairs without checking for existence
    for i in range(0, len(shuffled_users), 2):
        user_id_1 = shuffled_users[i]
        user_id_2 = shuffled_users[i + 1] if i + 1 < len(shuffled_users) else None

        pair = UserPair(user_one=user_id_1.id, user_two=user_id_2.id if user_id_2 else None)

        generated_pairs.append(pair)

        paired_users_set.add(user_id_1.id)
        if user_id_2:
            paired_users_set.add(user_id_2.id)

    # If the total number of users is odd, one user will have two new pairs
    if is_odd_total_users:
        user_with_two_pairs = shuffled_users[-1]  # Pick the last user in the shuffled list
        remaining_users = [user for user in shuffled_users if user != user_with_two_pairs]

        # Ensure the second pair is with a different user
        user_for_second_pair = sample([user for user in remaining_users if user != user_with_two_pairs], 1)[0]

        additional_pair = UserPair(user_one=user_with_two_pairs.id, user_two=user_for_second_pair.id)
        generated_pairs.append(additional_pair)

        paired_users_set.add(user_with_two_pairs.id)
        paired_users_set.add(user_for_second_pair.id)

    return generated_pairs


async def delete_all_pair_meets():
    # Delete all records from 'users_pair_meets' table
    await supabase.table('users_pair_meets').delete().execute()

async def create_new_pair_meets(pairs: List[UserPair]):
    # Convert UserPair instances and tuples to dictionaries
    records = [dict(pair) for pair in pairs]

    await supabase.table('users_pair_meets').upsert(records).execute()

async def pair_users() -> List[UserPair]:
    available_users = await get_available_users()
    paired_users = await get_paired_users()

    unpaired_users = await get_unpaired_users(available_users, paired_users)

    if not unpaired_users:
        # All users are already paired, delete all pairs and try again
        await delete_all_pair_meets()
        await pair_users()
    else:
        # Create new pairs and insert into 'users_pair_meets' table
        await create_new_pair_meets(unpaired_users)
        return unpaired_users

async def main():
    await pair_users()

if __name__ == "__main__":
    asyncio.run(main())

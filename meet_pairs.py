import random

class User:
    def __init__(self, name):
        self.name = name

def print_user_pairs(users):
    # Shuffle the list of users
    random.shuffle(users)

    # Pair the users using zip and print in a more functional way
    pairs = list(zip(users[::2], users[1::2]))
    pairs_str = [f"{user1.name} and {user2.name}" for user1, user2 in pairs]

    # If there is an odd number of users, add the name of the last user
    if len(users) % 2 != 0:
        pairs_str.append(f"Only {users[-1].name}")

    # Print the pairs
    print("\n".join(pairs_str))

# Example Usage:

# Creating a list of User objects
users = [User("Alice"), User("Bob"), User("Charlie"), User("David")]

# Calling the function
print_user_pairs(users)

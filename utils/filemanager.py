import json
import os
import typing

from utils import usermanager


def check_path():
    """
    Function checks existing important files and directories and create them
    :return: None
    """
    if not os.path.exists("users"):
        os.makedirs("users")
        print("\"users\" directory created...")
    if not os.path.exists("logs"):
        os.makedirs("logs")
        print("\"logs\" directory created...")

    # configurating tokens
    if not os.path.exists("config.json"):
        print("You must have config.json file with your tokens...")
        with open('config.json', 'w') as file:
            file.write("{\n\t\"group_id\": YOUR_GROUP_ID,\n\t\"vk_token\": \"YOUR_VK_BOT_TOKEN\"\n}")
            file.close()
        print("Token file created. Please past your tokens. Program will shutdown...")
        exit(1)


def get_config() -> dict:
    """
    Loads configuration file.
    :return: Dictionary object
    """
    with open('config.json', 'r') as file:
        config = json.loads(file.read())
        file.close()
        return config


def get_user(user_id: int) -> usermanager.User:
    """
    Function reads user profile from file
    :param user_id: id пользователя
    :return: User object
    """
    if f"{user_id}.user" in os.listdir("users"):
        file = open(f"users/{user_id}.user", "r")
        user = usermanager.get_user_from_json(file.read())
        file.close()
        return user
    else:
        print(f"File {user_id}.user not found!")


def get_users() -> typing.List[usermanager.User]:
    users: typing.List[usermanager.User] = []
    for file in os.listdir('users'):
        args = file.split('.')
        user = get_user(int(''.join(args[:len(args) - 1])))
        users.append(user)
    return users


def update_user(user: usermanager.User):
    """
    Function writes user profile in file
    :param user: User object
    :return: None
    """
    with open(f"users/{user.user_id}.user", "w") as file:
        file.write(user.get_json())
        file.close()


def user_exists(user_id: int) -> bool:
    """
    Function checks user profile in files
    :param user_id: user id
    :return: bool
    """
    return f"{user_id}.user" in os.listdir("users")

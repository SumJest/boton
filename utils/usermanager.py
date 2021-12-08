import json


class User(object):
    user_id: int
    action_state: int
    is_blocked: bool
    group: str

    def __init__(self, user_id: int, action_state: int = 0, group: str = "", is_blocked: bool = False):
        self.user_id = user_id
        self.action_state = action_state
        self.group = group
        self.is_blocked = is_blocked

    def __repr__(self):
        return f"user_id: {self.user_id}, action_state: {self.action_state}, group: {self.group},  " \
               f"is_blocked: {self.is_blocked} "

    def get_json(self):
        return json.dumps(self.__dict__)


def get_user_from_json(json_user: str) -> User:
    """
    Function creates User object from json string
    :param json_user:
    :return: User object
    """
    attr: dict = json.loads(json_user)
    user = User(0)
    for key in attr.keys():
        setattr(user, key, attr[key])
    return user

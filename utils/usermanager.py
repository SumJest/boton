import json
import typing


class User(object):
    user_id: int
    action_state: int
    is_blocked: bool
    groups: typing.List[str]
    subs: typing.List[str]

    def __init__(self, user_id: int, action_state: int = 0, groups: typing.List[str] = [], subs: typing.List[str] = [],
                 is_blocked: bool = False):
        self.user_id = user_id
        self.action_state = action_state
        self.groups = groups
        self.subs = subs
        self.is_blocked = is_blocked

    def __repr__(self):
        return f"user_id: {self.user_id}, action_state: {self.action_state}, groups: {'/'.join(self.groups)},  " \
               f"is_blocked: {self.is_blocked} "

    def get_json(self) -> str:
        """
        Function returns json object of user
        :return: str json
        """
        return json.dumps(self.__dict__)


class ActionStates:
    IDLE = 0
    ENTERING_HASHTAG = 1
    DELETING_HASHTAG = 2
    ASKING = 3


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

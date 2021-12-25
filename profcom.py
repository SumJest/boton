import json
import random
from datetime import datetime

from vkwave.bots import SimpleLongPollBot, SimpleBotEvent

from utils import filemanager as fm, my_filters
from utils import keyboardmanager
from utils import usermanager as um
from utils.messages import Messages

fm.check_path()

config = fm.get_config()

bot = SimpleLongPollBot(tokens=config["vk_token"], group_id=config["group_id"])
api = bot.api_context

km = keyboardmanager.KeyboardManager()

print("Bot successful started")


# ------------

def get_random_id():
    return random.getrandbits(32)


async def log(event: SimpleBotEvent):
    now = datetime.today()
    line = f"[{now.strftime('%d.%m.%Y-%H:%M:%S')}] [{event.object.type}] ({event.object.object.message.from_id}): " \
           f"{event.object.object.message.text}"
    print(line)
    with open(f"logs/log{now.strftime('%d-%m-%Y')}.txt", "a", encoding='utf-8') as file:
        file.write(line + "\n")
        file.close()


async def new_user(user_id: int) -> None:
    """
    Function registers a new user and sends a start's message.
    :param user_id: Id of user
    :return: None
    """
    user = um.User(user_id)
    fm.update_user(user)
    name = (await api.users.get(user_ids=user_id)).response[0].first_name
    await api.messages.send(user_id=user_id, message=Messages.hello_message.format(name=name),
                            random_id=get_random_id(), keyboard=km.keyboards['main'])


async def take_action(user_id: int, button_id: int) -> None:
    """
    Function do action, that button with button_id means.
    :param user_id: Id of user
    :param button_id: Id of button
    :return: None
    """
    if button_id == 0:
        if fm.user_exists(user_id):
            user = fm.get_user(user_id)
            user.action_state = um.ActionStates.IDLE
            fm.update_user(user)
        await api.messages.send(user_id=user_id, message=Messages.cancel, keyboard=km.keyboards['main'],
                                random_id=get_random_id())
    elif button_id == 1:
        user = fm.get_user(user_id)
        if len(user.subs) != 0:
            answer = ""
            for i in range(1, len(user.subs) + 1):
                answer += f"{i}. #{user.subs[i - 1]} \n"
            await api.messages.send(user_id=user_id, message=answer, random_id=get_random_id())
    elif button_id == 2:
        user = fm.get_user(user_id)
        user.action_state = um.ActionStates.ENTERING_HASHTAG
        fm.update_user(user)
        await api.messages.send(user_id=user_id, message=Messages.enter_hashtag,
                                random_id=get_random_id())
    elif button_id == 3:
        user = fm.get_user(user_id)
        user.action_state = um.ActionStates.DELETING_HASHTAG
        fm.update_user(user)
        await api.messages.send(user_id=user_id, message=Messages.enter_n_hashtag,
                                random_id=get_random_id())
    elif button_id == 4:
        user = fm.get_user(user_id)
        user.action_state = um.ActionStates.ASKING
        fm.update_user(user)
        await api.messages.send(user_id=user_id, message=Messages.enter_question,
                                keyboard=km.keyboards['cancel'], random_id=get_random_id())


@bot.message_handler(my_filters.HasPayloadFilter())
async def button_event(event: SimpleBotEvent):
    await log(event)
    payload: dict = json.loads(event.object.object.message.payload)
    # Start message
    if 'command' in payload.keys():
        if payload['command'] == "start":
            user_id = event.object.object.message.from_id
            if not fm.user_exists(user_id):
                await new_user(user_id)
    # If button implies any action
    if 'btn_id' in payload.keys():
        button_id = int(payload['btn_id'])
        user_id = event.object.object.message.from_id
        await take_action(user_id, button_id)
    # If need to open an another keyboard
    if 'open_id' in payload.keys():
        open_id = payload['open_id']
        await event.answer(message="Окей", keyboard=km.keyboards[open_id])
    # If need send a text
    if 'txt_id' in payload.keys() and 'kb_id' in payload.keys():
        txt_id = int(payload['txt_id'])
        kb_id = payload['kb_id']
        await event.answer(Messages.gettext(kb_id, txt_id))


@bot.message_handler()
async def text_message(event: SimpleBotEvent):
    await log(event)
    user_id = event.object.object.message.from_id
    if not fm.user_exists(user_id):
        await new_user(user_id)
    else:
        user = fm.get_user(user_id)
        if user.action_state == um.ActionStates.IDLE:
            conversation = (await api.messages.get_conversations_by_id(peer_ids=user_id)).response.items[0].important
            if not conversation:
                await api.messages.send(user_id=user_id, message=random.choice(Messages.want_to_ask),
                                        random_id=get_random_id())
        elif user.action_state == um.ActionStates.ENTERING_HASHTAG:
            hash_tag = event.object.object.message.text.lower()
            hash_tag = hash_tag.lstrip('#')
            if hash_tag not in user.subs:
                user.subs.append(hash_tag)
            user.action_state = um.ActionStates.IDLE
            fm.update_user(user)
            await event.answer(Messages.done, keyboard=km.keyboards['main'])
            return
        elif user.action_state == um.ActionStates.DELETING_HASHTAG:
            message = event.object.object.message.text
            if not str.isdigit(message):
                return Messages.enter_number
            hash_tag_id = int(message)
            if 1 <= hash_tag_id <= len(user.subs):
                user.subs.pop(hash_tag_id - 1)
                user.action_state = um.ActionStates.IDLE
                fm.update_user(user)
                await event.answer(Messages.done, keyboard=km.keyboards['main'])
                return
            else:
                return Messages.no_hashtag
        elif user.action_state == um.ActionStates.ASKING:
            message = event.object.object.message.text
            if not message:
                return Messages.err_question
            await api.messages.mark_as_important_conversation(peer_id=user.user_id, important=1)
            user.action_state = um.ActionStates.IDLE
            fm.update_user(user)
            await event.answer(Messages.set_question,
                               keyboard=km.keyboards['main'])


# @bot.handler(my_filters.JoinFilter())
# async def join_event(event: SimpleBotEvent):
#     print(f"Новый участник группы [{event.object.object.user_id}]!")
#
#
# @bot.handler(my_filters.LeaveFilter())
# async def leave_event(event: SimpleBotEvent):
#     print(f"Участник [{event.object.object.user_id}] покинул группу!")


@bot.handler(my_filters.NewPostFilter())
async def post_event(event: SimpleBotEvent):
    for user in fm.get_users():
        for hash_tag in user.subs:
            if f"#{hash_tag}" in event.object.object.text.lower():
                await api.messages.send(user_id=user.user_id, random_id=get_random_id(), message=Messages.new_post,
                                        attachment=f"wall{event.object.object.owner_id}_{event.object.object.id}")
                break


# @bot.handler()
# async def any_event(event: SimpleBotEvent):
#    if event.object.type == "message_reply" and event.object.object.admin_author_id is not None:
#        print(event.object.object)
# message = event.object.object
# resp = (await api.users.get(user_ids=message.admin_author_id)).response[0]
# await api.messages.edit(peer_id=message.peer_id,
#                         conversation_message_id=message.conversation_message_id,
#                         message=f"{message.text} \nОтветил(а): {resp.first_name} {resp.last_name[0]}.")


if __name__ == "__main__":
    bot.run_forever()

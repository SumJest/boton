import json
import random
from datetime import datetime

from vkwave.api import API
from vkwave.client import AIOHTTPClient
from vkwave.bots import SimpleLongPollBot, SimpleBotEvent
from vkwave.bots.core.dispatching import filters

from utils import filemanager as fm, my_filters, messages
from utils import keyboardmanager
from utils.messages import Messages
from utils import usermanager as um

fm.check_path()

config = fm.get_config()

bot = SimpleLongPollBot(tokens=config["vk_token"], group_id=config["group_id"])

api_session = API(tokens=config['vk_token'], clients=AIOHTTPClient())
api = api_session.get_context()

km = keyboardmanager.KeyboardManager()

print("Bot successful started")


# ------------

def get_random_id():
    return random.getrandbits(32)

def is_int(n: str) -> bool:
    try:
        int(n)
        return True
    except ValueError:
        return False

async def log(event: SimpleBotEvent):
    now = datetime.today()
    line = f"[{now.strftime('%d.%m.%Y-%H:%M:%S')}] [{event.object.type}] ({event.object.object.message.from_id}): " \
           f"{event.object.object.message.text}"
    print(line)
    with open(f"logs/log{now.strftime('%d-%m-%Y')}.txt", "a", encoding='utf-8') as file:
        file.write(line + "\n")
        file.close()


@bot.message_handler(filters.TextFilter(["начать", "start"]))
async def start_message(event: SimpleBotEvent):
    await log(event)
    user_id = event.object.object.message.from_id
    if not fm.user_exists(user_id):
        user = um.User(user_id)
        fm.update_user(user)
        name = (await api.users.get(user_ids=user_id)).response[0].first_name
        await event.answer(message=Messages.hello_message.format(name=name), keyboard=km.keyboards['main'])


@bot.message_handler(my_filters.HasPayloadFilter())
async def button_event(event: SimpleBotEvent):
    await log(event)
    payload: dict = json.loads(event.object.object.message.payload)
    if 'btn_id' in payload.keys():
        button_id = int(payload['btn_id'])
        if button_id == 0:
            user_id = event.object.object.message.from_id
            if fm.user_exists(user_id):
                user = fm.get_user(user_id)
                user.action_state = um.ActionStates.IDLE
                fm.update_user(user)
            await event.answer(message="Возвращаюсь...", keyboard=km.keyboards['main'])
        elif button_id == 1:
            user_id = event.object.object.message.from_id
            user = fm.get_user(user_id)

            if len(user.subs) != 0:
                answer = ""
                for i in range(1, len(user.subs) + 1):
                    answer += f"{i}. #{user.subs[i-1]}"
                await event.answer(message=answer)
        elif button_id == 2:
            await event.answer("Введите хэштэг, на который хотите подписаться (#пример): ")
            user_id = event.object.object.message.from_id
            user = fm.get_user(user_id)
            user.action_state = um.ActionStates.ENTERING_HASHTAG
            fm.update_user(user)
        elif button_id == 3:
            await event.answer("Введите номер хэштэга, который хотите удалить из подписок: ")
            user_id = event.object.object.message.from_id
            user = fm.get_user(user_id)
            user.action_state = um.ActionStates.DELETING_HASHTAG
            fm.update_user(user)
    if 'open_id' in payload.keys():
        open_id = payload['open_id']
        await event.answer(message="Выберете интересующую вас тему.", keyboard=km.keyboards[open_id])
    if 'txt_id' in payload.keys() and 'kb_id' in payload.keys():
        txt_id = int(payload['txt_id'])
        kb_id = payload['kb_id']
        await event.answer(Messages.gettext(kb_id, txt_id))


@bot.message_handler()
async def text_message(event: SimpleBotEvent):
    await log(event)
    user_id = event.object.object.message.from_id
    if not fm.user_exists(user_id):
        user = um.User(user_id)
        fm.update_user(user)
        name = (await api.users.get(user_ids=user_id)).response[0].first_name
        await event.answer(message=Messages.hello_message.format(name=name), keyboard=km.keyboards['main'])
    else:
        user = fm.get_user(user_id)
        if user.action_state == um.ActionStates.ENTERING_HASHTAG:
            hash_tag = event.object.object.message.text.lower()
            if hash_tag.startswith('#'):
                hash_tag = hash_tag.lstrip('#')
            if not hash_tag in user.subs:
                user.subs.append(hash_tag)
            user.action_state = um.ActionStates.IDLE
            fm.update_user(user)
            await event.answer("Готово", keyboard=km.keyboards['main'])
            return
        elif user.action_state == um.ActionStates.DELETING_HASHTAG:
            message = event.object.object.message.text
            if not is_int(message):
                return "Введите число!"
            id = int(message)
            if 1 <= id <= len(user.subs):
                user.subs.pop(id-1)
                user.action_state = um.ActionStates.IDLE
                fm.update_user(user)
                await event.answer("Готово", keyboard=km.keyboards['main'])
                return
            else:
                return "Хэштэг с таким номером не найден в подписках!"

    return "Ваш вопрос зарегистрирован, пожалуйста подождите и вам ответит специалист!"


@bot.handler(my_filters.JoinFilter())
async def join_event(event: SimpleBotEvent):
    print(f"Новый участник группы [{event.object.object.user_id}]!")


@bot.handler(my_filters.LeaveFilter())
async def leave_event(event: SimpleBotEvent):
    print(f"Участник [{event.object.object.user_id}] покинул группу!")


@bot.handler(my_filters.NewPostFilter())
async def post_event(event: SimpleBotEvent):
    for user in fm.get_users():
        for hash_tag in user.subs:
            if f"#{hash_tag}" in event.object.object.text.lower():
                print(hash_tag)
                await api.messages.send(user_id=user.user_id, random_id=get_random_id(), message="Новый пост",
                                        attachment=f"wall{event.object.object.owner_id}_{event.object.object.id}")


if __name__ == "__main__":
    bot.run_forever()

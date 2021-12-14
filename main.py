import json
import random
from datetime import datetime

from vkwave.api import API
from vkwave.client import AIOHTTPClient
from vkwave.bots import SimpleLongPollBot, SimpleBotEvent
from vkwave.bots.core.dispatching import filters

from utils import filemanager as fm, my_filters, messages
from utils import keyboardmanager as km
from utils.messages import Messages
from utils import usermanager as um

fm.check_path()

config = fm.get_config()

bot = SimpleLongPollBot(tokens=config["vk_token"], group_id=config["group_id"])

api_session = API(tokens=config['vk_token'], clients=AIOHTTPClient())
api = api_session.get_context()

print("Bot successful started")


# ------------

def get_random_id():
    return random.getrandbits(32)


async def log(event: SimpleBotEvent):
    now = datetime.today()
    line = f"[{now.strftime('%d.%m.%Y-%H:%M:%S')}] [{event.object.type}] ({event.object.object.message.from_id}): " \
           f"{event.object.object.message.text}"
    print(line)
    with open(f"logs/log{now.strftime('%d-%m-%Y')}.txt", "a") as file:
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
        await event.answer(message=Messages.hello_message.format(name=name), keyboard=km.main_keyboard.get_keyboard())


@bot.message_handler(my_filters.HasPayloadFilter())
async def button_event(event: SimpleBotEvent):
    await log(event)
    payload: dict = json.loads(event.object.object.message.payload)
    if 'btn_id' in payload.keys():
        button_id = int(payload['btn_id'])
        if button_id == 0:
            await event.answer(message="Возвращаюсь...", keyboard=km.main_keyboard.get_keyboard())
        if button_id == 1:
            await event.answer(message="Выберете интересующую вас тему.", keyboard=km.mat_help_keyboard.get_keyboard())
        if button_id == 2:
            await event.answer(message="Выберете интересующую вас тему.",
                               keyboard=km.social_payment_keyboard.get_keyboard())
        if button_id == 3:
            await event.answer(message="Выберете интересующую вас тему.",
                               keyboard=km.ref_income_keyboard.get_keyboard())
        if button_id == 4:
            await event.answer(message="Выберете интересующую вас тему.", keyboard=km.voucher_keyboard.get_keyboard())
        if button_id == 5:
            return Messages.join_prof_message
        if 6 <= button_id <= 16:
            return messages.get_mat_help_message(button_id - 6)
        if 17 <= button_id <= 18:
            return messages.get_soc_pay_message(button_id - 17)
        if button_id == 19:
            return messages.get_ref_income_message(button_id - 19)
        if 20 <= button_id <= 21:
            return messages.get_voucher_message(button_id - 20)


@bot.message_handler()
async def text_message(event: SimpleBotEvent):
    await log(event)
    user_id = event.object.object.message.from_id
    if not fm.user_exists(user_id):
        user = um.User(user_id)
        fm.update_user(user)
        name = (await api.users.get(user_ids=user_id)).response[0].first_name
        await event.answer(message=Messages.hello_message.format(name=name), keyboard=km.main_keyboard.get_keyboard())
    return "Ваш вопрос зарегистрирован, пожалуйста подождите и вам ответит специалист!"


@bot.handler(my_filters.JoinFilter())
async def join_event(event: SimpleBotEvent):
    print(f"Новый участник группы [{event.object.object.user_id}]!")


@bot.handler(my_filters.LeaveFilter())
async def leave_event(event: SimpleBotEvent):
    print(f"Участник [{event.object.object.user_id}] покинул группу!")


@bot.handler(my_filters.NewPostFilter())
async def post_event(event: SimpleBotEvent):
    await api.messages.send(user_id=144268714, random_id=get_random_id(),
                            attachment=f"wall{event.object.object.owner_id}_{event.object.object.id}")
    print(f"Новый пост!")


if __name__ == "__main__":
    bot.run_forever()

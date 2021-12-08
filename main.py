from datetime import datetime

from vkwave.api import API
from vkwave.client import AIOHTTPClient
from vkwave.bots import SimpleLongPollBot, SimpleBotEvent
from vkwave.bots.core.dispatching import filters

from utils import filemanager as fm
from utils.messages import Messages
from utils import usermanager as um

fm.check_path()

config = fm.get_config()

bot = SimpleLongPollBot(tokens=config["vk_token"], group_id=config["group_id"])

api_session = API(tokens=config['vk_token'], clients=AIOHTTPClient())
api = api_session.get_context()

print("Bot successful started")


# ------------

async def log(event: SimpleBotEvent):
    now = datetime.today()
    line = f"[{now.strftime('%d.%m.%Y-%H:%M:%S')}] ({event.object.object.message.from_id}): " \
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
        return Messages.hello_message.format(name=name)


@bot.message_handler()
async def text_message(event: SimpleBotEvent):
    await log(event)
    return event.object.object.message.text


if __name__ == "__main__":
    bot.run_forever()

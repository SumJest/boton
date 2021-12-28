import os
from vkwave.bots import Keyboard, ButtonColor


class KeyboardManager:
    keyboards: dict = {}

    def __init__(self):
        self.reload()

    def reload(self):
        """
        Function updates keyboards from directory
        :return: None
        """
        for file in os.listdir('keyboards'):
            with open(f"keyboards/{file}", 'r', encoding='utf-8') as f:
                name = file.split('.')
                self.keyboards[''.join(name[:len(name) - 1])] = f.read()
                f.close()

    @staticmethod
    def gen_end_dialog_keyboard(message_id: int) -> str:
        """
        Function generates an end dialog keyboard.
        :param message_id: Id of message that attached keyboard
        :return: Json keyboard
        """
        end_dialog_keyboard = Keyboard(inline=True)
        end_dialog_keyboard.add_callback_button(text="Да", color=ButtonColor.POSITIVE,
                                                payload={"btn_id": "5", "msg_id": str(message_id)})
        end_dialog_keyboard.add_callback_button(text="Нет", color=ButtonColor.NEGATIVE,
                                                payload={"btn_id": "6", "msg_id": str(message_id)})
        return end_dialog_keyboard.get_keyboard()

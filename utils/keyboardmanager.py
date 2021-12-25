import os


# def deserialize_json(keyboard: str) -> Keyboard:
#     kb_json = json.loads(keyboard)
#     return Keyboard(one_time=False, inline=False, buttons=kb_json['buttons'])


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

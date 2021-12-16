import json

from vkwave.bots import Keyboard

c_keyboard: Keyboard
c_name: str = ''

def load_json(json_keyboard: str) -> Keyboard:
    d_keyboard = json.loads(json_keyboard)
    keyboard = Keyboard(inline=False, one_time=False)
    count = len(d_keyboard['buttons'])
    for i in range(count):
        for button2 in d_keyboard['buttons'][i]:
            keyboard.add_text_button(button2['action']['label'], button2['color'], button2['action']['payload'])
        if i != count - 1:
            keyboard.add_row()
    return keyboard


while True:
    inp = input().split(' ')
    cmd = inp[0]
    args = inp[1:]
    if cmd == 'open':
        c_name = args[1]
        with open(f'keyboards/{c_name}.json', 'r', encoding='utf-8') as f:
            c_keyboard = load_json(f.read())
            f.close()
        print(f"Keyboard {c_name} opened")
    # elif add

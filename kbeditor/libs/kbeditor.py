import json
import os
import typing

from vkwave.bots import Keyboard

c_keyboard: Keyboard = Keyboard()
c_name: str = ''
texts: typing.List = []


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


def save(keyboard: Keyboard, name: str):
    with open(f'keyboards/{name}.json', 'w', encoding='utf-8') as file:
        f.write(keyboard.get_keyboard())
        f.close()
    if name not in os.listdir('../../texts'):
        os.mkdir(f'texts/{name}')


while True:
    inp = input().split(' ')
    cmd = inp[0]
    args = inp[1:]
    if cmd == 'open':
        c_name = args[0]
        with open(f'keyboards/{c_name}.json', 'r', encoding='utf-8') as f:
            c_keyboard = load_json(f.read())
            f.close()
        print(f"Keyboard {c_name} opened")
    elif cmd == "create":
        c_name = args[0]
        c_keyboard = Keyboard()
        print(f"Keyboard {c_name} opened")
    elif cmd == "list":
        print("Keyboards: ")
        for file in os.listdir('../../keyboards/'):
            name = file.split('.')
            print(''.join(name[:len(name) - 1]))
    elif cmd == "save":
        if c_keyboard is not None and c_name is not None:
            save(c_keyboard, c_name)
            print(f"Keyboard {c_name} saved")
    elif cmd == "show":
        if c_keyboard is not None and c_name is not None:
            j_keyboard = json.loads(c_keyboard.get_keyboard())
            i = 0
            for button in j_keyboard['buttons']:
                output = ""
                for button1 in button:
                    output += f"{i}. '{button1['action']['label']}' - {button1['color']}: {button1['action']['payload']}, "
                i += 1
                print(output)
    elif cmd == 'add':
        n = int(args[0])
        j_keyboard = json.loads(c_keyboard.get_keyboard())
        if n >= len(j_keyboard['buttons']):
            j_keyboard['buttons'].append(json.loads(" ".join(args[1:])))
        else:
            j_keyboard['buttons'][n].append(json.loads(" ".join(args[1:])))


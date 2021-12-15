import json

from vkwave.bots import Keyboard


def load_json(json_keyboard: str) -> Keyboard:
    d_keyboard = json.loads(json_keyboard)
    keyboard = Keyboard(inline=False, one_time=False)
    count = len(d_keyboard['buttons'])
    for i in range(count):
        for button2 in d_keyboard['buttons'][i]:
            keyboard.add_text_button(button2['action']['label'], button2['color'], button2['action']['payload'])
        if i != count-1:
            keyboard.add_row()
    return keyboard



with open('keyboards/main.json', 'w', encoding='utf-8') as f:
    keyboard = Keyboard()
    keyboard.add_text_button("Добавить", '')
    f.write(keyboard.get_keyboard())
    f.close()
from vkwave.bots import Keyboard, ButtonColor

# Главное меню
main_keyboard = Keyboard(one_time=False, inline=False)
main_keyboard.add_text_button("Материальная помощь", color=ButtonColor.POSITIVE, payload={'btn_id': '1'})
main_keyboard.add_row()
main_keyboard.add_text_button("Социальная стипендия", color=ButtonColor.POSITIVE, payload={'btn_id': '2'})
main_keyboard.add_row()
main_keyboard.add_text_button("Справка о доходах", color=ButtonColor.POSITIVE, payload={'btn_id': '3'})
main_keyboard.add_row()
main_keyboard.add_text_button("Путевка в санаторий ЧелГУ", color=ButtonColor.POSITIVE, payload={'btn_id': '4'})
main_keyboard.add_row()
main_keyboard.add_text_button("Вступление в Профсоюз", color=ButtonColor.PRIMARY, payload={'btn_id': '5'})

# Материальная помощь

mat_help_keyboard = Keyboard(one_time=False, inline=False)
mat_help_keyboard.add_text_button("Причины для оформления", color=ButtonColor.PRIMARY, payload={'btn_id': '6'})
mat_help_keyboard.add_text_button("Необходимые документы", color=ButtonColor.PRIMARY, payload={'btn_id': '7'})
mat_help_keyboard.add_row()
mat_help_keyboard.add_text_button("Порядок оформления", color=ButtonColor.PRIMARY, payload={'btn_id': '8'})
mat_help_keyboard.add_text_button("Срок подачи документов", color=ButtonColor.PRIMARY, payload={'btn_id': '9'})
mat_help_keyboard.add_row()
mat_help_keyboard.add_text_button("Частота выплат", color=ButtonColor.PRIMARY, payload={'btn_id': '10'})
mat_help_keyboard.add_text_button("Когда происходит выплата", color=ButtonColor.PRIMARY, payload={'btn_id': '11'})
mat_help_keyboard.add_row()
mat_help_keyboard.add_text_button("Не пришла выплата", color=ButtonColor.PRIMARY, payload={'btn_id': '12'})
mat_help_keyboard.add_text_button("Принятие документов", color=ButtonColor.PRIMARY, payload={'btn_id': '13'})
mat_help_keyboard.add_row()
mat_help_keyboard.add_text_button("Выплата по вакцинации", color=ButtonColor.PRIMARY, payload={'btn_id': '14'})
mat_help_keyboard.add_text_button("Критерии к карте", color=ButtonColor.PRIMARY, payload={'btn_id': '15'})
mat_help_keyboard.add_row()
mat_help_keyboard.add_text_button("Отсутствует/просрочен билет", color=ButtonColor.PRIMARY, payload={'btn_id': '16'})
mat_help_keyboard.add_row()
mat_help_keyboard.add_text_button("Назад", color=ButtonColor.NEGATIVE, payload={'btn_id': '0'})

# Социальная стипендия

social_payment_keyboard = Keyboard(one_time=False, inline=False)
social_payment_keyboard.add_text_button("Куда сдавать документы?", color=ButtonColor.PRIMARY, payload={'btn_id': '17'})
social_payment_keyboard.add_row()
social_payment_keyboard.add_text_button("Стипендия по проживанию в общежитии", color=ButtonColor.PRIMARY,
                                        payload={'btn_id': '18'})
social_payment_keyboard.add_row()
social_payment_keyboard.add_text_button("Назад", color=ButtonColor.NEGATIVE, payload={'btn_id': '0'})

# Справка о доходах
ref_income_keyboard = Keyboard(one_time=False, inline=False)
ref_income_keyboard.add_text_button("Как оформить справку о доходах?", color=ButtonColor.PRIMARY,
                                    payload={'btn_id': '19'})
ref_income_keyboard.add_row()
ref_income_keyboard.add_text_button("Назад", color=ButtonColor.NEGATIVE, payload={'btn_id': '0'})

# Путевка в санаторий Челгу
voucher_keyboard = Keyboard(one_time=False, inline=False)
voucher_keyboard.add_text_button("Что включает в себя путевка в санаторий?", color=ButtonColor.PRIMARY,
                                        payload={'btn_id': '20'})
voucher_keyboard.add_row()
voucher_keyboard.add_text_button("Документы для оформления", color=ButtonColor.PRIMARY,
                                        payload={'btn_id': '21'})
voucher_keyboard.add_row()
voucher_keyboard.add_text_button("Назад", color=ButtonColor.NEGATIVE, payload={'btn_id': '0'})

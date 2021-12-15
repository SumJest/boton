class Messages:
    hello_message = "Здравствуй, {name}, я бот, которому вы можете задавать вопросы, касающиеся профсоюзной " \
                    "организации ЮУрГУ. Перед тем как задать свой вопрос, посмотрите, может ответ уже есть в меню. " \
                    "Для этого выберете интересующую вас тему из представленных. Если это не решило ваш вопрос, " \
                    "то просто напишите мне его и вам ответят специалисты."

    @staticmethod
    def gettext(kb_id: str, txt_id: int) -> str:
        with open(f'texts/{kb_id}/{txt_id}.txt', 'r', encoding='utf-8') as file:
            message = file.read()
            file.close()
            return message

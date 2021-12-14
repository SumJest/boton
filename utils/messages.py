def get_mat_help_message(id) -> str:
    with open(f"texts/mathelp/{id}.txt", 'r', encoding="utf-8") as f:
        message = f.read()
        f.close()
        return message


def get_ref_income_message(id) -> str:
    with open(f"texts/ref_income/{id}.txt", 'r', encoding="utf-8") as f:
        message = f.read()
        f.close()
        return message


def get_soc_pay_message(id) -> str:
    with open(f"texts/social_payment/{id}.txt", 'r', encoding="utf-8") as f:
        message = f.read()
        f.close()
        return message


def get_voucher_message(id) -> str:
    with open(f"texts/voucher/{id}.txt", 'r', encoding="utf-8") as f:
        message = f.read()
        f.close()
        return message


class Messages:
    hello_message = "Здравствуй, {name}, я бот, которому вы можете задавать вопросы, касающиеся профсоюзной " \
                    "организации ЮУрГУ. Перед тем как задать свой вопрос, посмотрите, может ответ уже есть в меню. " \
                    "Для этого выберете интересующую вас тему из представленных. Если это не решило ваш вопрос, " \
                    "то просто напишите мне его и вам ответят специалисты."
    join_prof_message = "Чтобы вступить в профсоюз, необходимо написать заявление о вступлении в Профсоюз."

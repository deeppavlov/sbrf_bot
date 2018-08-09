import random

def provide_info_for_openning(s):
    s['__COMMANDS__'].append({'command': 'TERMINATE'})
    confidence = 1.0
    response = []
    p = s["properties"]
    if "DATES" in p:
        response.append("Открыте счета в день обращения при условии:\n\t- предоставления полного пакета документов\n\t- отсутствия замечаний к комплектности пакета документов\n\t- отсутствие действующих решений налоговых/таможенных органов о приостановлении операций по счетам")
    if "RATES" in p:
        response.append("Тарифы на обслуживание вы можете посмотреть на текущей странице сайта в разделе \"Полный перечень всехъ тарифов\" или по ссылке https://www.sberbank.ru/ru/s_m_business/bankingservice/rko/tariffs")
    if "DOCUMENTS" in p:
        response.append("Список необходимых документов вы можете посмотреть на текущей странице сайта в разделе \"Договор Банковского счета\"")
    if "REMOTE" in p:
        response.append("Вы можете зарезервировать счет в личном кабинете или на сайте Банка. Для открытия счета вам необходимо обратиться в отделение Банка.")
    if "PROCEDURE" in p:
        if "RUB" in s["currency"]:
            response.append("Для открытия счета в рублях вам необходимо обратиться в отделение")
        else:
            response.append(random.choice([
                "Для открытия расчетного счета в валюте необходимо обращаться только в офис Банка.",
                "Удаленно через систему возможно открыть только рублёвый расчётный счёт. Для открытия валютного счёта Вам стоит обратиться в отделения Банка.",
                "Для открытия валютного счета Вам необходимо обращаться только в офис Банка.",
                "Открыть валютный счет Вы можете только при личном обращении в офисе Банка."
            ]))

    return "\n".join(response), confidence, s


def provide_info_for_reservation(s):
    s['__COMMANDS__'].append({'command': 'TERMINATE'})
    confidence = 1.0
    response = []
    p = s["properties"]
    if "RATES" in p:
        response.append("Тарифы на обслуживание вы можете посмотреть на текущей странице сайта в разделе \"Полный перечень всехъ тарифов\" или по ссылке https://www.sberbank.ru/ru/s_m_business/bankingservice/rko/tariffs")
    if "DOCUMENTS" in p:
        response.append("Список необходимых документов вы можете посмотреть на текущей странице сайта в разделе \"Договор Банковского счета\"")
    if "QUESTIONNAIRE" in p:
        response.append("Анкета - информационные сведения клиента размещена на сайте банка в разделе \"Иные документы для открытия и ведения счета\"")
    if "PROCEDURE" in p:
        if "RUB" in s["currency"]:
            if "RS" in s["account_type"] or "GOZ" in s["account_type"]:
                response.append("Зарезервировать счет вы можете, перейдя по ссылке https://www.sberbank.ru/start")
            else:
                response.append("Счет указанного типа невозможно зарезервировать онлайн. Для его открытия вам необходимо обратиться в офис Банка")
        else:
            response.append(random.choice([
                "Для открытия расчетного счета в валюте необходимо обращаться только в офис Банка.",
                "Удаленно через систему возможно открыть только рублёвый расчётный счёт. Для открытия валютного счёта Вам стоит обратиться в отделения Банка.",
                "Для открытия валютного счета Вам необходимо обращаться только в офис Банка.",
                "Открыть валютный счет Вы можете только при личном обращении в офисе Банка."
            ]))

    return "\n".join(response), confidence, s


def ask_slot(state, params):
    confidence = 1.0
    if params['slot'] == 'currency':
        state['__COMMANDS__'].append({'command': 'UPDATE_SLOTS', 'slot': 'currency'})
        return random.choice([
            "В какой валюте Вы хотите открыть счёт?",
            "Уточните, пожалуйста, валюту, в которой Вы хотели бы открыть счет?",
            "Уточните, в какой валюте Вы желаете открыть счет?"
            "Уточните, в какой валюте Вы хотели-бы открыть расчетный счет?"
            ]), confidence, state
    elif params['slot'] == 'intent':
        state['__COMMANDS__'].append({'command': 'UPDATE_SLOTS', 'slot': 'intent'})
        return "Уточните: вы хотите открыть или зарезервировать счет?", confidence, state
    elif params['slot'] == 'properties':
        state['__COMMANDS__'].append({'command': 'UPDATE_SLOTS', 'slot': 'properties'})
        if state["intent"][0] == "RESERVE_ACCOUNT":
            return f"Какая информация вас интересует: тарифы, комплект документов, анкета или процедура открытия?", \
                   confidence, state
        elif state["intent"][0] == "OPEN_ACCOUNT":
            return f"Какая информация вас интересует: сроки, тарифы, комплект документов, удаленное обслуживание или процедура открытия?", \
                   confidence, state
        else:
            return "Упс, не знаю как и спросить :(", confidence, state
    elif params['slot'] == 'resident':
        state['__COMMANDS__'].append({'command': 'UPDATE_SLOTS_YES_NO', 'slot': 'resident',
                                      'yes': 'RESIDENT', 'no': 'NO_RESIDENT'})
        return "Уточните, Вы являетесь резидентом или нерезидентом?", confidence, state
    elif params['slot'] == 'client_type':
        state['__COMMANDS__'].append({'command': 'UPDATE_SLOTS_YES_NO', 'slot': 'client_type',
                                      'yes': 'INDIVIDUAL', 'no': 'ORGANIZATION'})
        return random.choice([
            "Какой тип организации (форма собственности), для которой Вы желаете открыть счёт? (ИП, ЮЛ, ООО, нотариус и пр.)",
            "Уточните, пожалуйста, форму собственности (тип) организации для которой желаете открыть счет? (ИП, ЮЛ, ООО, нотариус и пр.)",
            "Какова форма собственности (тип) организации? (ИП, ЮЛ, ООО, нотариус и пр.)"
            ]), confidence, state
    elif params['slot'] == 'account_type':
        state['__COMMANDS__'].append({'command': 'UPDATE_SLOTS', 'slot': 'account_type'})
        return random.choice([
            "Счет какого вида хотели бы открыть? (расчётный, валютный, ГОЗ, ТСЖ и пр.)",
            "Какой вид счета Вы планируете открыть? (расчётный, валютный, ГОЗ, ТСЖ и пр.)",
            ]), confidence, state
    else:
        return ("Упс, не знаю как и спросить про [%s] :(" % params['slot']), confidence, state


def update_slot(state, slot, value):
    state[slot]=value
    return None, None, state


def get():
    return [
        (lambda s: "OPEN_ACCOUNT" in s["intent"] and "RESERVE_ACCOUNT" in s["intent"], lambda s: update_slot(s, 'intent', ['RESERVE_ACCOUNT'])),
        (lambda s: not s["intent"] and not s["properties"], lambda s: ask_slot(s, {'slot': 'intent'})),
        (lambda s: not s["intent"] and s["properties"], lambda s: ask_slot(s, {'slot': 'intent'})),
        (lambda s: "OPEN_ACCOUNT" in s["intent"] and not s["properties"], lambda s: ask_slot(s, {'slot': 'properties'})),
        (lambda s: "RESERVE_ACCOUNT" in s["intent"] and not s["properties"], lambda s: ask_slot(s, {'slot': 'properties'})),
        (lambda s: s["intent"] and "DOCUMENTS" in s["properties"] and not s["resident"],
         lambda s: ask_slot(s, {'slot': 'resident'})),
        (lambda s: s["intent"] and "DOCUMENTS" in s["properties"] and not s["client_type"],
         lambda s: ask_slot(s, {'slot': 'client_type'})),
        (lambda s: s["intent"] and "PROCEDURE" in s["properties"] and not s["currency"],
         lambda s: ask_slot(s, {'slot': 'currency'})),
        (lambda s: "RESERVE_ACCOUNT" in s["intent"] and "PROCEDURE" in s["properties"] and not s["account_type"],
         lambda s: ask_slot(s, {'slot': 'account_type'})),
        (lambda s: "OPEN_ACCOUNT" in s["intent"] and s["properties"], provide_info_for_openning),
        (lambda s: "RESERVE_ACCOUNT" in s["intent"] and s["properties"], provide_info_for_reservation),
        (lambda s: True, lambda s: ("Я вас не понимаю. Спросите, пожалуйста, по другому", 1.0, s))
    ]
import json
import sys

from deeppavlov.core.commands.infer import build_model_from_config
from components.agent import Agent, HighestConfidenceSelector
from components.random_response_skill import RandomResponseSkill

from components.filter import IntentFilter
from components.tfidf_vectorizer import TfIdfVectorizer
from components.faq_cos import FaqCosineSimilarityModel

def init_agent():
    demo = build_model_from_config(json.load(open('skill.demo.json')), as_component=True)
    open_account = build_model_from_config(json.load(open('skill.open_account.json')), as_component=True)
    sms_inform = build_model_from_config(json.load(open('skill.sms_inform.json')), as_component=True)
    tarifs = build_model_from_config(json.load(open('skill.tarifs.json')), as_component=True)
    faq = build_model_from_config(json.load(open('skill.faq.json')), as_component=True)

    classifier = build_model_from_config(json.load(open('intent_classifier.json')), as_component=True)

    hello = RandomResponseSkill(
        responses=[
            'Я Demo-Бот:) Чем могу помочь? Я умею рассказывать про открытие и резервирование счетов, тарифы на услуги и продуты, подключение SMS-информирование и отвечать на FAQ-вопросы.',
            'Чем Вам помочь? Я умею рассказывать про открытие и резервирование счетов, тарифы на услуги и продуты, подключение SMS-информирование и отвечать на FAQ-вопросы.'
        ],
        confidence=0.5
    )

    knn_clf = build_model_from_config(json.load(open('knn_classifier.json')), as_component=True)

    intents = ['OTHER', 'OPEN_ACCOUNT', 'SMS_INFORM', 'RATES', 'FAQ']

    filter = IntentFilter(intents, knn_clf, default_intent=0, always_open=[0])

    agent = Agent([hello, demo, sms_inform, tarifs, faq], skills_selector=HighestConfidenceSelector(), skills_filter=filter)

    return agent


if __name__ == '__main__':
    agent = init_agent()
    for line in sys.stdin:
        print(agent([line]), flush=True)

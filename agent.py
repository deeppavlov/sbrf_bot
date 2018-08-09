from deeppavlov.core.commands.infer import build_model_from_config
from components.agent import Agent, HighestConfidenceSelector
from components.random_response_skill import RandomResponseSkill

from components.filter import IntentFilter
from components.tfidf_vectorizer import TfIdfVectorizer
from components.faq_cos import FaqCosineSimilarityModel

import json
import sys

demo = build_model_from_config(json.load(open('skill.demo.json')), as_component=True)
open_account = build_model_from_config(json.load(open('skill.open_account.json')), as_component=True)
sms_inform = build_model_from_config(json.load(open('skill.sms_inform.json')), as_component=True)
tarifs = build_model_from_config(json.load(open('skill.tarifs.json')), as_component=True)
faq = build_model_from_config(json.load(open('skill.faq.json')), as_component=True)

classifier = build_model_from_config(json.load(open('intent_classifier.json')), as_component=True)

knn_clf = build_model_from_config(json.load(open('knn_classifier.json')), as_component=True)

hello = RandomResponseSkill(
    responses=[
        'Привет! Чем могу помочь?',
        'Привет! Я SBRF Demo Бот :) Чем вам помочь? Я могу рассказть про открытие и резервирование счетов, тарифы на услуги и продуты, а так же подключить SMS-информирование.',
        'Хай, чувачек! Че надо?'
    ],
    confidence=0.5
)

intents = ['OTHER', 'OPEN_ACCOUNT', 'SMS_INFORM', 'RATES', 'FAQ']

filter = IntentFilter(intents, knn_clf, default_intent=0, always_open=[0])

agent = Agent([hello, demo, sms_inform, tarifs, faq], skills_selector=HighestConfidenceSelector(), skills_filter=filter)


for line in sys.stdin:
    print(agent([line]), flush=True)
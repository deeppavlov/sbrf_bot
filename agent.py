from deeppavlov.core.commands.infer import build_model_from_config
from deeppavlov.core.agent import Agent, HighestConfidenceSelector

from filter import IntentFilter

import json
import sys

demo = build_model_from_config(json.load(open('skill.demo.json')), as_component=True)
open_account = build_model_from_config(json.load(open('skill.open_account.json')), as_component=True)
sms_inform = build_model_from_config(json.load(open('skill.sms_inform.json')), as_component=True)
tarifs = build_model_from_config(json.load(open('skill.tarifs.json')), as_component=True)

classifier = build_model_from_config(json.load(open('intent_classifier.json')), as_component=True)

intents = ['DEMO', 'SMS_INFORM', 'TARIFS']

filter = IntentFilter(intents, classifier, default_intent=0)

agent = Agent([demo, sms_inform, tarifs], skills_selector=HighestConfidenceSelector(), skills_filter=filter)

for line in sys.stdin:
    print(agent([line]), flush=True)
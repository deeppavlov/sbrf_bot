import random

from deeppavlov.core.models.component import Component


class RandomResponseSkill(Component):
    def __init__(self, responses, confidence):
        if isinstance(responses, str):
            responses = [responses]
        self.responses = responses
        self.confidence = confidence

    def __call__(self, utterances_batch, history_batch, states_batch):
        response = [random.choice(self.responses) for _ in utterances_batch]
        confidence = [self.confidence] * len(utterances_batch)
        state = [None] * len(utterances_batch)
        return response, confidence, state

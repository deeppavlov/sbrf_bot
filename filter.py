from deeppavlov.core.models.component import Component
from deeppavlov.core.common.log import get_logger

logger = get_logger(__name__)


class IntentFilter(Component):
    def __init__(self, intents, clf, default_intent=0, *args, **kwargs):
        self.intents = intents
        self.size = len(intents)
        self.clf = clf
        self.max_batch_size = 128
        self.intent_idxs = [default_intent]*self.max_batch_size

    def __call__(self, utterances, batch_history):
        result = [[False] * self.size] * len(utterances)
        clf_result = self.clf(utterances)
        logger.info(f"Intent from classifier: {clf_result}")
        for i in range(len(utterances)):
            if "intent" in clf_result[i]:
                self.intent_idxs[i] = self.intents.index(clf_result[i]["intent"])
                logger.info(f"Intent index: {self.intent_idxs[i]}")
            result[i][self.intent_idxs[i]] = True
        logger.info(f"Filter result: {result}")
        return result

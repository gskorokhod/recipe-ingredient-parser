from utils import *
from constants import *
from features import doc_to_features
import os
import pycrfsuite
from unidecode import unidecode


class Parser:
    def __init__(self, path):
        tagger = pycrfsuite.Tagger()
        tagger.open(path)
        self.tagger = tagger

    def parse(self, sent):
        ans = {}

        prepared_sent = sent_to_features(sent)
        features = doc_to_features(prepared_sent)
        tagged = self.tagger.tag(features)

        for pr, tag in zip(prepared_sent, tagged):
            ans[pr[0]] = tag

        return ans


if __name__ == '__main__':
    models = list(os.listdir(MODEL_DIR))
    default_path = ''

    if models:
        models.sort()
        default_path = f'{MODEL_DIR}/{models[-1]}'

        parser = Parser(default_path)

        while True:
            inpt = input('Sentence or q to exit: ')
            if inpt.lower() == 'q':
                exit(0)
            else:
                print(parser.parse(inpt))
                print()

    else:
        print('WARNING: Model dir empty!')

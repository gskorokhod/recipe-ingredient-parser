import os
from itertools import chain
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelBinarizer
from constants import MODEL_DIR
from features import doc_to_features, prepare_data
import pycrfsuite
from get_tagged_dataset import get_ds
from utils import split_dataset, doc_to_words, doc_to_tags
from collections import Counter

dataset = get_ds()
labels = {'OTHER', 'I-COMMENT', 'B-RANGE_END', 'B-NAME',
          'B-COMMENT', 'I-UNIT', 'B-INDEX', 'B-QTY', 'I-NAME', 'B-UNIT'}


def bio_classification_report(y_true, y_pred):
    """
    Classification report for a list of BIO-encoded sequences.
    It computes token-level metrics and discards "O" labels.

    Note that it requires scikit-learn 0.15+ (or a version from github master)
    to calculate averages properly!
    """
    lb = LabelBinarizer()
    y_true_combined = lb.fit_transform(list(chain.from_iterable(y_true)))
    y_pred_combined = lb.transform(list(chain.from_iterable(y_pred)))

    return classification_report(
        y_true_combined,
        y_pred_combined,
    )


def print_transitions(trans_features):
    for (label_from, label_to), weight in trans_features:
        print("%-6s -> %-7s %0.6f" % (label_from, label_to, weight))


def print_state_features(state_features):
    for (attr, label), weight in state_features:
        print("%0.6f %-6s %s" % (weight, label, attr))


models = os.listdir(MODEL_DIR)

if not models:
    print('Model dir empty!')
    exit(0)

models.sort()
path = f'{MODEL_DIR}/{models[-1]}'

ln = len(dataset)
train_set, test_set = split_dataset(dataset[:ln], 0.05)

tagger = pycrfsuite.Tagger()
tagger.open(path)


info = tagger.info()

print("Top likely transitions:")
print_transitions(Counter(info.transitions).most_common(15))

print("\nTop unlikely transitions:")
print_transitions(Counter(info.transitions).most_common()[-15:])

print("Top positive:")
print_state_features(Counter(info.state_features).most_common(20))

print("\nTop negative:")
print_state_features(Counter(info.state_features).most_common()[-20:])

input()

x_test, y_test = prepare_data(test_set)
y_pred = [tagger.tag(xseq) for xseq in x_test]
print(bio_classification_report(y_test, y_pred))

for example_doc in test_set:
    print(' '.join(doc_to_words(example_doc)), end='\n\n')

    print("Predicted:", ' '.join(tagger.tag(doc_to_features(example_doc))))
    print("Correct:  ", ' '.join(doc_to_tags(example_doc)))

    print('\nInput q to end or anything else to print the next one...')
    while True:
        inpt = input()
        if inpt.lower() == 'q':
            exit(0)
        else:
            break



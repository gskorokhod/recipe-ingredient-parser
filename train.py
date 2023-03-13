import pycrfsuite
import constants
from get_tagged_dataset import get_ds
from utils import split_dataset, get_tag_vocabulary
from features import prepare_data
from datetime import datetime

dataset = get_ds()

print('Finding label set...')
labels = get_tag_vocabulary(dataset)
print(f'Labels: {labels}')

ln = len(dataset)
# ln = int(len(dataset) * 0.9)  # Try on a smaller DS for now

train_set, test_set = split_dataset(dataset[:ln], constants.TEST_SIZE)

print(f'{len(train_set)} training documents')
print('Preparing data...')
x_train, y_train = prepare_data(train_set)

print('Creating model...')
trainer = pycrfsuite.Trainer(verbose=True)

for xseq, yseq in zip(x_train, y_train):
    trainer.append(xseq, yseq)

trainer.set_params({
    'c1': 1.0,   # coefficient for L1 penalty
    'c2': 1e-3,  # coefficient for L2 penalty
    'max_iterations': 1000,  # stop earlier
    'feature.possible_transitions': True  # include transitions that are possible, but not observed
})

print('Fitting model...')
timestamp = str(datetime.now()).replace(' ', '_').replace(':', '-').replace('.', '-')
path = f'{constants.MODEL_DIR}/model-{timestamp}.crfsuite'
trainer.train(path)
print('Fitting done!')

print('Last iteration:')
print(trainer.logparser.last_iteration)

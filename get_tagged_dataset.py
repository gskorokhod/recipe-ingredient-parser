import os
from utils import normalize
from constants import DATASET_FILE, DATA_DIR
import nltk


IN_PAREN_TAG = 'YesPAREN'


def get_ds():
    ans = []
    curr_sentence = []

    with open(DATASET_FILE, 'r') as in_file:
        lines = in_file.readlines()

        for i, line in enumerate(lines):
            print(f'Processing line {i} of {len(lines)}')
            line = line.strip()
            if line:
                words = [x for x in line.split() if x]
                token, i_tg, l_tg, is_cap, is_in_parenthesis, tag = words
                curr_sentence.append((token, is_in_parenthesis == IN_PAREN_TAG, tag))
            else:
                tokens = [tk for tk, _, _ in curr_sentence]
                tagged = nltk.pos_tag(tokens)

                # Take the word, POS tag, and its label
                sentence = [(word, is_par, pos, label) for (word, is_par, label), (_, pos) in zip(curr_sentence, tagged)]

                ans.append(sentence[:])
                curr_sentence = []
    print()
    return ans


def get_ingredient_set():
    if os.path.exists(f'{DATA_DIR}/ingredients.txt'):
        with open(f'{DATA_DIR}/ingredients.txt', 'r') as f:
            return set([x.strip() for x in f.readlines()])
    else:
        ds = get_ds()
        return get_ingredient_set_from_ds(ds)


def get_ingredient_set_from_ds(ds):
    #ingredient_list = [normalize(x.sentence) for x in IngredientSimilarity.similarity.get_ingredients()]
    ingredient_set = set()

    new_ings = []
    for doc in ds:
        for word, _, _, tag in doc:
            if 'NAME' in tag:
                new_ings.append(normalize(word))

    ingredient_set = ingredient_set.union(set(new_ings))

    with open('data/ingredients.txt', 'w') as f:
        for ing in ingredient_set:
            f.write(ing + '\n')

    return ingredient_set


if __name__ == '__main__':
    print(get_ds())

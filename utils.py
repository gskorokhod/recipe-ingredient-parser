import nltk
from unidecode import unidecode
from get_tagged_dataset import get_ingredient_set
from constants import *
from IngredientSimilarity import normalize


normalized_units = [normalize(x) for x in UNITS]
ingredient_set = get_ingredient_set()


def is_number(s):
    return all([ch in NUMBER_SYMBOLS for ch in s])


def is_unit(s):
    norm = normalize(s)
    return norm in normalized_units


def is_ingredient(s):
    norm = normalize(s)
    return norm in ingredient_set


def get_length_bracket(s):
    last_bracket = LENGTH_BRACKETS[0]

    for br in LENGTH_BRACKETS:
        if len(s) >= br:
            last_bracket = br
        else:
            break

    return last_bracket


def untag(tagged_docs):
    return [doc[:3] for doc in tagged_docs]


def doc_to_tags(tagged_doc):
    return [tag for word, is_in_parenthesis, pos, tag in tagged_doc]


def doc_to_words(tagged_doc):
    return [word for word, is_in_parenthesis, pos, tag in tagged_doc]


def get_word_vocabulary(tagged_docs):
    ans = set()
    for doc in tagged_docs:
        doc_vocab = set(doc_to_words(doc))
        ans = ans.union(doc_vocab)
    return ans


def get_tag_vocabulary(tagged_docs):
    ans = set()
    for doc in tagged_docs:
        doc_vocab = set(doc_to_tags(doc))
        ans = ans.union(doc_vocab)
    return ans


def split_dataset(ds, test_size):
    train_size = 1.0 - test_size
    train_last_ind = int(train_size * len(ds))

    return ds[:train_last_ind], ds[train_last_ind:]


def split_sentence(st):
    ans = []

    ascii_text = unidecode(st)
    words = ascii_text.split()

    for token in words:
        new_tokens = []
        next_token = ''
        prev_ch = None
        for i in range(len(token)):
            ch = token[i]

            if prev_ch is not None:
                if prev_ch in NUMBER_SYMBOLS and ch not in NUMBER_SYMBOLS:
                    new_tokens.append(next_token)
                    next_token = ''

            if ch in PUNCTUATION:
                if next_token:
                    new_tokens.append(next_token)
                new_tokens.append(ch)
                next_token = ''
            else:
                next_token += ch
            prev_ch = ch

        if next_token:
            new_tokens.append(next_token)
        if new_tokens:
            ans.extend(new_tokens)

    return ans


def cleanup(tokens):
    ans = []

    for tk in tokens:
        tk = tk.lower()

        for rep in REPLACEMENTS.keys():
            if rep in tk:
                tk = tk.replace(rep, REPLACEMENTS[rep])

        if tk in SHORTENINGS:
            tk = SHORTENINGS[tk]

        ans.append(tk)

    return ans


def prepare_features(tokens):
    bracket_count = 0
    features = []
    pos_tagged = nltk.pos_tag(tokens)

    for tk in tokens:
        if tk == '(':
            bracket_count += 1
        elif tk == ')':
            bracket_count = max(bracket_count - 1, 0)

        features.append((tk, bracket_count > 0))

    ans = [(word, is_in_par, pos) for (word, is_in_par), (_, pos) in zip(features, pos_tagged)]
    return ans


def sent_to_features(sent):
    return prepare_features(cleanup(split_sentence(sent)))

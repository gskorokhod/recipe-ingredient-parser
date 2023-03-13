from utils import is_unit, is_number, untag, doc_to_tags, get_length_bracket, is_ingredient


def get_features(doc, i):
    word, is_in_parenthesis, pos = doc[i][:3]

    # Common features for all words
    features = [
        'bias',
        'word.lower=%s' % word.lower(),  # Maybe try normalize(word) in the future?
        'prefix_1=%s' % word[0],
        'prefix_2=%s' % word[:2],
        'prefix_3=%s' % word[:3],
        'prefix_4=%s' % word[:4],
        'suffix_1=%s' % word[-1],
        'suffix_2=%s' % word[-2:],
        'suffix_3=%s' % word[-3:],
        'suffix_4=%s' % word[-4:],
        'is_in_parenthesis=%s' % is_in_parenthesis,
        'is_capitalized=%s' % word[0].isupper(),
        'is_unit=%s' % is_unit(word),
        'is_ingredient=%s' % is_ingredient(word),
        'is_number=%s' % is_number(word),
        'index=%s' % i,  # People don't seem to use this, may remove in the future
        'length_bracket=%s' % get_length_bracket(word),
        'pos=%s' % pos
    ]

    # Features for words that are not
    # at the beginning of a document
    if i > 0:
        prev_word, prev_is_in_parenthesis, prev_pos = doc[i - 1][:3]

        features.extend([
            'prev_word.lower=%s' % prev_word.lower(),
            'prev_is_in_parenthesis=%s' % prev_is_in_parenthesis,
            'prev_word.is_unit=%s' % is_unit(prev_word),
            'prev_word.is_ingredient=%s' % is_ingredient(prev_word),
            'prev_word.is_number=%s' % is_number(prev_word),
            'prev_word.pos=%s' % prev_pos,
        ])
    else:
        features.append('BOS')

    # Features for words that are not
    # at the beginning of a document
    if i < len(doc) - 1:
        next_word, next_is_in_parenthesis, next_pos = doc[i + 1][:3]

        features.extend([
            'next_word.lower=%s' % next_word.lower(),
            'prev_is_in_parenthesis=%s' % next_is_in_parenthesis,
            'next_word.is_unit=%s' % is_unit(next_word),
            'next_word.is_ingredient=%s' % is_ingredient(next_word),
            'next_word.is_number=%s' % is_number(next_word),
            'next_word.pos=%s' % next_pos,
        ])
    else:
        features.append('EOS')

    return features


def doc_to_features(doc):
    return [get_features(untag(doc), index) for index in range(len(doc))]


def prepare_data(tagged_docs):
    x, y = [], []

    ln = len(tagged_docs)
    for i, doc in enumerate(tagged_docs):
        print(f'Processing tagged doc {i} of {ln}', end=" ")

        features = doc_to_features(doc)
        # print(features, end=" ")

        tags = doc_to_tags(doc)
        # print(tags)

        x.append(features[:])
        y.append(tags[:])

    return x, y


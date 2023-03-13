from nltk import PorterStemmer

from IngredientSimilarity.constants import *


ps = PorterStemmer()


def longest_common_substring(s1, s2):
    m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in range(1, 1 + len(s1)):
        for y in range(1, 1 + len(s2)):
            if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    return s1[x_longest - longest: x_longest]


def split_by_condition(st, cond):
    ans = []
    current_word = ''
    for ch in st:
        if cond(ch):
            ans.append(current_word)
            current_word = ''
        else:
            current_word += ch
    if current_word:
        ans.append(current_word)
    return ans


def split_by_symbols_and_nonascii(ch):
    if ch.isascii():
        if ch not in SYMBOLS_TO_SPLIT:
            return False
    return True


def split_by_symbols(ch):
    return ch in SYMBOLS_TO_SPLIT


def normalize_and_split(st, stem=True, split_condition=split_by_symbols_and_nonascii):
    st = st.strip().lower()
    split_st = split_by_condition(st, split_condition)
    ans = []
    for word in split_st:
        if word and (word not in WORDS_TO_REMOVE):
            if stem:
                ans.append(ps.stem(word))
            else:
                ans.append(word)
    return ans


def normalize(st, stem=True, split_condition=split_by_symbols_and_nonascii):
    return ' '.join(normalize_and_split(st, stem=stem, split_condition=split_condition))

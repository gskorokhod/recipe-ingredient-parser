import json
import os.path

from IngredientSimilarity.utils import *
from IngredientSimilarity.constants import *


class BagOfWords:
    def __init__(self, words=None):
        self.words = set()

        if words is not None:
            self.add(words)

    def __hash__(self):
        return hash(tuple(self.words))

    def __eq__(self, other):
        return self.words == other.words

    def __ne__(self, other):
        return self.words != other.words

    def __repr__(self):
        return str(self.words)

    def __str__(self):
        return str(self.words)

    def get_total_words(self):
        return sum(pair[1] for pair in self.words)

    def add_sentence(self, sentence):
        bag_dict = {}

        for el in self.words:
            key, amt = el
            bag_dict[key] = amt

        words = normalize_and_split(sentence, stem=True, split_condition=split_by_symbols_and_nonascii)
        for wd in words:
            if wd in bag_dict.keys():
                bag_dict[wd] += 1
            else:
                bag_dict[wd] = 1

        bag = set()
        for key in bag_dict:
            bag.add((key, bag_dict[key]))

        self.words = bag

    def add_bow(self, other):
        bag_dict = {}

        for el in self.words:
            key, amt = el
            bag_dict[key] = amt

        for pair in other.words:
            key, amt = pair
            if key in bag_dict.keys():
                bag_dict[key] += amt
            else:
                bag_dict[key] = amt

        bag = set()
        for key in bag_dict:
            bag.add((key, bag_dict[key]))

        self.words = bag

    def add(self, obj):
        if isinstance(obj, str):
            self.add_sentence(obj)
        elif isinstance(obj, BagOfWords):
            self.add_bow(obj)
        elif issubclass(obj.__class__, BagOfWords):
            self.add_bow(obj)
        else:
            raise ValueError("Must be bag of words or string!")

    def union(self, other):
        bow = BagOfWords(self)
        bow.add_bow(other)
        return bow

    def get_similarity_by_substring_len(self, other):
        total_ans = 0
        for w1 in self.words:
            ans = 0
            for w2 in other.words:
                substr_len = len(longest_common_substring(w1[0], w2[0]))
                substr_ratio = substr_len / max(len(w1[0]), len(w2[0]))
                substr = substr_ratio * max(w1[1], w2[1])
                if substr > ans:
                    ans = substr
            total_ans += ans
        return total_ans / max(self.get_total_words(), other.get_total_words())

    def get_similarity_by_exact_matches(self, other):
        ans = 0
        for w1 in self.words:
            for w2 in other.words:
                if w1[0] == w2[0]:
                    ans += min(w1[1], w2[1])
        return ans / min(self.get_total_words(), other.get_total_words())

    def get_similarity(self, other):
        s1 = self.get_similarity_by_substring_len(other)
        s2 = self.get_similarity_by_exact_matches(other)

        return (s1 + s2) / 2


class Ingredient(BagOfWords):
    def __init__(self, sentence, appearances=None):
        super().__init__(sentence)
        self.sentence = normalize(sentence, stem=False, split_condition=split_by_symbols)
        self.appearances = appearances

    def __str__(self):
        return f"Ingredient '{self.sentence}'"

    def __repr__(self):
        return f"Ingredient '{self.sentence}', BOW: ({self.words})"

    def __hash__(self):
        return hash(tuple(self.words))


def get_best_match(st, ingredients):
    in_bow = Ingredient(st)
    sim = -1
    ans = None
    for ing in ingredients:
        if ing.get_similarity(in_bow) > sim:
            sim = ing.get_similarity(in_bow)
            ans = ing
    return (ans, sim)


def generate_similarity_matrix(ingredients):
    n = len(ingredients)
    similarity_matrix = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                similarity_matrix[i][j] = 1
            else:
                similarity_matrix[i][j] = ingredients[i].get_similarity(ingredients[j])
    return similarity_matrix


def get_similarity_matrix():
    if os.path.exists(SIMILARITY_MATRIX_FILE):
        with open(SIMILARITY_MATRIX_FILE, 'r') as f:
            similarity_matrix = []

            lines = f.readlines()
            n = len(lines)

            for i, line in enumerate(lines):
                print(f'Reading line {i} of {n}', end=" ")

                line = line.strip('\n')
                ln = []
                for nm in line.split(";"):
                    if nm:
                        ln.append(float(nm))
                if len(ln) != n:
                    print('WARNING: inconsistent length', end="")
                print()
                similarity_matrix.append(ln)

            return similarity_matrix
    else:
        ingredients = get_ingredients()
        similarity_matrix = generate_similarity_matrix(ingredients)
        n = len(similarity_matrix)

        print(f"Saving similarity matrix to file...")
        with open(SIMILARITY_MATRIX_FILE, 'a') as f:
            for i in range(n):
                for j in range(n):
                    f.write(str(similarity_matrix[i][j]) + ';')
                f.write('\n')

        return similarity_matrix


def get_ingredients():
    print("Looking in path: " + os.path.abspath(INGREDIENTS_FILE))
    ans = []
    if os.path.exists(INGREDIENTS_FILE):
        print(f'Found cache file!')

        with open(INGREDIENTS_FILE, 'r') as f:
            lines = f.readlines()
            n = len(lines)

            for i, line in enumerate(lines):
                print(f'Processing {i} of {n}')

                line = line.strip('\n')
                name, amt = line.split(';')
                ans.append(Ingredient(name, int(amt)))
    elif os.path.exists(DATASET_FILE):
        print(f'No cache file, reading from dataset...')

        with open(DATASET_FILE, 'r') as f:
            data = json.load(f)

            temp_ingredients = {}
            size = len(data)

            for i, recipe in enumerate(data):
                print(f'Processing {i} of {size}')
                for ing in recipe['ingredients']:
                    if '®' not in ing:
                        sp = normalize(ing, stem=True, split_condition=split_by_symbols_and_nonascii).strip()
                        if sp:
                            bow = BagOfWords(sp)
                            if bow in temp_ingredients.keys():
                                temp_ingredients[bow][0] += 1
                            else:
                                sentence = normalize(ing, stem=False, split_condition=split_by_symbols)
                                temp_ingredients[bow] = (1, sentence)

            for ing in temp_ingredients.keys():
                amt, sentence = temp_ingredients[ing]
                ans.append(Ingredient(sentence, appearances=amt))
        if ans:
            print(f'Writing {len(ans)} ingredients to cache file...')
            with open(INGREDIENTS_FILE, 'w') as f:
                for ing in ans:
                    f.write(ing.sentence + '\n')
    else:
        print("WARNING! Could not find dataset or cache file")

    return ans


if __name__ == '__main__':
    ings = get_ingredients()
    while True:
        print()
        inpt = input("Sentence to test: ")
        ans, sim = get_best_match(inpt, ings)
        print(f'Best match: {ans}')
        print(f'Similarity: {sim}')



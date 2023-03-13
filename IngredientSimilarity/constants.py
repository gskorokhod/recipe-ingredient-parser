import os

SYMBOLS_TO_SPLIT = '.,-<>/?\'\";:[{]}\|=+_)(*&^%$#@!~№;%:?Х\\0123456789 '  # When normalizing, split on the following symbols

WORDS_TO_REMOVE = ['and', 'or', 'of', 'to', 'a', 'the', 'in', 'on', 'under', 'over', 'out',  # Prepositions, articles, etc
                   'large', 'small', 'medium', 'big', 'huge', 'tiny',  # Size adjectives
                   'well', 'good', 'best', 'super', 'proper', 'nice',  # Subjective adjectives (probably not part of ingredient name)
                   'deep', 'cold', 'warm', 'luke', 'lukewarm', 'chilled', 'chill']  # Temperature adjectives

ROOT_DIR = os.path.abspath(os.getcwd())
if not ROOT_DIR.endswith('/IngredientSimilarity'):
    ROOT_DIR = os.path.join(ROOT_DIR, 'IngredientSimilarity')

DATADIR = f'{ROOT_DIR}/data'
TMPDIR = f'{ROOT_DIR}/tmp'

DATASET_FILE = f'{DATADIR}/dataset.json'
INGREDIENTS_FILE = f'{TMPDIR}/ingredients.txt'
PAIRS_FILE = f'{TMPDIR}/pairs.txt'
SIMILARITY_MATRIX_FILE = f'{TMPDIR}/similarity.txt'

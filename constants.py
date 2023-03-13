DATA_DIR = 'data'
MODEL_DIR = 'model'
DATASET_FILE = f'{DATA_DIR}/tagged_phrases'


TEST_SIZE = 0.2

LENGTH_BRACKETS = [0, 2, 4, 6, 8, 12, 16, 20]
PUNCTUATION = '!"\';:@#~]}[{/?.>,<\\|£$%^&*()-_=+'
NUMBER_SYMBOLS = '0123456789$/.,'  # $ is used to clump fractions
SYMBOLS_TO_SPLIT = '.,-<>/?\'\";:[{]}\|=+_)(*&^%$#@!~№;%:?Х\\0123456789 '  # When normalizing, split on the following symbols
WORDS_TO_REMOVE = ['and', 'or', 'of', 'to', 'a', 'the', 'in', 'on', 'under', 'over', 'out',  # Prepositions, articles, etc
                   'large', 'small', 'medium', 'big', 'huge', 'tiny',  # Size adjectives
                   'well', 'good', 'best', 'super', 'proper', 'nice',  # Subjective adjectives (probably not part of ingredient name)
                   'deep', 'cold', 'warm', 'luke', 'lukewarm', 'chilled', 'chill']  # Temperature adjectives


REPLACEMENTS = {
    'liter': 'litre',  # Replace American spelling with proper English
    'meter': 'metre',
    'gramme': 'gram',
    'gramm': 'gram',  # Common spelling mistake
}

SHORTENINGS = {
    'tsp': 'teaspoon',  # Expand shortened units
    'tbsp': 'tablespoon',
    'g': 'gram',
    'mg': 'milligram',
    'kg': 'kilogram',
    'ml': 'millilitre',
    'l': 'litre',
    'mm': 'millimetre',
    'cm': 'centimetre',
    'dm': 'decimetre',
    'm': 'metre',
}

UNITS = ['cup', 'ounce', 'pound', 'teaspoon', 'tablespoon',
         'milligram', 'gram', 'kilogram',
         'millilitre', 'litre', 'gallon',
         'millimetre', 'centimetre', 'decimetre', 'metre',
         'pinch']


DATA_DIR = 'data'
MODEL_DIR = 'model'
DATASET_FILE = f'{DATA_DIR}/tagged_phrases'


TEST_SIZE = 0.2

LENGTH_BRACKETS = [0, 2, 4, 6, 8, 12, 16, 20]
PUNCTUATION = '!"\';:@#~]}[{/?.>,<\\|£$%^&*()-_=+'
NUMBER_SYMBOLS = '0123456789$/.,'  # $ is used to clump fractions

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


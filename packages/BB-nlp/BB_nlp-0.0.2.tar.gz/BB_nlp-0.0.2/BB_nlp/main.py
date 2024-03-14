from nltk.corpus import wordnet as wn
from nltk import download

download('wordnet')
tag_map = {
    'CC': None,  # Coordinating conjunction
    'WDT': None,  # Wh-determiner
    'WP': None,  # Wh-pronoun
    'WP$': None,  # Possessive wh-pronoun
    'DT': None,  # Determiner
    'FW': None,  # Foreign word
    'LS': None,  # List item marker
    'MD': None,  # Modal
    'POS': None,  # Possessive ending
    'PRP': None,  # Personal pronoun
    'PRP$': None,  # Possessive pronoun
    'SYM': None,  # Symbol
    'TO': None,  # to
    'UH': None,  # Interjection
    'JJ': [wn.ADJ, wn.ADJ_SAT],  # Adjective
    'JJR': [wn.ADJ, wn.ADJ_SAT],  # Adjective, comparative
    'JJS': [wn.ADJ, wn.ADJ_SAT],  # Adjective, superlative
    'PDT': [wn.ADJ_SAT, wn.ADJ],  # Predeterminer
    'RP': [wn.ADJ, wn.ADJ_SAT],  # Particle
    'CD': wn.NOUN,  # Cardinal number
    'NN': wn.NOUN,  # Noun, singular or mass
    'NNS': wn.NOUN,  # Noun, plural
    'NNP': wn.NOUN,  # Proper noun, singular
    'NNPS': wn.NOUN,  # Proper noun, plural
    'EX': wn.ADV,  # Existential there
    'IN': wn.ADV,  # Preposition or subordinating conjunction
    'RB': wn.ADV,  # Adverb
    'RBR': wn.ADV,  # Adverb, comparative
    'RBS': wn.ADV,  # Adverb, superlative
    'WRB': wn.ADV,  # Wh-adverb
    'VB': wn.VERB,  # Verb, base form
    'VBD': wn.VERB,  # Verb, past tense
    'VBG': wn.VERB,  # Verb, gerund or present participle
    'VBN': wn.VERB,  # Verb, past participle
    'VBP': wn.VERB,  # Verb, non-3rd person singular present
    'VBZ': wn.VERB,  # Verb, 3rd person singular present
}


def get_tag(word):
    if tag_map.__contains__(word):
        return tag_map[word]
    return None

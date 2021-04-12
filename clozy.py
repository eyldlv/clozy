import spacy
import re
from typing import Tuple, List
from random import randint

nlp = spacy.load('de_core_news_sm')



def erase_token(token:str, schuettelbox:List[str]) -> str:
    """ Return a tuple containing the blank"""
    return ' (' + str(len(schuettelbox)+1) + ')' + '_' * (len(token)*2 +1) 


def get_positions_of_pos(doc, tags):
    return [i for i in range(len(doc)) if doc[i].pos_ in tags]


def detokenizer(line: List[str]) -> str:
    return "".join(' ' + token if token.isalpha() else token for token in line)[1:]


def remove_adja_suffix(token, schuettelbox):
    """Remove suffixes from declined adjectives."""
    return ' (' + str(len(schuettelbox)+1) + ') ' + re.sub(r'(es|er|em|en|e)$', '____', token) 


def add_blank_to_adjd(token, schuettelbox):
    return ' (' + str(len(schuettelbox)+1) + ') ' + token + '____'

file = 'sample_texts/text1.txt'
n = 10


def remove_nth_word(text:List[spacy.tokens.Token], schuettelbox:List[str], n:int=10):
    return_string = []
    token_ctr = 0
    for token in text:
        token_ctr += 1
        if token_ctr >= n and token.is_alpha:
            token_ctr = 0
            return_string.append(erase_token(token.text, schuettelbox))
            schuettelbox.append(token.text)
        else:
            return_string.append(token.text)
    return detokenizer(return_string), schuettelbox


def remove_pos_new(text:List[spacy.tokens.Token], schuettelbox:List[str], tags:List[str]=['NOUN'], percentage:int=1) -> Tuple[str, List[str]]:
    """
    Turn a certain pos tag in the text to blanks. Nouns by default. All words of the same pos will be removed unless a diffrent percentage is given.

    Return a tuple containing the blanked text and a list of strings with the removed tokens.
    """
    return_string = []
    positions = get_positions_of_pos(text, tags)
    random_positions = [positions.pop(randint(0,len(positions)-1)) for _ in range(round(len(positions)*percentage))]
    for position, token in enumerate(text):
        if position in random_positions:
            return_string.append(erase_token(token.text, schuettelbox))
            schuettelbox.append(token.text)
        else:
            return_string.append(token.text)
    return detokenizer(return_string), schuettelbox

def remove_adjective_suffixes(text, schuettelbox):
    return_string = []
    for token in text:
        if token.tag_ == 'ADJD':
            return_string.append(add_blank_to_adjd(token.text, schuettelbox))
            schuettelbox.append(token.text)
        elif token.tag_ == 'ADJA':
            return_string.append(remove_adja_suffix(token.text, schuettelbox))
            schuettelbox.append(token.text)
        else:
            return_string.append(token.text)
    return detokenizer(return_string), schuettelbox


def print_schuettelbox(schuettelbox):
    print('Lösung:')
    print('---------------')
    for position, word in enumerate(schuettelbox,1):
        print(f'({position}) {word}')


def check(text):
    for token in text:
        print(token.text, token.pos_, sep='\t')

tags = ['NOUN']


schuettelbox = []
blank_text = []

with open('sample_texts/junk.txt', 'r') as f:
    for line in f:
        text = nlp(line)
        a = remove_nth_word(text, schuettelbox, 15)
        blank_text += [a[0]]


for paragraph in blank_text:
    print(paragraph)
print_schuettelbox(schuettelbox)



schuettelbox = []
blank_text = []

with open('sample_texts/junk.txt', 'r') as f:
    for line in f:
        text = nlp(line)
        a = remove_pos_new(text, schuettelbox, ['ADP'], 0.5)
        blank_text += [a[0]]


for paragraph in blank_text:
    print(paragraph)
print_schuettelbox(schuettelbox)



with open ('sample_texts/junk.txt', 'r') as f:
    schuettelbox = []
    blank_text = []
    for line in f:
        text = nlp(line)
        blank, schuettel = remove_adjective_suffixes(text, schuettelbox)
        # print(schuettel)
        blank_text += [blank]
        # schuettelbox += schuettel

for paragraph in blank_text:
    print(paragraph)
print_schuettelbox(schuettelbox)
# check(text)

# NOUN, VERB, AUX, ADJ, ADV (noch, jedoch, schon, selten), ADP (präpositionen), DET, SCONJ (dass), CCONJ (und, aber)
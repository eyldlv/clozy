import spacy
import re
from typing import Tuple, List
from random import randint

nlp = spacy.load('de_core_news_sm')
adjective_suffixes = {'er', 'e', 'es', 'em', 'en'}


def erase_token(token, schuettelbox):
    retr_string = ' (' + str(len(schuettelbox)+1) + ')' + '_' * (len(token)*2 +1) 
    return (retr_string, token)


def get_positions_of_pos(doc, tags):
    return [i for i in range(len(doc)) if doc[i].pos_ in tags]


def detokenizer(line: List[str]) -> str:
    return "".join(' ' + token if token.isalpha() else token for token in line)[1:]


def remove_adjective_suffix_from_token(token):
    return re.sub(r'(es|er|em|en|e)$', '____', token)


# def remove_pos(file, tags):
#     schuettelbox = []
#     return_line = []
#     with open(file, 'r', encoding='utf-8') as f:
#         for line in f:
#             for token in nlp(line):
#                 if token.pos_ in tags:
#                     blank = erase_token(token.text, schuettelbox)
#                     return_line.append(blank[0])
#                     schuettelbox.append(blank[1])
#                 else:
#                     return_line.append(token.text)
#     return detokenizer(return_line), schuettelbox


file = 'sample_texts/text1.txt'
n = 10


def remove_nth_word(text:List[spacy.tokens.Token], schuettelbox:List[str], n:int=10):
    return_string = []
    token_ctr = 0
    for token in text:
        token_ctr += 1
        if token_ctr >= n and token.is_alpha:
            token_ctr = 0
            blank = erase_token(token.text, schuettelbox)
            return_string.append(blank[0])
            schuettelbox.append(blank[1])
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
            blank = erase_token(token.text, schuettelbox)
            return_string.append(blank[0])
            schuettelbox.append(blank[1])
        else:
            return_string.append(token.text)
    return detokenizer(return_string), schuettelbox


def check(text):
    for token in text:
        print(token.text, token.pos_, sep='\t')

tags = ['NOUN']

# print(remove_pos_new(nlp('Die Katze sitzt auf dem Tisch.')))
# return_line, schuettelbox = remove_pos(file, tags)
# print(return_line)
# print(schuettelbox)

# cloze_test, schuettelbox = remove_nth_word(file, n)
# print (cloze_test)
# print(schuettelbox)

schuettelbox = []
blank_text = []

with open('sample_texts/junk.txt', 'r') as f:
    for line in f:
        text = nlp(line)
        a = remove_nth_word(text, schuettelbox)
        blank_text += [a[0]]
        schuettelbox += a[1]

for paragraph in blank_text:
    print(paragraph)
print(schuettelbox)

schuettelbox = []
blank_text = []

with open('sample_texts/junk.txt', 'r') as f:
    for line in f:
        text = nlp(line)
        a = remove_pos_new(text, schuettelbox, ['ADP'], 0.5)
        blank_text += [a[0]]
        schuettelbox += a[1]

for paragraph in blank_text:
    print(paragraph)
print(schuettelbox)

check(text)

# NOUN, VERB, AUX, ADJ, ADV (noch, jedoch, schon, selten), ADP (präpositionen), DET, SCONJ (dass), CCONJ (und, aber)
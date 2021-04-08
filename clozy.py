import spacy
import re
from typing import Tuple, List

nlp = spacy.load('de_core_news_sm')
adjective_suffixes = {'er', 'e', 'es', 'em', 'en'}


def erase_token(token, schuettelbox):
    retr_string = ' (' + str(len(schuettelbox)+1) + ')' + '_' * (len(token)*2 +1) 
    return (retr_string, token)


def get_positions_of_pos(doc, tags):
    return [i for i in range(len(doc)) if doc[i].pos_ in tags]

def detokenizer(line: List[str]) -> str:
    return "".join(' ' + token if token.isalpha() else token for token in line)[1:]


def remove_pos(file, tags):
    schuettelbox = []
    return_line = []
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            for token in nlp(line):
                if token.pos_ in tags:
                    blank = erase_token(token.text, schuettelbox)
                    return_line.append(blank[0])
                    schuettelbox.append(blank[1])
                else:
                    return_line.append(token.text)
    return detokenizer(return_line), schuettelbox


file = 'sample_texts/text1.txt'
n = 10


def remove_nth_word(line, n):
    return_line = []
    schuettelbox = []
    token_ctr = 0
    for token in nlp(line):
        token_ctr += 1
        if token_ctr >= n and token.is_alpha:
            token_ctr = 0
            blank = erase_token(token.text, schuettelbox)
            return_line.append(blank[0])
            schuettelbox.append(blank[1])
        else:
            return_line.append(token.text)
    return detokenizer(return_line), schuettelbox


def remove_adjective_suffix_from_token(token):
    return re.sub(r'(es|er|em|en|e)$', '____', token)



tags = ['NOUN']

# return_line, schuettelbox = remove_pos(file, tags)
# print(return_line)
# print(schuettelbox)

# cloze_test, schuettelbox = remove_nth_word(file, n)
# print (cloze_test)
# print(schuettelbox)

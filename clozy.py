import spacy
from typing import Tuple

nlp = spacy.load('de_core_news_sm')


def erase_token(token, schuettelbox):
    retr_string = ' (' + str(len(schuettelbox)+1) + ')' + '_' * (len(token)*2 +1) 
    return (retr_string, token)

def enumerate_blanks():
    pass


def remove_pos(file, tags):
    schuettelbox = []
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            for ctr, token in enumerate(nlp(line)):
                print(ctr, token)
                if token.pos_ in tags:
                    a = erase_token()
                    return_line.append(erase_token(token.text, schuettelbox)[0])
                    schuettelbox.append(erase_token(token.text, schuettelbox)[1])
                else:
                    return_line.append(token.text)
    return "".join(' ' + token if token.isalpha() else token for token in return_line), schuettelbox


file = 'sample_texts/text1.txt'
n = 10
return_line = []
# with open('sample_texts/text1.txt', 'r', encoding='utf-8') as file:
#     token_ctr = 0
#     for line in file:
#         for token in nlp(line):
#             token_ctr += 1
#             if token_ctr == n:
#                 token_ctr = 0
#                 return_line.append(erase_token(token.text)[0])
#                 schuettelbox.append(erase_token(token.text)[1])
#             else:
#                 return_line.append(token.text)




tags = ['NOUN']


return_line, schuettelbox = remove_pos(file, tags)
print(return_line)
print(schuettelbox)


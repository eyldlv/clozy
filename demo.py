import spacy
import clozy
from constants import nlp

input('Welcome to the clozy demo. Press any key to continue.')


schuettelbox = []
blank_text = []
print('Clozy can create German fill-in-the-blank texts using a given text file.')
print('Here are some examples.')
print('You can have all words belonging to a certain word class,\
     such as nouns or adjectives, removed.')
print('Here\'s an exmample for removing all the nouns (postag "NOUN").')
input('Press any key.')

with open('sample_texts/text4.txt','r') as infile:
    doc = nlp(infile.read())
    cloze, schuettelbox = clozy.pos_remover(doc, ['NOUN'])

print(cloze)
input('The removed words will be printed after the cloze: (Press any key)')
print(clozy.print_schuettelbox(schuettelbox))
print('This might too many nouns, so you can also limit the percentage of words\
    to be removed:')
input('This is the same text with only 50% of the words removed: (Press any key)')

cloze, schuettelbox = clozy.pos_remover(doc, ['NOUN'], 0.5)
print(cloze)


# clozy v. 0.0.1
# Demo

# Author: Eyal Dolev
# Matricuation number: 20-713-897
# Date: 30.05.2021

import clozy
from constants import nlp

input('Welcome to the clozy demo. Press any key to continue.')


print('Clozy can create German fill-in-the-blank texts using a given text file.')
print('Here are some examples.')

# clozy.pos_remover
print('You can have all words belonging to a certain word class,\
     such as nouns or adjectives, removed.')
print('Here\'s an exmample for removing all the nouns (postag "NOUN").\
using the --pos NOUN flag')
input('Press any key.')

with open('sample_texts/text4.txt','r') as infile:
    doc = nlp(infile.read())
    cloze, schuettelbox = clozy.pos_remover(doc, ['NOUN'])

print(cloze)
input('The removed words will be printed after the cloze: (Press any key)')
print(clozy.print_schuettelbox(schuettelbox))
print('This might too many nouns, so you can also limit the percentage of words\
 to be removed:')
input("This is the same text with only 50% of the words removed using\
--pos NOUN --postpercent 50: (Press any key)")

cloze, schuettelbox = clozy.pos_remover(doc, ['NOUN'], 0.5)
print(cloze)
input("The solution will be printed in the end: (Press any key)")
print(clozy.print_solution(schuettelbox))

# clozy.adj_remover
input("Here's an example for removing adjective suffixes using the flag:\
--adj (Press any key) ")

with open('sample_texts/text2.txt','r') as infile:
    doc = nlp(infile.read())
    cloze, schuettelbox = clozy.adjective_suffix_remover(doc)

print(cloze)
print(clozy.print_solution(schuettelbox))

# clozy.nth_word_remover
input("Finally, you can just have every n-th word removed, for instance \
every 8th word, using the --nth flag (Press any key)")

with open('sample_texts/text1.txt','r') as infile:
    doc = nlp(infile.read())
    cloze, schuettelbox = clozy.nth_word_remover(doc, 8)

print(cloze)
print(clozy.print_schuettelbox(schuettelbox))
print(clozy.print_solution(schuettelbox))

print("Have fun using clozy!")
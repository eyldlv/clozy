import re
from typing import Tuple, List
from random import randint
from spacy.tokens import Token


def erase_token(gap_num:int, gap_length=10) -> str:
    """ Return blank based on token 
    
    args: original token, gap number in the cloze
    for args token="Baum", gap_num=1  returns: "(1)________"
    """
    # return ' (' + str(gap_num) + ')' + '_' * (len(token)*2 +1) 
    return ' (' + str(gap_num) + ')' + '_' * (gap_length) 


def get_positions_of_pos(
        doc:List[Token], tags:List[str]) -> List[int]:
    """ Get the positions of given postags in the text. 
    Required to remove only part of them.
    """
    return [i for i in range(len(doc)) if doc[i].pos_ in tags]


def detokenizer(line: List[str]) -> str:
    """ Concetante list of tokens to one string """
    return "".join(' ' + token if token.isalnum() else token
        for token in line)[1:]


def remove_adja_suffix(token:str, gap_num:int) -> str:
    """Remove suffixes from declined adjectives and return as enumerated blank 
    """
    return ' (' + str(gap_num) + ') ' + \
        re.sub(r'(es|er|em|en|e)$', '____', token) 


def add_blank_to_adjd(token:str, gap_num:int) -> str:
    """Remove suffixes from predicate adjectives and return as enumerated blank
    """
    return ' (' + str(gap_num) + ') ' + token + '____'


def nth_word_remover(
        doc:List[Token], n:int=10) -> Tuple[str, List[str]]:
    return_string = []
    token_ctr = 0
    schuettelbox = []
    for token in doc:
        token_ctr += 1
        if token_ctr >= n and token.is_alpha:
            token_ctr = 0
            return_string.append(erase_token(len(schuettelbox)+1))
            schuettelbox.append(token.text)

        else:
            return_string.append(token.text)

    return detokenizer(return_string), schuettelbox


def pos_remover(
        doc:List[Token], tags:List[str], 
        percentage:int=1) -> Tuple[str, List[str]]:
    """
    Turn a certain postag in the text to blanks. Nouns by default. 
    All words of the same pos will be removed unless a diffrent percentage 
    is given.

    Return a tuple containing the blanked text and a list of strings with the
    removed tokens.
    """
    schuettelbox = []
    return_string = []
    positions = get_positions_of_pos(doc, tags)
    random_positions = [positions.pop(randint(0,len(positions)-1)) 
        for _ in range(round(len(positions)*percentage))]
    for position, token in enumerate(doc):
        if position in random_positions:
            return_string.append(erase_token(len(schuettelbox)+1))
            
            schuettelbox.append(token.text)
        else:
            return_string.append(token.text)

    return detokenizer(return_string), schuettelbox


def adjective_suffix_remover(
        doc:List[Token]) -> Tuple[str, List[str]]:
    """ Remove adjective suffixes from the text. Will also add a blank suffix 
    to undeclined predicate adjectives.
    
    Returns a tuple containing the cloze text and a list of strings with the
    removed tokens.
    """
    return_string = []
    schuettelbox = []
    for token in doc:
        if token.tag_ == 'ADJD':
            return_string.append(add_blank_to_adjd(token.text, 
                len(schuettelbox)+1))
            schuettelbox.append(token.text)
        elif token.tag_ == 'ADJA':
            return_string.append(remove_adja_suffix(token.text, 
                len(schuettelbox)+1))
            schuettelbox.append(token.text)
        else:
            return_string.append(token.text)
    return detokenizer(return_string), schuettelbox


def print_schuettelbox(schuettelbox:List[str]) -> str:
    return_string = '-------------------------------------------------------\n'
    schuettelbox = schuettelbox[:]
    while schuettelbox:
        if len(schuettelbox) > 5:
            return_string += '\t'.join(schuettelbox.pop(
                randint(0,len(schuettelbox)-1)) for _ in range(5)) + '\n'
        else:
            return_string += '\t'.join(schuettelbox.pop(
                randint(0,len(schuettelbox)-1)) for _ in range(
                len(schuettelbox))) + '\n'
    return_string += '-------------------------------------------------------\n'
    return return_string


def print_solution(schuettelbox:List[str]) -> str:
    """ Convert the list of removed tokens to a string for printing.
    """
    return_str = '\nLösung:\n----------------\n'
    return_str += ''.join(f'({position}) {word}\n' for position, 
        word in enumerate(schuettelbox,1))
    return_str += '------------------------------------------------------------'
    
    return return_str


def get_postags(doc:List[Token]):
    postags_dict = {}
    for token in doc:
        if token.pos_ not in ['PUNCT', 'SPACE']:
            if token.pos_ in postags_dict:
                if (len(postags_dict[token.pos_]) < 3 
                    and token.text not in postags_dict[token.pos_]):
                    postags_dict[token.pos_] += [token.text]
            elif token.pos_ not in postags_dict:
                postags_dict[token.pos_] = [token.text] 
    return postags_dict

def main():
    input('Welcome to the clozy demo. Press any key to continue.')
    nlp = spacy.load('de_core_news_sm')

    schuettelbox = []
    blank_text = []
    input('Clozy can create German fill-in-the-blank texts using a given text file.')
    with open('sample_texts/text3.txt', 'r') as f:
        for line in f:
            text = nlp(line)
            a = nth_word_remover(text, schuettelbox, 15)
            blank_text += [a[0]]


    for paragraph in blank_text:
        print(paragraph)
    print_schuettelbox(schuettelbox)



    schuettelbox = []
    blank_text = []

    with open('sample_texts/text3.txt', 'r') as f:
        for line in f:
            text = nlp(line)
            a = pos_remover(text, schuettelbox, ['ADP'], 0.5)
            blank_text += [a[0]]


    for paragraph in blank_text:
        print(paragraph, end='')
    print_schuettelbox(schuettelbox)



    with open ('sample_texts/junk.txt', 'r') as f:
        schuettelbox = []
        blank_text = []
        for line in f:
            text = nlp(line)
            blank, schuettel = adjective_suffix_remover(text, schuettelbox)
            # print(schuettel)
            blank_text += [blank]
            # schuettelbox += schuettel

    for paragraph in blank_text:
        print(paragraph, end='')
    print_schuettelbox(schuettelbox)
    # check(text)

    # NOUN, VERB, AUX, ADJ, ADV (noch, jedoch, schon, selten), ADP (präpositionen), DET, SCONJ (dass), CCONJ (und, aber)

if __name__ == '__main__':
    main()
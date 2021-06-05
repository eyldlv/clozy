# clozy v. 0.0.1
# main module

# Author: Eyal Dolev
# Matricuation number: 20-713-897
# Date: 30.05.2021

import re
from random import randint
from typing import Tuple, List, Dict
from spacy.tokens import Token


def erase_token(gap_num:int, gap_length=10) -> str:
    """ Return enumerated blank 
    
    gap_num: gap number in the cloze for enumeration
    gap_length: optinal length of gap, default: 10
    """
    return ' (' + str(gap_num) + ')' + '_' * (gap_length) 


def get_positions_of_pos(
        doc:List[Token], tags:List[str]) -> List[int]:
    """ Return a list with the positions of the given postags in the text. 
    Required to remove only part of them.
    """
    return [i for i in range(len(doc)) if doc[i].pos_ in tags]


def detokenizer(line: List[str]) -> str:
    """ Concetante list of tokens to one string """
    return "".join(' ' + token if token.isalnum() else token
        for token in line)[1:]


def remove_adja_suffix(token:str, gap_num:int) -> str:
    """Remove suffix from declined adjective and return as enumerated blank 
    """
    return ' (' + str(gap_num) + ') ' + \
        re.sub(r'(es|er|em|en|e)$', '____', token) 


def add_blank_to_adjd(token:str, gap_num:int) -> str:
    """Remove suffix from predicate adjective and return as enumerated blank
    """
    return ' (' + str(gap_num) + ') ' + token + '____'


def nth_word_remover(
        doc:List[Token], n:int=10) -> Tuple[str, List[str]]:
    """ Turn every nth word to a blank. Default is every 10th word. In case 
    the nth word is a punctuation or a number (i.e. not is_alpha), the word will
    skipped and the next valid word will be removed.

    Returns a tuple containing the blanked text and a list of strings with the
    removed tokens.
    """
    return_string = [] 
    schuettelbox = []    
    token_ctr = 0
    for token in doc:
        if token.is_alpha: # count only true words, no numbers of punctuation
            token_ctr += 1
            if token_ctr >= n: 
                token_ctr = 0                     
                return_string.append(erase_token(len(schuettelbox)+1))
                schuettelbox.append(token.text)
            else:
               return_string.append(token.text)  

        else:
            return_string.append(token.text) #appending punctuation

    return detokenizer(return_string), schuettelbox


def pos_remover(
        doc:List[Token], tags:List[str], 
        percentage:int=1) -> Tuple[str, List[str]]:
    """
    Turn given postags to blanks. All words of the given postags will be removed
    unless a diffrent percentage is given.

    Returns a tuple containing the blanked text and a list of strings with the
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
    to undeclined predicate adjectives. (e.g. 'Der Baum ist schön___.')
    
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
    """ Return a pretty string with the words removed for crating in blanks, but
    in randomized order.
    """
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
    """ Convert the list of removed tokens to a string for pretty printing.
    """
    return_str = '\nLösung:\n----------------\n'
    return_str += ''.join(f'({position}) {word}\n' for position, 
        word in enumerate(schuettelbox,1))
    return_str += '------------------------------------------------------------'
    
    return return_str


def get_postags(doc:List[Token]) -> Dict[str, List[str]]:
    """ Inspect a text and return a dictionary with up to 5 words per postag.
    """
    postags_dict = {}
    for token in doc:
        if token.pos_ not in ['PUNCT', 'SPACE']:
            if token.pos_ in postags_dict:
                if (len(postags_dict[token.pos_]) < 5 
                    and token.text not in postags_dict[token.pos_]):
                    postags_dict[token.pos_] += [token.text]
            elif token.pos_ not in postags_dict:
                postags_dict[token.pos_] = [token.text] 
    return postags_dict
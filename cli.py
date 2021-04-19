import argparse
from clozy import nth_word_remover, adjective_suffix_remover, pos_remover
from clozy import print_schuettelbox
import spacy


def get_arguments():
    parser = argparse.ArgumentParser("CLI for clozy, script for creating cloze texts.")
    parser.add_argument("file", type=argparse.FileType('r', encoding='utf-8'), 
                        nargs='+')
    parser.add_argument('--nth', '-n', type=int, nargs='?', action='store', 
                        const=10,
                        help="Remove every n-th word. Default is 10.")
    parser.add_argument('--adj', action='store_true', 
                        help='Remove adjective suffixes.')
    parser.add_argument('--pos', type=str, nargs='*', default=['NOUN'],
                        help='Remove words with pos tag.')
    parser.add_argument('--pospercent', type=int, 
                        help='When defined, limit pos-tag removal to x percent.\
                        e.g. --pos ADJ --pospercent 50 will randomly \
                        remove 50% of all adjectives.')
    args = parser.parse_args()
    return args




def main():
    args = get_arguments()
    nlp = spacy.load('de_core_news_sm')

    for file in args.file:
        
        schuettelbox = []


        for line in file:
            text = nlp(line)
            if args.nth:
                print(nth_word_remover(text, schuettelbox, args.nth)[0], end='')
                print('\n')
                
    print(print_schuettelbox(schuettelbox))



if __name__ == '__main__':
    main()


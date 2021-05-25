import argparse
import clozy
import spacy
import sys


def get_arguments():
    parser = argparse.ArgumentParser("CLI for clozy, script for creating cloze texts.")
    parser.add_argument("file", type=argparse.FileType('r', encoding='utf-8'), 
                        nargs='+')
    parser.add_argument('--outfile', nargs='?', const='output.txt', action='store', 
                        help='Store output to file. Filename is optional. \
                              Default ist "output.txt"')
    parser.add_argument('--nth', '-n', type=int, nargs='?', action='store', 
                        const=10,
                        help="Remove every n-th word. Default is 10.")
    parser.add_argument('--adj', action='store_true', 
                        help='Remove adjective suffixes.')
    parser.add_argument('--pos', type=str, nargs='*', default=['NOUN'],
                        help='Remove words with pos tag.')
    parser.add_argument('--pospercent', type=int, default=100,
                        help='When defined, limit pos-tag removal to x percent.\
                        e.g. --pos ADJ --pospercent 50 will randomly \
                        remove 50% of all adjectives.')
    parser.add_argument('--poslist', action='store_true', 
                        help='Print available parts-of-speech for given file.')
    
    args = parser.parse_args()
    return args


def main():
    args = get_arguments()
    nlp = spacy.load('de_core_news_sm')

    if args.outfile:
        sys.stdout = open(args.outfile, 'w', encoding='utf-8')

    for file in args.file:
        
        schuettelbox = []

        for line in file:
            text = nlp(line)

            if args.nth:
                print(clozy.nth_word_remover(text, schuettelbox, args.nth)[0], end='')
                print('\n')
            
            elif args.adj:
                print(clozy.adjective_suffix_remover(text, schuettelbox)[0], end='')
            
            elif args.pos:
                print(clozy.pos_remover(text, schuettelbox, args.pos, args.pospercent/100)[0], end='')
    
        print(clozy.print_schuettelbox(schuettelbox))
        



if __name__ == '__main__':
    main()


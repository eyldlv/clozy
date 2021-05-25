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
    parser.add_argument('--pos', type=str, nargs='+', 
                        help='Remove words with supplied pos tag. Run with \
                              --poslist to see available part-of-speech tags.')
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
    if sum(1 for arg in (args.pos, args.adj, args.nth) if arg) > 1:
        print('Too many arguments given. Please choose either --pos, --adj or --nth.')
        sys.exit()

    nlp = spacy.load('de_core_news_sm')
    
    if args.outfile:
        sys.stdout = open(args.outfile, 'w', encoding='utf-8')

    for file in args.file:
        
        schuettelbox = []
        clozed_text = ''

        for line in file:
            text = nlp(line)

            if args.poslist:
                postags = clozy.get_postags(text)

            elif args.nth:
                tup = clozy.nth_word_remover(text, schuettelbox, args.nth)
                clozed_text += tup[0]
                schuettelbox = tup[1]

            elif args.adj:
                tup = clozy.adjective_suffix_remover(text, schuettelbox)
                clozed_text += tup[0]
                schuettelbox = tup[1]
            
            elif args.pos:
                
                tup = clozy.pos_remover(text, schuettelbox, args.pos, args.pospercent/100)
                clozed_text += tup[0]
                schuettelbox = tup[1]
                
    
        print(clozed_text)
        print(clozy.print_schuettelbox(schuettelbox))


if __name__ == '__main__':
    main()
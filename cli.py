import argparse
import clozy
import spacy
import sys


def get_arguments():
    parser = argparse.ArgumentParser(
            "CLI for clozy, script for creating cloze texts.")
    parser.add_argument("file", type=argparse.FileType('r', encoding='utf-8'), 
                        nargs='+', 
                        help='Text file(s) to be used for creating the cloze.')
    parser.add_argument('--outfile', nargs='?', const='output.txt', 
                        action='store', 
                        help='Store output to file. Filename optional. \
                              Default: output.txt')
    parser.add_argument('--nth', '-n', type=int, nargs='?', action='store', 
                        const=10,
                        help="Remove every n-th word. Default: 10.")
    parser.add_argument('--adj', action='store_true', 
                        help='Remove adjective suffixes.')
    parser.add_argument('--pos', type=str, nargs='+', 
                        help='Remove all words with supplied pos-tag. Use \
                              "--poslist" to see available part-of-speech tags\
                              for the supplied files.')
    parser.add_argument('--pospercent', type=int, default=100,
                        help='When defined, limit pos-tag removal to x percent.\
                        e.g. --pos ADJ --pospercent 50 will randomly \
                        remove 50 percent of all adjectives.')
    parser.add_argument('--poslist', action='store_true', 
                        help='Print available parts-of-speech for the supplied\
                             file(s).')
    
    args = parser.parse_args()
    return args


def main():
    args = get_arguments()
    if not any([args.poslist, args.pos, args.adj, args.nth]):
        print('No action chosen. Please rerun with -h for help.')
        sys.exit()

    nlp = spacy.load('de_core_news_sm')    
    if args.outfile:
        sys.stdout = open(args.outfile, 'w', encoding='utf-8')

    for file in args.file:        
        text = nlp(file.read())
        if args.poslist:
            postags = clozy.get_postags(text)
            for postag, words in postags.items():
                for word in words:
                    print(word, end=', ')
                print(': ', end='')
                print(postag)
                
        if args.nth:
            clozed_text, schuettelbox = clozy.nth_word_remover(text, args.nth)
            print(clozed_text)
            print(clozy.print_schuettelbox(schuettelbox))
            
        if args.adj:
            clozed_text, schuettelbox = clozy.adjective_suffix_remover(text)
            print(clozed_text)
            print(clozy.print_schuettelbox(schuettelbox))

        if args.pos:
            clozed_text, schuettelbox = clozy.pos_remover(text, args.pos, 
                args.pospercent/100)
            print(clozed_text)
            print(clozy.print_schuettelbox(schuettelbox))

if __name__ == '__main__':
    main()
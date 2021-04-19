import argparse

def get_arguments():
    parser = argparse.ArgumentParser("CLI for clozy, script for creating cloze texts.")
    parser.add_argument("file", type=argparse.FileType('r', encoding='utf-8'), 
                        nargs='*')
    parser.add_argument('--nth', '-n', type=int, default=10, 
                        help="Remove every n-th word. Default is 10.")
    parser.add_argument('--adj', type=bool, action='store_true', 
                        help='Remove adjective suffixes.')
    parser.add_argument('--pos', type=str, nargs='*', default=['NOUN'],
                        help='Remove words with pos tag.')
    parser.add_argument('--pospercent', type=int, 
                        help='When defined, limit pos-tag removal to x percent.\
                        e.g. --pos ADJ --pospercent 50 will randomly \
                        remove 50% of all adjectives.')


def main():
    pass

if __name__ == 'main':
    main()


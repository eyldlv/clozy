from unittest import TestCase, main
import clozy
import spacy
from constants import nlp


class ClozyTest(TestCase):

    def test_get_postags(self):
        sentence = nlp('Äpfel sind lecker, aber Bananen sind gelb.')
        result = clozy.get_postags(sentence)
        self.assertEqual({'NOUN' : ['Äpfel', 'Bananen'],
                          'AUX' : ['sind'],
                          'ADJ'  : ['lecker', 'gelb'],
                          'CCONJ' : ['aber']}, result)

    def test_erase_token(self):
        result = clozy.erase_token(1)
        self.assertEqual( (' (1)__________'), result, "erase_token doesn't work properly")


    def test_remove_adja_suffix(self):
        token = 'schöner'
        result = clozy.remove_adja_suffix(token, 1)
        self.assertEqual(' (1) schön____', result)
        token = 'schöne'
        result = clozy.remove_adja_suffix(token, 1)
        self.assertEqual(' (1) schön____', result)
        token = 'schönes'
        result = clozy.remove_adja_suffix(token, 1)
        self.assertEqual(' (1) schön____', result)
        token = 'schönem'
        result = clozy.remove_adja_suffix(token, 1)
        self.assertEqual(' (1) schön____', result)
        token = 'schönen'
        result = clozy.remove_adja_suffix(token, 1)
        self.assertEqual(' (1) schön____', result)
    
    def test_add_blank_to_adjd(self):
        token = 'schön'
        result = clozy.add_blank_to_adjd(token, 1)
        self.assertEqual(' (1) schön____', result)


    def test_nth_word(self):
        text = nlp('Auf einem Baum saß ein alter Hahn.')
        result = clozy.nth_word_remover(text, 4)
        self.assertEqual(('Auf einem Baum (1)__________ ein alter Hahn.', ['saß']), result)

        text = nlp('Ich will. Nach Hause.')
        result = clozy.nth_word_remover(text, 3)
        self.assertEqual(('Ich will. (1)__________ Hause.', ['Nach']), result, 'If word is a punctuation mark or a number it should be skipped.')
    
    def test_get_positions_of_pos(self):
        text = nlp('Auf einem Baum saß ein alter Hahn.')
        result = clozy.get_positions_of_pos(text, ['NOUN'])
        self.assertEqual([2, 6], result)

    
    def test_pos_remover(self):
        text = nlp('Auf einem Baum saß ein alter Hahn.')
        result = clozy.pos_remover(text, ['NOUN'])
        self.assertEqual(('Auf einem (1)__________ saß ein alter (2)__________.', ['Baum', 'Hahn']), result)
        
        # Check that only half of the words gets deleted
        text = nlp('Die Katze sitzt auf dem Tisch.')
        result = clozy.pos_remover(text, ['NOUN'], 0.5)[0]
        possible_results = ['Die (1)__________ sitzt auf dem Tisch.', 'Die Katze sitzt auf dem (1)__________.']
        self.assertTrue(result in possible_results)


    def test_print_schuettelbox(self):
        # testing a random function
        schuettelbox = ['Apfel', 'Baum', 'ist', 'Zucker', 'Tag']
        result = clozy.print_schuettelbox(schuettelbox)
        for word in schuettelbox:
            self.assertIn(word, result, f'{word} is missing.')
    
    def test_print_solution(self):
        schuettelbox = ['Apfel', 'Baum', 'ist']
        result = clozy.print_solution(schuettelbox)
        self.assertEqual('\nLösung:\n----------------\n(1) Apfel\n(2) Baum\n(3) ist\n------------------------------------------------------------', result)

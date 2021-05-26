from unittest import TestCase, main
import clozy
import spacy

nlp = spacy.load('de_core_news_sm')

class ClozyTest(TestCase):

    def test_get_postags(self):
        sentence = nlp('Äpfel sind lecker, aber Bananen sind gelb.')
        result = clozy.get_postags(sentence)
        self.assertEqual({'NOUN' : ['Äpfel', 'Bananen'],
                          'AUX' : ['sind'],
                          'ADV'  : ['lecker', 'gelb'],
                          'CCONJ' : ['aber']}, result)

    def test_erase_token(self):
        
        token = 'Baum'
        result = clozy.erase_token(token, [])
        self.assertEqual( (' (1)_________'), result, "erase_token doesn't work properly")


    def test_remove_adja_suffix(self):
        token = 'schöner'
        result = clozy.remove_adja_suffix(token, [])
        self.assertEqual(' (1) schön____', result)
        token = 'schöne'
        result = clozy.remove_adja_suffix(token, [])
        self.assertEqual(' (1) schön____', result)
        token = 'schönes'
        result = clozy.remove_adja_suffix(token, [])
        self.assertEqual(' (1) schön____', result)
        token = 'schönem'
        result = clozy.remove_adja_suffix(token, [])
        self.assertEqual(' (1) schön____', result)
        token = 'schönen'
        result = clozy.remove_adja_suffix(token, [])
        self.assertEqual(' (1) schön____', result)
    
    def test_add_blank_to_adjd(self):
        token = 'schön'
        result = clozy.add_blank_to_adjd(token, [])
        self.assertEqual(' (1) schön____', result)


    def test_nth_word(self):
        text = nlp('Auf einem Baum saß ein alter Hahn.')
        result = clozy.nth_word_remover(text, [], 4)
        self.assertEqual(('Auf einem Baum (1)_______ ein alter Hahn.', ['saß']), result)

        text = nlp('Ich will. Nach Hause.')
        result = clozy.nth_word_remover(text, [], 3)
        self.assertEqual(('Ich will. (1)_________ Hause.', ['Nach']), result, 'If word is a punctuation mark or a number it should be skipped.')
    
    def test_get_positions_of_pos(self):
        text = nlp('Auf einem Baum saß ein alter Hahn.')
        result = clozy.get_positions_of_pos(text, ['NOUN'])
        self.assertEqual([2, 6], result)

    
    def test_pos_new(self):
        text = nlp('Auf einem Baum saß ein alter Hahn.')
        result = clozy.pos_remover(text, [])
        self.assertEqual(('Auf einem (1)_________ saß ein alter (2)_________.', ['Baum', 'Hahn']), result)
        
        # Check that only half of the words gets deleted
        text = nlp('Die Katze sitzt auf dem Tisch.')
        result = clozy.pos_remover(text, [], ['NOUN'], 0.5)[0]
        possible_results = ['Die (1)___________ sitzt auf dem Tisch.', 'Die Katze sitzt auf dem (1)___________.']
        self.assertTrue(result in possible_results)
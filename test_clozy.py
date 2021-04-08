from unittest import TestCase, main
import clozy

class ClozyTest(TestCase):

    def test_erase_token(self):
        
        token = 'Baum'
        result = clozy.erase_token(token, [])
        self.assertEqual( (' (1)_________', 'Baum'), result, "erase_token doesn't work properly")

    def test_remove_adjective_suffix(self):
        token = 'schöner'
        result = clozy.remove_adjective_suffix_from_token(token)
        self.assertEqual('schön____', result, 'adjective suffix doesnt work')
        token = 'schönes'
        result = clozy.remove_adjective_suffix_from_token(token)
        self.assertEqual('schön____', result, 'adjective suffix doesnt work')
        token = 'schönem'
        result = clozy.remove_adjective_suffix_from_token(token)
        self.assertEqual('schön____', result, 'adjective suffix doesnt work')
        token = 'schönen'
        result = clozy.remove_adjective_suffix_from_token(token)
        self.assertEqual('schön____', result, 'adjective suffix doesnt work')
        token = 'schöne'
        result = clozy.remove_adjective_suffix_from_token(token)
        self.assertEqual('schön____', result, 'adjective suffix doesnt work')

    def test_nth_word(self):
        text = 'Auf einem Baum saß ein alter Hahn.'
        result = clozy.remove_nth_word(text, 4)[0]
        self.assertEqual('Auf einem Baum (1)_______ ein alter Hahn.', result)

        text = 'Ich will. Nach Hause.'
        result = clozy.remove_nth_word(text, 3)[0]
        self.assertEqual('Ich will. (1)_________ Hause.', result, 'If word is a punctuation mark or a number it should be skipped.')
    
    def test_get_positions_of_pos(self):
        text = clozy.nlp('Auf einem Baum saß ein alter Hahn.')
        result = clozy.get_positions_of_pos(text, ['NOUN'])
        self.assertEqual([2, 6], result)
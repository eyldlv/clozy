from unittest import TestCase, main
import clozy

class ClozyTest(TestCase):

    # def test_erase_token(self):
    #     token = 'Baum'
    #     result = clozy.erase_token(token)
    #     self.assertEqual( ('_________', 'Baum'), result, "erase_token doesn't work properly")

    def test_remove_adjective_suffix(self):
        token = 'schöner'
        result = clozy.remove_adjective_suffix(token)
        self.assertEqual('schön____', result, 'adjective suffix doesnt work')
        token = 'schönes'
        result = clozy.remove_adjective_suffix(token)
        self.assertEqual('schön____', result, 'adjective suffix doesnt work')
        token = 'schönem'
        result = clozy.remove_adjective_suffix(token)
        self.assertEqual('schön____', result, 'adjective suffix doesnt work')
        token = 'schönen'
        result = clozy.remove_adjective_suffix(token)
        self.assertEqual('schön____', result, 'adjective suffix doesnt work')
        token = 'schöne'
        result = clozy.remove_adjective_suffix(token)
        self.assertEqual('schön____', result, 'adjective suffix doesnt work')
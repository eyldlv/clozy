from unittest import TestCase, main
import clozy

class ClozyTest(TestCase):

    def test_erase_token(self):
        token = 'Baum'
        result = clozy.erase_token(token)
        self.assertEqual( ('_________', 'Baum'), result, "erase_token doesn't work properly")
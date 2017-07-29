import unittest
from lib.session import HashSession


class TestHashSessions(unittest.TestCase):
    def setUp(self):
        self.session = HashSession()
    
    def test_get_set_item(self):
        
        key = self.session.gen_key()
        data = {
            'login': 'Mikhalych',
            'email': 'mikh@mail.org',
            'access': '1'
        }
        self.session[key] = data
        result = self.session[key]
        print(self.assertEqual(data, result))

    def test_gen_key_len(self):
        key = HashSession.gen_key()
        self.assertEqual(len(key), 64)

    def test_gen_key_is_hex(self):
        key = HashSession.gen_key()
        try:
            int(key, 16)
        except ValueError:
            self.fail(f'The key "{key}" is not hexidecimal')
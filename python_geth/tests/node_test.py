import unittest


class TestTruffleTemplate(unittest.TestCase):
    def setUp(self):
        """Call before every test case."""
        self.truffle_config_f = open("../templates/truffle-config.txt", "r")
        self.truffle_config = self.truffle_config_f.read()

    def tearDown(self):
        """Call after every test case."""
        self.truffle_config_f.close()

    def testPort(self):
        "Check if there is the PORT option"
        assert self.truffle_config.replace('<PORT>', 'Found it')

    def testFrom(self):
        "Check if there is the From option"
        assert self.truffle_config.replace('<FROM>', 'Found it')


if __name__ == '__main__':
    unittest.main()

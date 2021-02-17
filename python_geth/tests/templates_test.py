import json
import os.path as path
import unittest


class TestTruffleTemplate(unittest.TestCase):
    def setUp(self):
        """Call before every test case."""
        text_file_path = path.dirname(path.abspath(__file__)) + '/../templates/truffle-config.txt'
        self.truffle_config_f = open(text_file_path, "r")
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


class TestGenesis(unittest.TestCase):
    def setUp(self):
        """Call before every test case."""
        text_file_path = path.dirname(path.abspath(__file__)) + '/../templates/genesis.json'
        self.genesis_f = open(text_file_path, "r")
        self.genesis = self.genesis_f.read()

    def tearDown(self):
        """Call after every test case."""
        self.genesis_f.close()

    def testFrom(self):
        "Check if the json of genesis is as should"
        string_genesis = "{  \"nonce\": \"0x0000000000000042\",  \"timestamp\": \"0x0\",  \"parentHash\": " \
                         "\"0x0000000000000000000000000000000000000000000000000000000000000000\",  \"extraData\": " \
                         "\"0x00\",  \"gasLimit\": \"0x8000000\",  \"difficulty\": \"0x400\",  \"mixhash\": " \
                         "\"0x0000000000000000000000000000000000000000000000000000000000000000\",  \"coinbase\": " \
                         "\"0x3333333333333333333333333333333333333333\",  \"alloc\": {},  \"config\": {    " \
                         "\"chainId\": 4777,    \"homesteadBlock\": 0,    \"eip150Block\": 0," \
                         "    \"eip150Hash\": " \
                         "\"0x0000000000000000000000000000000000000000000000000000000000000000\"," \
                         "    \"eip155Block\": 0,    \"eip158Block\": 0,    \"byzantiumBlock\": 0," \
                         "    \"constantinopleBlock\": 0,    \"petersburgBlock\": 0,    \"ethash\": {}, " \
                         "\"isQuorum\": true," \
                         "\"maxCodeSize\": 128," \
                         "\"txnSizeLimit\": 128  }} "

        assert json.loads(self.genesis) == json.loads(string_genesis)


if __name__ == '__main__':
    unittest.main()

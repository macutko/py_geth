import os
import unittest

from python_geth.node import Node


class TestNodeClass(unittest.TestCase):
    def setUp(self):
        """Call before every test case."""
        self.node = Node(datadir="node01_test", port=30303, rpcport=8000, name="Node01")
        self.node.start_node()

    def tearDown(self):
        """Call after every test case."""
        self.node.stop_node()
        os.system('rm -rf node01_test')

    def testW3(self):
        assert self.node.w3.isConnected()


if __name__ == '__main__':
    unittest.main()

import unittest

from python_geth.tests import templates_test, node_test


def test_suite():
    """Add all your tests here"""
    suite = unittest.TestLoader().loadTestsFromModule(templates_test)
    suite.addTests(unittest.TestLoader().loadTestsFromModule(node_test))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(test_suite())

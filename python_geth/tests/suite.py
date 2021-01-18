import unittest

from python_geth.tests import templates_test


def test_suite():
    suite = unittest.TestLoader().loadTestsFromModule(templates_test)
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(test_suite())

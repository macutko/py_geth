import unittest

from python_geth.tests import templates_test

def test_suite():
    suite = unittest.TestLoader().loadTestsFromModule(templates_test)
    unittest.TextTestRunner(verbosity=2).run(suite)
    return suite

if __name__ == "__main__":


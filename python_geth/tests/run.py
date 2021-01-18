import unittest

from python_geth.tests import templates_test

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromModule(templates_test)
    unittest.TextTestRunner(verbosity=2).run(suite)

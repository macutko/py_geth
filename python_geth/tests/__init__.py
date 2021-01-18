# implement a basic test under somepackage.tests

from python_geth.tests.suite import test_suite


def get_suite():
    """Return a unittest.TestSuite."""
    return test_suite()

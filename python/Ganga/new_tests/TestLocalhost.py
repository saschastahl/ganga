# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestLocalhost(unittest.TestCase):
    """
    Test the Localhost objects
    """

    def test_create_localhost(self):
        """
        Check you can create a Localhost object
        """
        from Ganga.Lib.Localhost.Localhost import Localhost
        e = Localhost()
        self.assertIsInstance(e, Localhost)
# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestIBackend(unittest.TestCase):
    """
    Test the IBackend object
    """

    def test_create_ibackend(self):
        """
        Check you can create a IBackend object
        """
        from Ganga.GPIDev.Adapters.IBackend import IBackend
        a = IBackend()
        self.assertIsInstance(a, IBackend)
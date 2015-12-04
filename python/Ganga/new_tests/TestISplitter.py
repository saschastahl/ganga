# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestSplitter(unittest.TestCase):
    """
    Test the ISplitter object
    """

    def test_create_splittingerror(self):
        """
        Check you can create a SplittingError object
        """
        from Ganga.GPIDev.Adapters.ISplitter import SplittingError
        a = SplittingError("TestMessage")
        self.assertIsInstance(a, SplittingError)

    def test_create_isplitter(self):
        """
        Check you can create a ISplitter object
        """
        from Ganga.GPIDev.Adapters.ISplitter import ISplitter
        a = ISplitter()
        self.assertIsInstance(a, ISplitter)
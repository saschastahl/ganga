# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestIChecker(unittest.TestCase):
    """
    Test the IBackend object
    """

    def test_create_ichecker(self):
        """
        Check you can create a IChecker object
        """
        from Ganga.GPIDev.Adapters.IChecker import IChecker
        a = IChecker()
        self.assertIsInstance(a, IChecker)

    def test_create_ifilechecker(self):
        """
        Check you can create a IChecker object
        """
        from Ganga.GPIDev.Adapters.IChecker import IFileChecker
        a = IFileChecker()
        self.assertIsInstance(a, IFileChecker)
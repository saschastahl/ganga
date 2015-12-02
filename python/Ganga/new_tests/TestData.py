# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestData(unittest.TestCase):
    """
    Test the Data objects
    """

    def test_create_duplicatedataitemerror(self):
        """
        Check you can create a DuplicateDataItemError object
        """
        from Ganga.Core.GangaThread.MTRunner.Data import DuplicateDataItemError
        e = DuplicateDataItemError("My Error")
        self.assertIsInstance(e, DuplicateDataItemError)

    def test_create_data(self):
        """
        Check you can create a Data object
        """
        from Ganga.Core.GangaThread.MTRunner.Data import Data
        e = Data()
        self.assertIsInstance(e, Data)
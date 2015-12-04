# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestIMerger(unittest.TestCase):
    """
    Test the IMerger object
    """

    # TODO: Needs config up and running to do a test
    # def test_create_imerger(self):
    #     """
    #     Check you can create a IMerger object
    #     """
    #     from Ganga.GPIDev.Adapters.IMerger import IMerger
    #     a = IMerger()
    #     self.assertIsInstance(a, IMerger)

# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestGangaList(unittest.TestCase):
    """
    Test the GangaList objects
    """

    def test_create_gangalist(self):
        """
        Check you can create a GangaList object
        """
        from Ganga.GPIDev.Lib.GangaList.GangaList import GangaList
        e = GangaList()
        self.assertIsInstance(e, GangaList)

    def test_create_gangalistiter(self):
        """
        Check you can create a GangaListIter object
        """
        from Ganga.GPIDev.Lib.GangaList.GangaList import GangaListIter
        e = GangaListIter("iter")
        self.assertIsInstance(e, GangaListIter)
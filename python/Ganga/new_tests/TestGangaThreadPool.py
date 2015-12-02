# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestGangaThreadPool(unittest.TestCase):
    """
    Test the GangaThreadPool object
    """

    def test_create_gangathreadpool(self):
        """
        Check you can create a GangaThread object
        """
        from Ganga.Core.GangaThread.GangaThreadPool import GangaThreadPool
        a = GangaThreadPool()
        self.assertIsInstance(a, GangaThreadPool)
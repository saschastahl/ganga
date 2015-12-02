# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestGangaThread(unittest.TestCase):
    """
    Test the GangaThread object
    """

    def test_create_gangathread(self):
        """
        Check you can create a GangaThread object
        """
        from Ganga.Core.GangaThread.GangaThread import GangaThread
        a = GangaThread("TestThread")
        self.assertIsInstance(a, GangaThread)
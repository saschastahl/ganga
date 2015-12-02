# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestVStreamer(unittest.TestCase):
    """
    Test the VStreamer objects
    """

    def test_create_vstreamer(self):
        """
        Check you can create a GangaList object
        """
        from Ganga.Core.GangaRepository.VStreamer import VStreamer
        e = VStreamer()
        self.assertIsInstance(e, VStreamer)

    def test_create_emptygangaobject(self):
        """
        Check you can create a EmptyGangaObject object
        """
        from Ganga.Core.GangaRepository.VStreamer import EmptyGangaObject
        e = EmptyGangaObject()
        self.assertIsInstance(e, EmptyGangaObject)

    def test_create_loader(self):
        """
        Check you can create a Loader object
        """
        from Ganga.Core.GangaRepository.VStreamer import Loader
        e = Loader()
        self.assertIsInstance(e, Loader)

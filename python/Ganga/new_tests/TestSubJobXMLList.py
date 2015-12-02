# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestSubJobXMLList(unittest.TestCase):
    """
    Test the SessionLockRefresher module
    """

    def test_create_sjxliterator(self):
        """
        Check you can create a SJXLIterator object
        """
        from Ganga.Core.GangaRepository.SubJobXMLList import SJXLIterator
        e = SJXLIterator([])

        self.assertIsInstance(e, SJXLIterator)

    def test_create_subjobxmllist(self):
        """
        Check you can create a SubJobXMLList object
        """
        from Ganga.Core.GangaRepository.SubJobXMLList import SubJobXMLList
        e = SubJobXMLList()

        self.assertIsInstance(e, SubJobXMLList)


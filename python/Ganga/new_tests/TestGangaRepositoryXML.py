# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestGangaRepositoryXML(unittest.TestCase):
    """
    Test the GangaRepositoryXML objects
    """

    # TODO: needs a functional registry to work properly
    # def test_create_repositoryxml(self):
    #     """
    #     Check you can create a GangaRepositoryLocal object
    #     """
    #     from Ganga.Core.GangaRepository.GangaRepositoryXML import GangaRepositoryLocal
    #     e = GangaRepositoryLocal("TestRepository")
    #     self.assertIsInstance(e, GangaRepositoryLocal)
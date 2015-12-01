# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestGangaRepositorySQLite(unittest.TestCase):
    """
    Test the GangaRepositorySQLite objects
    """

    def test_create_repositorysqlite(self):
        """
        Check you can create a GangaRepositorySQLite object
        """
        from Ganga.Core.GangaRepository.GangaRepositorySQLite import GangaRepositorySQLite
        e = GangaRepositorySQLite("TestRepository")
        self.assertIsInstance(e, GangaRepositorySQLite)
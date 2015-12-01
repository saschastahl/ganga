# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestGangaRepository(unittest.TestCase):
    """
    Test the GangaRepository objects
    """

    def test_create_schemaversionerror(self):
        """
        Check you can create a SchemaVersionError object
        """
        from Ganga.Core.GangaRepository.GangaRepository import SchemaVersionError
        e = SchemaVersionError()
        self.assertIsInstance(e, SchemaVersionError)

    def test_create_inaccessibleobjecterror(self):
        """
        Check you can create a InaccessibleObjectError object
        """
        from Ganga.Core.GangaRepository.GangaRepository import InaccessibleObjectError
        e = InaccessibleObjectError()
        self.assertIsInstance(e, InaccessibleObjectError)

    # def test_create_repositoryerror(self):
    #     """
    #     Check you can create a RepositoryError object
    #     """
    #     from Ganga.Core.GangaRepository.GangaRepository import RepositoryError, GangaRepository
    #     e = RepositoryError(GangaRepository("TestRepository"), "TestRepoError")
    #     self.assertIsInstance(e, RepositoryError)

    def test_create_gangarepository(self):
        """
        Check you can create a GangaRepository object
        """
        from Ganga.Core.GangaRepository.GangaRepository import GangaRepository
        e = GangaRepository("TestRepository")
        self.assertIsInstance(e, GangaRepository)

    def test_create_gangarepositorytransient(self):
        """
        Check you can create a GangaRepositoryTransient object
        """
        from Ganga.Core.GangaRepository.GangaRepository import GangaRepositoryTransient
        e = GangaRepositoryTransient()
        self.assertIsInstance(e, GangaRepositoryTransient)
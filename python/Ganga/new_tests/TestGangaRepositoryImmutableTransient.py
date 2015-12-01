# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestGangaRepositoryImmutableTransient(unittest.TestCase):
    """
    Test the GangaRepository objects
    """

    def test_create_repoimmutabletransient(self):
        """
        Check you can create a GangaRepositoryImmutableTransient object
        """
        from Ganga.Core.GangaRepository.GangaRepositoryImmutableTransient import GangaRepositoryImmutableTransient
        e = GangaRepositoryImmutableTransient("TestRepository", ".txt")
        self.assertIsInstance(e, GangaRepositoryImmutableTransient)
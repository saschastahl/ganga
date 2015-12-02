# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestAlgorithm(unittest.TestCase):
    """
    Test the Algorithm objects
    """

    def test_create_algorithmerror(self):
        """
        Check you can create a Algorithm object
        """
        from Ganga.Core.GangaThread.MTRunner.Algorithm import AlgorithmError
        e = AlgorithmError("My Error")
        self.assertIsInstance(e, AlgorithmError)

    def test_create_algorithm(self):
        """
        Check you can create a Algorithm object
        """
        from Ganga.Core.GangaThread.MTRunner.Algorithm import Algorithm
        e = Algorithm()
        self.assertIsInstance(e, Algorithm)
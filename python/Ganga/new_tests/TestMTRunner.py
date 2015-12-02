# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestMTRunner(unittest.TestCase):
    """
    Test the MTRunner objects
    """

    def test_create_mtrunnererror(self):
        """
        Check you can create a MTRunnerError object
        """
        from Ganga.Core.GangaThread.MTRunner.MTRunner import MTRunnerError
        e = MTRunnerError("My Error")
        self.assertIsInstance(e, MTRunnerError)

    def test_create_gangaworkagent(self):
        """
        Check you can create a GangaWorkAgent object
        """
        from Ganga.Core.GangaThread.MTRunner.MTRunner import GangaWorkAgent
        e = GangaWorkAgent("runner_obj", "TestWorkAgent")
        self.assertIsInstance(e, GangaWorkAgent)

    def test_create_mtrunner(self):
        """
        Check you can create a MTRunner object
        """
        from Ganga.Core.GangaThread.MTRunner.MTRunner import MTRunner
        from Ganga.Core.GangaThread.MTRunner.Algorithm import Algorithm
        e = MTRunner("TestMTRunner", algorithm=Algorithm(), data = [1, 2])
        self.assertIsInstance(e, MTRunner)
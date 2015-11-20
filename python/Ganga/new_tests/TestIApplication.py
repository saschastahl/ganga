# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestIApplication(unittest.TestCase):
    """
    Test the IApplication object
    """

    def test_create_iapplication(self):
        """
        Check you can create a IApplication object
        """
        from Ganga.GPIDev.Adapters.IApplication import IApplication
        a = IApplication()
        self.assertIsInstance(a, IApplication)

    def test_create_postprocessorstatusupdate(self):
        """
        Check you can create a PostprocessStatusUpdate object
        """
        from Ganga.GPIDev.Adapters.IApplication import PostprocessStatusUpdate
        a = PostprocessStatusUpdate("TestStatus")
        self.assertIsInstance(a, PostprocessStatusUpdate)
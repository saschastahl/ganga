# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestIPostProcessor(unittest.TestCase):
    """
    Test the IPostProcessor object
    """

    def test_create_postprocessexception(self):
        """
        Check you can create a PostProcessException object
        """
        from Ganga.GPIDev.Adapters.IPostProcessor import PostProcessException
        a = PostProcessException()
        self.assertIsInstance(a, PostProcessException)

    def test_create_iprepareapp(self):
        """
        Check you can create a IPostProcessor object
        """
        from Ganga.GPIDev.Adapters.IPostProcessor import IPostProcessor
        a = IPostProcessor()
        self.assertIsInstance(a, IPostProcessor)

    def test_create_multipostprocessor(self):
        """
        Check you can create a MultiPostProcessor object
        """
        from Ganga.GPIDev.Adapters.IPostProcessor import MultiPostProcessor
        a = MultiPostProcessor()
        self.assertIsInstance(a, MultiPostProcessor)
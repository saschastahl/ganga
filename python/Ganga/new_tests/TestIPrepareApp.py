# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestIPrepareApp(unittest.TestCase):
    """
    Test the IPrepareApp object
    """

    def test_create_iprepareapp(self):
        """
        Check you can create a IPrepareApp object
        """
        from Ganga.GPIDev.Adapters.IPrepareApp import IPrepareApp
        a = IPrepareApp()
        self.assertIsInstance(a, IPrepareApp)
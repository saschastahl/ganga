# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestIRuntimeHandler(unittest.TestCase):
    """
    Test the TestIRuntimeHandler object
    """

    def test_create_iruntimehandler(self):
        """
        Check you can create a TestIRuntimeHandler object
        """
        from Ganga.GPIDev.Adapters.IRuntimeHandler import IRuntimeHandler
        a = IRuntimeHandler()
        self.assertIsInstance(a, IRuntimeHandler)
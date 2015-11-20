# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestExecutable(unittest.TestCase):
    """
    Test the Executable objects
    """

    def test_create_executable(self):
        """
        Check you can create a Executable object
        """
        from Ganga.Lib.Executable.Executable import Executable
        e = Executable()
        self.assertIsInstance(e, Executable)

    def test_exe_rthandler(self):
        """
        Check you can create an Executable RTHandler object
        """
        from Ganga.Lib.Executable.Executable import RTHandler
        e = RTHandler()
        self.assertIsInstance(e, RTHandler)

    def test_exe_lcgrthandler(self):
        """
        Check you can create an Executable LCGRTHandler object
        """
        from Ganga.Lib.Executable.Executable import LCGRTHandler
        e = LCGRTHandler()
        self.assertIsInstance(e, LCGRTHandler)

    def test_exe_gliterthandler(self):
        """
        Check you can create an Executable gLiteRTHandler object
        """
        from Ganga.Lib.Executable.Executable import gLiteRTHandler
        e = gLiteRTHandler()
        self.assertIsInstance(e, gLiteRTHandler)

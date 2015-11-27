# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestFileWorkspace(unittest.TestCase):
    """
    Test the FileWorkspace object
    TODO: Requires config system set up with 'Configuration':'gangadir available
    """

    # def test_create_fileworkspace(self):
    #     """
    #     Check you can create a FileWorkspace object
    #     """
    #     from Ganga.Core.FileWorkspace import FileWorkspace
    #     j = FileWorkspace()
    #     self.assertIsInstance(j, FileWorkspace)
    #
    # def test_create_inputworkspace(self):
    #     """
    #     Check you can create a FileWorkspace object
    #     """
    #     from Ganga.Core.FileWorkspace import InputWorkspace
    #     j = InputWorkspace()
    #     self.assertIsInstance(j, InputWorkspace)
    #
    # def test_create_outputworkspace(self):
    #     """
    #     Check you can create a OutputWorkspace object
    #     """
    #     from Ganga.Core.FileWorkspace import OutputWorkspace
    #     j = OutputWorkspace()
    #     self.assertIsInstance(j, OutputWorkspace)
    #
    # def test_create_debugworkspace(self):
    #     """
    #     Check you can create a DebugWorkspace object
    #     """
    #     from Ganga.Core.FileWorkspace import DebugWorkspace
    #     j = DebugWorkspace()
    #     self.assertIsInstance(j, DebugWorkspace)
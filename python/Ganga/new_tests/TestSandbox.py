# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestSandbox(unittest.TestCase):
    """
    Test the Sandbox objects
    """

    def test_create_SandboxError(self):
        """
        Check you can create a SandboxError object
        """
        from Ganga.Core.Sandbox.Sandbox import SandboxError
        e = SandboxError()
        self.assertIsInstance(e, SandboxError)
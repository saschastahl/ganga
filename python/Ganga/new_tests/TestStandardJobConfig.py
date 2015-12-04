# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestStandardJobConfig(unittest.TestCase):
    """
    Test the StandardJobConfig objects
    """

    def test_create_standardjobconfig(self):
        """
        Check you can create a StandardJobConfig object
        """
        from Ganga.GPIDev.Adapters.StandardJobConfig import StandardJobConfig
        e = StandardJobConfig()
        self.assertIsInstance(e, StandardJobConfig)
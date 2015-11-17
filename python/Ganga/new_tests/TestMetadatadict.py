# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestMetadatadict(unittest.TestCase):
    """
    Test the Metadict object
    """

    def test_create_metadatadict(self):
        """
        Check you can create a Metadatadict object
        """
        from Ganga.GPIDev.Lib.Job.Job import MetadataDict
        m = MetadataDict()
        self.assertIsInstance(m, MetadataDict)
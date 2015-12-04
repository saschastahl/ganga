# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestIMonitoringService(unittest.TestCase):
    """
    Test the IMonitoringService object
    """

    def test_create_imonitoringservice(self):
        """
        Check you can create a IMonitoringService object
        """
        from Ganga.GPIDev.Adapters.IMonitoringService import IMonitoringService
        a = IMonitoringService(None)
        self.assertIsInstance(a, IMonitoringService)

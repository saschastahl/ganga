# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestMonitoring(unittest.TestCase):
    """
    Test the Monitoring object
    """

    def test_create_monitoringclient(self):
        """
        Check you can create a MonitoringClient object
        """
        from Ganga.Core.MonitoringComponent.Monitoring import MonitoringClient
        a = MonitoringClient("MonitoringService")
        self.assertIsInstance(a, MonitoringClient)
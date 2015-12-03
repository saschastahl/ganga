# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestLocalGangaMCService(unittest.TestCase):
    """
    Test the LocalGangaMCService objects
    """

    def test_create_jobaction(self):
        """
        Check you can create a JobAction object
        """
        from Ganga.Core.MonitoringComponent.Local_GangaMC_Service import JobAction
        j = JobAction(str)
        self.assertIsInstance(j, JobAction)

    def test_create_monitoringworkerthread(self):
        """
        Check you can create a MonitoringWorkerThread object
        """
        from Ganga.Core.MonitoringComponent.Local_GangaMC_Service import MonitoringWorkerThread
        j = MonitoringWorkerThread("TestThread")
        self.assertIsInstance(j, MonitoringWorkerThread)

    def test_create_dictentry(self):
        """
        Check you can create a _DictEntry object
        """
        from Ganga.Core.MonitoringComponent.Local_GangaMC_Service import _DictEntry
        j = _DictEntry("Backend", "jobSet", "entryLock", 1.0)
        self.assertIsInstance(j, _DictEntry)

    def test_create_updatedict(self):
        """
        Check you can create a UpdateDict object
        """
        from Ganga.Core.MonitoringComponent.Local_GangaMC_Service import UpdateDict
        j = UpdateDict()
        self.assertIsInstance(j, UpdateDict)

    def test_create_callbackhookentry(self):
        """
        Check you can create a CallbackHookEntry object
        """
        from Ganga.Core.MonitoringComponent.Local_GangaMC_Service import CallbackHookEntry
        j = CallbackHookEntry({})
        self.assertIsInstance(j, CallbackHookEntry)

    def test_create_jobregistrymonitory(self):
        """
        Check you can create a JobRegistry_Monitor object
        """
        from Ganga.Core.MonitoringComponent.Local_GangaMC_Service import JobRegistry_Monitor
        j = JobRegistry_Monitor("TestRegistry")
        self.assertIsInstance(j, JobRegistry_Monitor)
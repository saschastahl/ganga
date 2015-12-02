# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestWorkerThreadPool(unittest.TestCase):
    """
    Test the WorkerThreadPool objects
    """
    # TODO: Default construction requires config available
    # def test_create_workerthreadpool_def(self):
    #      """
    #      Check you can create a WorkerThreadPool object
    #      """
    #      from Ganga.Core.GangaThread.WorkerThreads.WorkerThreadPool import WorkerThreadPool
    #      e = WorkerThreadPool()
    #      self.assertIsInstance(e, WorkerThreadPool)

    # TODO: Cannot import the module as getConfig is a default argument
    # def test_create_workerthreadpool(self):
    #      """
    #      Check you can create a WorkerThreadPool object
    #      """
    #      from Ganga.Core.GangaThread.WorkerThreads.WorkerThreadPool import WorkerThreadPool
    #      e = WorkerThreadPool(5, "testthread_")
    #      self.assertIsInstance(e, WorkerThreadPool)
# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestConfig(unittest.TestCase):
    """
    Test the SessionLockRefresher module
    """

    def test_create_sessionlockrefresher(self):
        """
        Check you can create a config error
        """
        from Ganga.Core.GangaRepository.SessionLock import SessionLockRefresher
        e = SessionLockRefresher("TestSession", "/tmp/test/dir", "test_fn", "TestRepo", False)

        self.assertIsInstance(e, SessionLockRefresher)

    def test_create_sessionlockmanager(self):
        """
        Check you can create a config error
        """
        from Ganga.Core.GangaRepository.SessionLock import SessionLockManager
        e = SessionLockManager("TestSession", "/tmp/test/dir", "TestSessionLockManager")

        self.assertIsInstance(e, SessionLockManager)
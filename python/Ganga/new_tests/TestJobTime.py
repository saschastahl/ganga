# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestJobTime(unittest.TestCase):
    """
    Test the JobTime object
    """

    def test_create_jobtime(self):
        """
        Check you can create a JobTime object
        """
        from Ganga.GPIDev.Lib.Job.Job import JobTime
        j = JobTime()
        self.assertIsInstance(j, JobTime)
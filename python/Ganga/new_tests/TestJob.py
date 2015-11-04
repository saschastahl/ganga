import unittest

from Ganga.GPIDev.Lib.Job.Job import Job


class TestProxy(unittest.TestCase):
    """
    Test the Job object
    """

    def test_create_job(self):
        """
        Check you can create a job object
        """
        j = Job()
        self.assertIsInstance(j, Job)

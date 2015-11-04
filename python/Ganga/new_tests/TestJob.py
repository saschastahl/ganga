import unittest2

class TestJob(unittest2.TestCase):
    """
    Test the Job object
    """

    def test_import_job(self):
        """
        Check you can create a job object
        """
        from Ganga.GPIDev.Lib.Job.Job import Job

    def test_create_job(self):
        """
        Check you can create a job object
        """
        from Ganga.GPIDev.Lib.Job.Job import Job
        j = Job()
        self.assertIsInstance(j, Job)

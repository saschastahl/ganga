# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestJob(unittest.TestCase):
    """
    Test the Job object
    """

    def test_import_job(self):
        """
        Check you can import the Job class
        """
        from Ganga.GPIDev.Lib.Job.Job import Job

    def test_create_job(self):
        """
        Check you can create a job object
        """
        from Ganga.GPIDev.Lib.Job.Job import Job
        j = Job()
        self.assertIsInstance(j, Job)

    def test_clone_job(self):
        """
        Check you can clone a job object
        """
        from Ganga.GPIDev.Lib.Job.Job import Job
        j = Job()
        j2 = j.clone()
        self.assertIsInstance(j2, Job)

    def test_set_properties(self):
        """
        Create a job and assign some properties
        """
        from Ganga.GPIDev.Lib.Job.Job import Job

        j = Job()
        j.name = "Test"

        self.assertEqual(len(j.inputfiles), 0)
        self.assertEqual(len(j.outputfiles), 0)
        self.assertEqual(j.name, "Test")

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

    def test_proxy(self):
        """
        Check a proxy can be added
        """
        import Ganga.GPIDev.Base.Proxy
        from Ganga.GPIDev.Lib.Job.Job import Job

        j = Job()
        pj = Ganga.GPIDev.Base.Proxy.addProxy(j)
        pj.name = "Test"

        self.assertIsInstance(Ganga.GPIDev.Base.Proxy.stripProxy(pj), Job)
        self.assertEqual(pj.name, "Test")

    def test_proxy_class_creation(self):
        """
        Check the copy construct method with proxy
        """
        # TODO: Should be done with: import ganga; j = ganga.Job()
        # TODO: GPIPRoxyFactory also doesn't work due to registry not being present
        #from Ganga.GPIDev.Base.Proxy import GPIProxyClassFactory
        #from Ganga.GPIDev.Lib.Job.Job import Job
        #pJob = GPIProxyClassFactory("Job", Job)
        #pj = pJob()
        #pj.name = "Test"

        from Ganga.GPIDev.Lib.Job.Job import Job
        j = Job()
        j.name = "Test"
        j2 = Job()
        j2.name = "Test2"
        j2.__construct__( tuple([j]) )

        self.assertIsInstance(j2, Job)
        self.assertEqual(j2.name, "Test")

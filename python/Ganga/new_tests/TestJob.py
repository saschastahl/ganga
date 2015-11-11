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

    def test_exceptions(self):
        """
        Create the exceptions classes
        """
        from Ganga.GPIDev.Lib.Job.Job import JobStatusError, JobError, PreparedStateError, FakeError
        e1 = JobStatusError()
        e2 = JobError()
        e3 = PreparedStateError()
        e4 = FakeError()

        self.assertIsInstance(e1, JobStatusError)
        self.assertIsInstance(e2, JobError)
        self.assertIsInstance(e3, PreparedStateError)
        self.assertIsInstance(e4, FakeError)

    # TODO: Can't run status change tests until registry is sorted
    #def test_status_update(self):
    #    """
    #    Test status changes
    #    """
    #    from Ganga.GPIDev.Lib.Job.Job import Job, JobStatusError
    #    j = Job()
    #    def update():
    #        j.updateStatus("running")
    #
    #    self.assertRaises(JobStatusError, update)
    #
    #    j.updateStatus("submitting")
    #    self.assertEqual(j.status, "submitting")

    def test_jobinfo(self):
        """
        Test the job info object
        """
        from Ganga.GPIDev.Lib.Job.Job import JobInfo
        ji = JobInfo()

        self.assertIsInstance(ji, JobInfo)

    def test_jobinfo_increment(self):
        """
        Test the job info object
        """
        from Ganga.GPIDev.Lib.Job.Job import JobInfo
        ji = JobInfo()
        ji.increment()

        self.assertEqual(ji.submit_counter, 1)

    def test_jobtemplate(self):
        """
        Test the job template object
        """
        from Ganga.GPIDev.Lib.Job.Job import JobTemplate
        jt = JobTemplate()

        self.assertIsInstance(jt, JobTemplate)
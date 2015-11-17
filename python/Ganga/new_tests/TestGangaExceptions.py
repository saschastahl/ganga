# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestGangaExceptions(unittest.TestCase):
    """
    Test the Ganga Exceptions
    """

    def test_ganga_exception(self):
        """
        Check you can create the GangaException
        """
        from Ganga.Core.exceptions import GangaException
        e = GangaException()
        self.assertIsInstance(e, GangaException)

    def test_app_config_error(self):
        """
        Check you can create the ApplicationConfigurationError
        """
        from Ganga.Core.exceptions import ApplicationConfigurationError
        e = ApplicationConfigurationError("", "Test Error Message")
        self.assertIsInstance(e, ApplicationConfigurationError)

    def test_app_prepare_error(self):
        """
        Check you can create the ApplicationPrepareError
        """
        from Ganga.Core.exceptions import ApplicationPrepareError
        e = ApplicationPrepareError()
        self.assertIsInstance(e, ApplicationPrepareError)

    def test_backend_error(self):
        """
        Check you can create the BackendError
        """
        from Ganga.Core.exceptions import BackendError
        e = BackendError("TestBackend", "Test Error Message")
        self.assertIsInstance(e, BackendError)

    def test_registry_error(self):
        """
        Check you can create the RepositoryError
        """
        from Ganga.Core.exceptions import RepositoryError
        e = RepositoryError()
        self.assertIsInstance(e, RepositoryError)

    def test_incomplete_job_submit_error(self):
        """
        Check you can create the IncompleteJobSubmissionError
        """
        from Ganga.Core.exceptions import IncompleteJobSubmissionError
        e = IncompleteJobSubmissionError()
        self.assertIsInstance(e, IncompleteJobSubmissionError)

    def test_incomplete_kill_error(self):
        """
        Check you can create the IncompleteKillError
        """
        from Ganga.Core.exceptions import IncompleteKillError
        e = IncompleteKillError()
        self.assertIsInstance(e, IncompleteKillError)

    def test_job_manager_error(self):
        """
        Check you can create the JobManagerError
        """
        from Ganga.Core.exceptions import JobManagerError
        e = JobManagerError("Test Error Message")
        self.assertIsInstance(e, JobManagerError)

    def test_attribute_error(self):
        """
        Check you can create the GangaAttributeError
        """
        from Ganga.Core.exceptions import GangaAttributeError
        e = GangaAttributeError()
        self.assertIsInstance(e, GangaAttributeError)

    def test_value_error(self):
        """
        Check you can create the GangaValueError
        """
        from Ganga.Core.exceptions import GangaValueError
        e = GangaValueError()
        self.assertIsInstance(e, GangaValueError)

    def test_io_error(self):
        """
        Check you can create the GangaIOError
        """
        from Ganga.Core.exceptions import GangaIOError
        e = GangaIOError()
        self.assertIsInstance(e, GangaIOError)

    def test_protected_attr_error(self):
        """
        Check you can create the ProtectedAttributeError
        """
        from Ganga.Core.exceptions import ProtectedAttributeError
        e = ProtectedAttributeError()
        self.assertIsInstance(e, ProtectedAttributeError)

    def test_read_only_object_error(self):
        """
        Check you can create the ReadOnlyObjectError
        """
        from Ganga.Core.exceptions import ReadOnlyObjectError
        e = ReadOnlyObjectError()
        self.assertIsInstance(e, ReadOnlyObjectError)

    def test_type_mismatch_error(self):
        """
        Check you can create the TypeMismatchError
        """
        from Ganga.Core.exceptions import TypeMismatchError
        e = TypeMismatchError()
        self.assertIsInstance(e, TypeMismatchError)

    def test_schema_error(self):
        """
        Check you can create the SchemaError
        """
        from Ganga.Core.exceptions import SchemaError
        e = SchemaError()
        self.assertIsInstance(e, SchemaError)
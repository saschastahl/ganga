# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestLogger(unittest.TestCase):
    """
    Test the logging object
    """

    def test_import_job(self):
        """
        Check you can import the Job class
        """
        import logging
        from Ganga.Utility.logging import getLogger, _formats
        private_logger = getLogger("TESTLOGGER.CHILD.GRANDCHILD")
        formatter = logging.Formatter(_formats['DEBUG'])
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        private_logger.setLevel(logging.DEBUG)
        private_logger.addHandler(console)
        private_logger.critical('hello')
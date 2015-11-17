# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestUtils(unittest.TestCase):
    """
    Test the Utils module
    """

    def test_generic_wrapper(self):
        """
        Check you can create the GenericWrapper class
        """
        from Ganga.Utility.util import GenericWrapper
        from Ganga.GPIDev.Lib.Job.Job import Job

        a = 0
        def myfunc():
            a += 1
            return

        g = GenericWrapper(Job, myfunc, myfunc)
        self.assertIsInstance(g, GenericWrapper)

    def test_execute_once(self):
        """
        Check the execute_once function
        """
        from Ganga.Utility.util import execute_once
        import Ganga.Utility.logic as logic

        assert(execute_once())
        assert(execute_once())

        if execute_once() and execute_once():
            assert(0)

        for i in range(5):
            assert(logic.equivalent(execute_once(), i == 0))
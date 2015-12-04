# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestApplicationRuntimeHandlers(unittest.TestCase):
    """
    Test the Config module
    """

    def test_applicationruntimehandlers(self):
        """
        Check you can create a config error
        """
        from Ganga.GPIDev.Adapters.ApplicationRuntimeHandlers import _ApplicationRuntimeHandlers
        a = _ApplicationRuntimeHandlers()
        a.add('a', 'X', 1)
        a.add('a', 'Y', 1)
        a.add('b', 'X', 1)
        a.add('c', 'Z', 1)

        def compare(alist, blist):
            alist.sort()
            blist.sort()
            self.assertEqual(alist, blist)

        compare(a.getAllBackends(), ['X', 'Y', 'Z'])
        compare(a.getAllApplications(), ['a', 'b', 'c'])

        compare(a.getAllBackends('a'), ['X', 'Y'])
        compare(a.getAllBackends('b'), ['X'])
        compare(a.getAllBackends('c'), ['Z'])

        compare(a.getAllApplications('X'), ['a', 'b'])
        compare(a.getAllApplications('Y'), ['a'])
        compare(a.getAllApplications('Z'), ['c'])

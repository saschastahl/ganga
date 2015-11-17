# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from Ganga.GPIDev.Base.Objects import GangaObject
from Ganga.GPIDev.Schema.Schema import Schema, Version, SimpleItem, ComponentItem, FileItem, SharedItem


class TestGangaObject(GangaObject):
    _schema = Schema(Version(1, 0), {'a': SimpleItem(42, typelist=['int'])})
    _category = 'TestGangaObject'
    _name = 'TestGangaObject'

    _exportmethods = ['example']

    def example(self):
        return 'example_string'

    def not_proxied(self):
        return 'example_string'


import Ganga.GPIDev.Base.Proxy
import Ganga.Core.exceptions


class TestProxy(unittest.TestCase):
    """
    Test the Proxy functions
    """

    def setUp(self):
        """
        Create an instance of the GangaObject subclass and save the proxy
        version of it
        """
        new_object = TestGangaObject()
        self.p = Ganga.GPIDev.Base.Proxy.addProxy(new_object)

    def test_default(self):
        """
        Check that the default value of a parameter is saved correctly
        """
        self.assertEqual(self.p.a, 42)

    def test_assign(self):
        """
        Make sure that valid values can be assigned to an attribute of the proxy
        """
        new_value = 7
        self.p.a = new_value
        self.assertEqual(self.p.a, new_value)

    def test_set_nonexistant(self):
        """
        Ensure that assigning to non-existant attributes raises an exception
        """
        def _assign():
            self.p.b = 'fail'

        self.assertRaises(Ganga.Core.exceptions.GangaAttributeError, _assign)

    def test_get_nonexistent(self):
        """
        Try to retrieve a non-existent attribute
        """
        def _get():
            temp = self.p.b

        self.assertRaises(AttributeError, _get)

    def test_set_wrong_type(self):
        """
        Ensure that assigning an incorrect type to an attribute raises an exception
        """
        def _assign():
            self.p.a = 'fail'

        self.assertRaises(Ganga.Core.exceptions.TypeMismatchError, _assign)

    def test_stripProxy(self):
        """
        Check that stripping the proxy returns the original class
        """
        stripped = Ganga.GPIDev.Base.Proxy.stripProxy(self.p)
        # TODO In Python >= 2.7 use
        #  self.assertIsInstance(stripped, TestGangaObject)
        self.assertEqual(type(stripped), TestGangaObject)

    def test_isType(self):
        self.assertTrue(Ganga.GPIDev.Base.Proxy.isType(self.p, TestGangaObject))

    def test_isProxy(self):
        self.assertTrue(Ganga.GPIDev.Base.Proxy.isProxy(self.p))

    def test_make_proxy_proxy(self):
        self.assertTrue(Ganga.GPIDev.Base.Proxy.addProxy(self.p) is self.p)

    def test_call_proxy_method(self):
        self.assertEqual(self.p.example(), 'example_string')

    def test_call_nonproxied_method(self):
        def _call():
            self.p.not_proxied()

        self.assertRaises(AttributeError, _call)


class TestVersion(unittest.TestCase):
    """
    Make sure that the version checks are working
    """
    def test_equal(self):
        v1 = Version(1, 0)
        v2 = Version(1, 0)
        self.assertEqual(v1, v2)
        self.assertTrue(v1.isCompatible(v2))

    def test_different(self):
        v1 = Version(1, 0)
        v2 = Version(1, 2)
        self.assertNotEqual(v1, v2)
        self.assertTrue(v2.isCompatible(v1))
        self.assertFalse(v1.isCompatible(v2))


class TestSchema(unittest.TestCase):
    def test_create(self):
        """
        Create a complex schema and make sure all the items are added
        """
        dd = {
            'application': ComponentItem(category='applications'),
            'backend': ComponentItem(category='backends'),
            'name': SimpleItem('', comparable=0),
            'share_str': SharedItem('Shared Test', comparable=0),
            'workdir': SimpleItem(defvalue=None, type='string', transient=1, protected=1, comparable=0),
            'status': SimpleItem(defvalue='new', protected=1, comparable=0),
            'id': SimpleItem(defvalue=None, type='string', protected=1, comparable=0),
            'inputbox': FileItem(defvalue=[], sequence=1),
            'outputbox': FileItem(defvalue=[], sequence=1),
            'overriden_copyable': SimpleItem(defvalue=None, protected=1, copyable=1),
            'plain_copyable': SimpleItem(defvalue=None, copyable=0)
        }
        s = Schema(Version(1, 0), dd)
        self.assertEqual(s.allItems(), dd.items())
        self.assertEqual(sorted(s.componentItems()+s.sharedItems()+s.simpleItems()), sorted(dd.items()))

    def test_get_non_existant(self):
        """
        Make sure that fetching a non-existant member raises the correct exception.
        """
        new_object = TestGangaObject()
        p = Ganga.GPIDev.Base.Proxy.addProxy(new_object)

        def _get():
            temp = p._schema['b']

        self.assertRaises(AttributeError, _get)

class TestSchemaOld(unittest.TestCase):
    def test_schema(self):
        """
        Copied the original schema tests to here. Probably covered in other places.
        """

        import copy
        dd = {
            'application': ComponentItem(category='applications'),
            'backend':     ComponentItem(category='backends'),
            'name':        SimpleItem('', comparable=0),
            'workdir':     SimpleItem(defvalue=None, type='string', transient=1, protected=1, comparable=0),
            'status':      SimpleItem(defvalue='new', protected=1, comparable=0),
            'id':           SimpleItem(defvalue=None, type='string', protected=1, comparable=0),
            'inputbox':     FileItem(defvalue=[], sequence=1),
            'outputbox':    FileItem(defvalue=[], sequence=1),
            'overriden_copyable': SimpleItem(defvalue=None, protected=1, copyable=1),
            'plain_copyable': SimpleItem(defvalue=None, copyable=0)
        }

        schema = Schema(Version(1, 0), dd)

        # NOT a public interface: emulate the Ganga Plugin object for test purposes
        # Note that pclass MUST be a new-style class in order to support deepcopy
        class pclass(object):
            _category = 'jobs'
            _name = 'Job'
        schema._pluginclass = pclass
        # end of emulating code
        # allSchemas.add(schema)

        assert(schema.name == 'Job')
        assert(schema.category == 'jobs')

        assert(schema.allItems() == dd.items())

        cc = (schema.componentItems() + schema.simpleItems()).sort()
        cc2 = dd.items().sort()
        assert(cc == cc2)

        for i in schema.allItems():
            assert(schema[i[0]] == schema.getItem(i[0]))

        assert(schema['id'].isA(SimpleItem))
        assert(schema['application'].isA(ComponentItem))
        assert(schema['inputbox'].isA(ComponentItem))
        assert(schema['inputbox'].isA(FileItem))

        assert(schema['id']['protected'])
        assert(schema['id']['type'] == 'string')

        schema2 = copy.deepcopy(schema)

        assert(schema2 is not schema)
        assert(schema.datadict is not schema2.datadict)
        assert(schema._pluginclass is schema2._pluginclass)

        for i in schema.allItems():
            assert(schema.getItem(i[0]) is not schema2.getItem(i[0]))

        # check the implied rules

        assert(schema['overriden_copyable']['copyable'] == 1)
        assert(schema['plain_copyable']['copyable'] == 0)
        assert(schema['id']['copyable'] == 0)
        assert(schema['application']['copyable'] == 1)

        assert(not schema['id']['comparable'])

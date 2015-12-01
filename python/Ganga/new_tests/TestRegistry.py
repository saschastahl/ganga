# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestRegistry(unittest.TestCase):
    """
    Test the Registry objects
    """

    def test_create_registryerror(self):
        """
        Check you can create a RegistryError object
        """
        from Ganga.Core.GangaRepository.Registry import RegistryError
        e = RegistryError()
        self.assertIsInstance(e, RegistryError)

    def test_create_registryaccesserror(self):
        """
        Check you can create a RegistryAccessError object
        """
        from Ganga.Core.GangaRepository.Registry import RegistryAccessError
        e = RegistryAccessError()
        self.assertIsInstance(e, RegistryAccessError)

    def test_create_registrylockerror(self):
        """
        Check you can create a RegistryLockError object
        """
        from Ganga.Core.GangaRepository.Registry import RegistryLockError
        e = RegistryLockError()
        self.assertIsInstance(e, RegistryLockError)

    def test_create_objectnotinregistryerror(self):
        """
        Check you can create a ObjectNotInRegistryError object
        """
        from Ganga.Core.GangaRepository.Registry import ObjectNotInRegistryError
        e = ObjectNotInRegistryError()
        self.assertIsInstance(e, ObjectNotInRegistryError)

    def test_create_registrykeyerror(self):
        """
        Check you can create a RegistryKeyError object
        """
        from Ganga.Core.GangaRepository.Registry import RegistryKeyError
        e = RegistryKeyError()
        self.assertIsInstance(e, RegistryKeyError)

    def test_create_registryindexerror(self):
        """
        Check you can create a RegistryIndexError object
        """
        from Ganga.Core.GangaRepository.Registry import RegistryIndexError
        e = RegistryIndexError()
        self.assertIsInstance(e, RegistryIndexError)

    def test_create_incompleteobject(self):
        """
        Check you can create a IncompleteObject object
        """
        from Ganga.Core.GangaRepository.Registry import IncompleteObject
        e = IncompleteObject("TestRegistry", 1)
        self.assertIsInstance(e, IncompleteObject)

    def test_create_registry(self):
        """
        Check you can create a Registry object
        """
        from Ganga.Core.GangaRepository.Registry import Registry
        e = Registry("TestRegistry", "My TestRegistry Doc")
        self.assertIsInstance(e, Registry)
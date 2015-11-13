# import unittest2 for python 2.6
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestConfig(unittest.TestCase):
    """
    Test the Config module
    """

    def test_config_error(self):
        """
        Check you can create a config error
        """
        from Ganga.Utility.Config.Config import ConfigError
        e = ConfigError()

        self.assertIsInstance(e, ConfigError)

    def test_config_option(self):
        """
        Check you can create a config option
        """
        from Ganga.Utility.Config.Config import ConfigOption
        o = ConfigOption("Test")

        self.assertIsInstance(o, ConfigOption)

    def test_package_config_option(self):
        """
        Check you can create a package config option
        """
        from Ganga.Utility.Config.Config import PackageConfig
        o = PackageConfig("Test", "my test doc string")

        self.assertIsInstance(o, PackageConfig)
"""
Provides Persistency and the base class for all Registries
Also, a list of all Registries is kept here
"""
allRegistries = {}


def addRegistry(registry):
    allRegistries[registry.name] = registry


def getRegistries():
    return allRegistries.values()


def getRegistry(name):
    return allRegistries[name]

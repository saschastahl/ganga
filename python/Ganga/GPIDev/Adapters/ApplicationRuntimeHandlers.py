##########################################################################
# Ganga Project. http://cern.ch/ganga
#
# $Id: ApplicationRuntimeHandlers.py,v 1.1 2008-07-17 16:40:52 moscicki Exp $
##########################################################################

""" Application adapter table is a mechanism to match application and backend handlers.
"""


class _ApplicationRuntimeHandlers(object):

    def __init__(self):
        self.handlers = {}

    def add(self, application, backend, handler):
        self.handlers.setdefault(backend, {})[application] = handler

    def get(self, application, backend):
        return self.handlers[backend][application]

    def getAllBackends(self, application=None):
        if application is None:
            return self.handlers.keys()
        else:
            return [b for b in self.handlers.keys() if application in self.handlers[b]]

    def getAllApplications(self, backend=None):
        if backend is None:
            apps = {}

            for a in self.handlers.values():
                apps.update(a)

            return apps.keys()
        else:
            return self.handlers[backend].keys()

allHandlers = _ApplicationRuntimeHandlers()


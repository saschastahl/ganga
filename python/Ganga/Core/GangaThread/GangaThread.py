# System imports
from threading import Thread

# Required Ganga imports from other modules
from Ganga.Utility.logging import getLogger

# Global Variables
logger = getLogger()


class GangaThread(Thread):

    def __init__(self, name, auto_register=True, critical=True, **kwds):
        from Ganga.Core.GangaThread.GangaThreadPool import GangaThreadPool

        self.gangaName = str(name)  # want to copy actual not by ref!
        name = 'GANGA_Update_Thread_%s' % name

        Thread.__init__(self, args=list(), name=name, **kwds)
        self.setDaemon(True)
        self.__should_stop_flag = False
        self.__critical = critical

        if auto_register:
            tpool = GangaThreadPool.getInstance()
            tpool.addServiceThread(self)

    def isCritical(self):
        """Return critical flag.

        @return: Boolean critical flag.
        """
        return self.__critical

    def setCritical(self, critical):
        """Set critical flag, which can be used for example in shutdown
        algorithms. See Ganga/Core/__init__.py for example.

        @param critical: Boolean critical flag.
        """
        self.__critical = critical

    def should_stop(self):
        return self.__should_stop_flag

    def stop(self):
        if not self.__should_stop_flag:
            logger.debug("Stopping: %s", self.gangaName)
            self.__should_stop_flag = True

    def unregister(self):
        from Ganga.Core.GangaThread.GangaThreadPool import GangaThreadPool
        GangaThreadPool.getInstance().delServiceThread(self)

    def register(self):
        from Ganga.Core.GangaThread.GangaThreadPool import GangaThreadPool
        GangaThreadPool.getInstance().addServiceThread(self)

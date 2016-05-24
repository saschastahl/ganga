from __future__ import absolute_import
import pytest

from Ganga.testlib.GangaUnitTest import GangaUnitTest


class TestJob(GangaUnitTest):

    def testSubmitNoBackend(self):
        from Ganga.GPI import DaVinci, Boole, Job, TestSubmitter, JobError
        from GangaLHCb.testlib import addLocalTestSubmitter

        for ap in [DaVinci, Boole]:

            j = Job(application=ap(), backend=TestSubmitter())

            # Test that submission fails before adding runtime handler
            with pytest.raises(JobError):
                j.submit()

            # Test that submission succeeds after adding it.
            addLocalTestSubmitter(ap)
            assert j.submit()

    @external
    def testSubmitLocalBackend(self):
        from Ganga.GPI import DaVinci, Boole, Job
        from GangaLHCb.testlib import addLocalTestSubmitter
        from Ganga.testlib.monitoring import run_until_completed

        for ap in [DaVinci, Boole]:

            j = Job(application=ap())
            addLocalTestSubmitter(ap)
            j.submit()

            run_until_completed(j)

            assert j.status in ['completed']


from __future__ import absolute_import

import pytest
from Ganga.testlib.mark import external
from Ganga.testlib.GangaUnitTest import GangaUnitTest


class TestDatasets(GangaUnitTest):

    def testDatasets(self):
        """
        Test the parts of the LHCbDataset which can be tested locally
        NB:
            99.9% of use of this is an LHCbDataset which consists of ONLY DiracFile objects
            There should __NEVER__ be any PhysicalFile or LogicalFile objects in this.
            Although the these are 'supported' in transitioning from Ganga 6.0.xy to 6.1
            they're changed upon load to LocalFile and DiracFile only, their use is discouraged
            as this will likely be dropped in the future
        """
        from Ganga.GPI import DiracFile, LHCbDataset, Job, LocalFile, OutputData

        # test constructors/setters
        ds = LHCbDataset(['lfn:a', 'pfn:b'])
        assert len(ds) == 2
        print(ds[0])
        assert isinstance(ds[0], DiracFile)
        assert isinstance(ds[1], LocalFile)
        ds = LHCbDataset()
        ds.files = ['lfn:a', 'pfn:b']
        assert isinstance(ds[0], DiracFile)
        assert isinstance(ds[1], LocalFile)
        ds.files.append('lfn:c')
        assert isinstance(ds[-1], DiracFile)
        d = OutputData(['a', 'b'])
        assert isinstance(d.files[0], str)
        assert isinstance(d.files[1], str)

        # check job assignments
        j = Job()
        j.inputdata = ['lfn:a', 'pfn:b']
        assert isinstance(j.inputdata, LHCbDataset)
        j.outputfiles = ['a', DiracFile('b')]
        assert isinstance(j.outputfiles[0], LocalFile)
        print(type(j.outputfiles[1]))
        assert isinstance(j.outputfiles[1], DiracFile)

    @external
    def testDatasets_External(self):
        """
        Test the components of LHCbDataset which rely on external code
        """
        from Ganga.GPI import LHCbDataset
        LFN_DATA = ['LFN:/lhcb/LHCb/Collision11/DIMUON.DST/00016768/0000/00016768_00000005_1.dimuon.dst',
                    'LFN:/lhcb/LHCb/Collision11/DIMUON.DST/00016768/0000/00016768_00000006_1.dimuon.dst']
        ds = LHCbDataset(LFN_DATA)

        assert len(ds.getReplicas().keys()) == 2
        assert ds.getCatalog()

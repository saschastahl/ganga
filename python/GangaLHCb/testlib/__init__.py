from Ganga.GPIDev.Adapters.ApplicationRuntimeHandlers import allHandlers
from GangaLHCb.Lib.RTHandlers.LHCbGaudiRunTimeHandler import LHCbGaudiRunTimeHandler
from Ganga.GPIDev.Base.Proxy import getName

def addLocalTestSubmitter(ap):
    allHandlers.add(getName(ap), 'TestSubmitter', LHCbGaudiRunTimeHandler)

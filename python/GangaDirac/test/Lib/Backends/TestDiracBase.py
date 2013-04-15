from GangaTest.Framework.tests                     import GangaGPITestCase
from GangaDirac.Lib.Backends.DiracBase             import DiracBase
#from GangaGaudi.Lib.RTHandlers.RunTimeHandlerUtils import get_share_path
from Ganga.GPIDev.Adapters.StandardJobConfig       import StandardJobConfig
#from Ganga.Core.exceptions                         import ApplicationConfigurationError, GangaException
from Ganga.GPI                                     import *
#import GangaDirac.Lib.Server.DiracServer as DiracServer
#GangaTest.Framework.utils defines some utility methods
#from GangaTest.Framework.utils import sleep_until_completed,sleep_until_state
import unittest, tempfile, os

class TestDiracBase(GangaGPITestCase):
    def setUp(self):
        from GangaDirac.Lib.Server.WorkerThreadPool import WorkerThreadPool
        class testServer(object):
            def __init__(this, returnObject):
                this.returnObject = returnObject
                this.toCheck      = {}

            def execute(this,command,timeout=60,env=None,cwd=None,shell=False):
                import inspect
                frame = inspect.currentframe()
                fedInVars = inspect.getargvalues(frame).locals
                del frame

                for key, value in this.toCheck.iteritems():
                    if key in fedInVars:
                        self.assertEqual(fedInVars[key], value)

                return this.returnObject
            def execute_nonblocking( this,command,command_args=(),command_kwargs={},timeout=60,env=None,cwd=None,shell=False,
                                     priority=5,callback_func=None,callback_args =(),callback_kwargs={} ):
                import inspect
                frame = inspect.currentframe()
                fedInVars = inspect.getargvalues(frame).locals
                del frame
                
                for key, value in this.toCheck.iteritems():
                    if key in fedInVars:
                        self.assertEqual(fedInVars[key], value)

                return this.returnObject
        self.ts = testServer(None)
        setattr(WorkerThreadPool, "execute", self.ts.execute)
        setattr(WorkerThreadPool, "execute_nonblocking", self.ts.execute_nonblocking)
        self.db = DiracBase()
        self.script="""
# dirac job created by ganga
###DIRAC_IMPORT###
###DIRAC_JOB_IMPORT###
dirac = ###DIRAC_OBJECT###
j = ###JOB_OBJECT###

# default commands added by ganga
j.setName('###NAME###')
j.setApplicationScript('###APP_NAME###','###APP_VERSION###','###APP_SCRIPT###',logFile='###APP_LOG_FILE###')
j.setRootPythonScript('###ROOTPY_VERSION###', '###ROOTPY_SCRIPT###', ###ROOTPY_ARGS###, '###ROOTPY_LOG_FILE###')
j.setRootMacro('###ROOT_VERSION###', '###ROOT_MACRO###', ###ROOT_ARGS###, '###ROOT_LOG_FILE###')
j.setExecutable('###EXE###','###EXE_ARG_STR###','###EXE_LOG_FILE###')
j.setExecutionEnv(###ENVIRONMENT###)
j.setInputSandbox(##INPUT_SANDBOX##)
j.setOutputSandbox(###OUTPUT_SANDBOX###)
j.setInputData(###INPUTDATA###)
j.setParametricInputData(###PARAMETRIC_INPUTDATA###)
j.setOutputData(###OUTPUTDATA###,OutputPath='###OUTPUT_PATH###',OutputSE=###OUTPUT_SE###)
j.setSystemConfig('###PLATFORM###')

# <-- user settings
###SETTINGS###
# user settings -->

# diracOpts added by user
###DIRAC_OPTS###

# submit the job to dirac
result = dirac.submit(j)
print result
"""
        
    def test__setup_subjob_dataset(self):
        self.assertEqual(self.db._setup_subjob_dataset([]),None,'Not None')

    def test__addition_sandbox_content(self):
        self.assertEqual(self.db._addition_sandbox_content(None),[],'Not empty list')

    def test__setup_bulk_subjobs(self):
        from Ganga.Core import BackendError
        from Ganga.GPIDev.Lib.Dataset.Dataset import Dataset

        fd, name=tempfile.mkstemp()
        file = os.fdopen(fd,'w')
        file.write(self.script.replace('###PARAMETRIC_INPUTDATA###',
                                       str([['a'],['b']])))
        file.close()
        self.assertRaises(BackendError,
                          self.db._setup_bulk_subjobs,
                          [],
                          name)

        d=Dirac()
        j=Job(application=DaVinci(),
              splitter=SplitByFiles(),
#              merger=SmartMerger(),
              inputdata=Dataset(),
              backend=d)
        d._impl._parent = j._impl
#        self.db._parent = j._impl
        dirac_ids = [123,456]

        def _setup_subjob_dataset(dataset):
            self.assertTrue(dataset in [['a'],['b']],'dataset not passed properly')
            return None

        setattr(self.db,'_setup_subjob_dataset',_setup_subjob_dataset)
        self.assertTrue(d._impl._setup_bulk_subjobs(dirac_ids, name),'didnt run')

        self.assertEqual(len(j.subjobs),len(dirac_ids),'didnt work')
        for id,backend_id,subjob in zip(range(len(dirac_ids)), dirac_ids, j.subjobs):
            self.assertEqual(id,subjob.id,'ids dont match')
            self.assertEqual(backend_id,subjob.backend.id,'backend.ids dont match')
            self.assertTrue(isinstance(subjob.application._impl, j.application._impl.__class__),'apps dont match')
            self.assertEqual(subjob.splitter, None,'splitter not done')
 #           self.assertEqual(subjob.merger, None,'mergers dont match')
            #self.assertEqual(subjob.inputdata, None)#,'inputdata dont match')
            self.assertTrue(isinstance(subjob.backend._impl, j.backend._impl.__class__),'backend dont match')

        
        os.remove(name)

    def test__common_submit(self):
        from Ganga.Core import BackendError

        fd, name=tempfile.mkstemp()
        file = os.fdopen(fd,'w')
        file.write(self.script.replace('###PARAMETRIC_INPUTDATA###',
                                       str([['a'],['b']])))
        file.close()
        self.ts.returnObject={}
#        class errorserver:
#            def execute(this, dirac_cmd):
#                return {}

        self.db.id = 1234
        self.db.actualCE='test'
        self.db.status='test'
        self.assertRaises(BackendError,
                          self.db._common_submit,
                          name,
                          self.ts)
#                          errorserver())

        self.assertEqual(self.db.id,None,'id not None')
        self.assertEqual(self.db.actualCE,None,'actualCE not None')
        self.assertEqual(self.db.status,None,'status not None')

#        class server:
#            def __init__(this, list_return=False):
#                this.list_return = list_return 
#            def execute(this, dirac_cmd):
#                self.assertEqual(dirac_cmd,"execfile('%s')"%name,'cmd wrong')
#                if this.list_return is True:
#                    return {'OK':True, 'Value': [123,456]}
#                return {'OK':True, 'Value': 12345}

        self.ts.toCheck={'command':"execfile('%s')"%name}
        self.ts.returnObject={'OK':True, 'Value': 12345}
        self.assertTrue(self.db._common_submit(name, self.ts))
        self.assertEqual(self.db.id,12345,'id not set')

        def _setup_bulk_subjobs(dirac_ids, dirac_script):
            self.assertEqual(dirac_ids,[123,456],'ids not equal')
            self.assertEqual(dirac_script, name,'dirac script not equal')
            return True

        setattr(self.db,'_setup_bulk_subjobs',_setup_bulk_subjobs)
        self.ts.returnObject={'OK':True, 'Value': [123,456]}
        self.assertTrue(self.db._common_submit(name, self.ts))

        os.remove(name)

    def test_submit(self):
        j=Job(backend=self.db)
        self.db._parent=j._impl


        file1 = tempfile.NamedTemporaryFile('w')
        file2 = tempfile.NamedTemporaryFile('w')
        file3 = tempfile.NamedTemporaryFile('w')
        sjc = StandardJobConfig(exe = self.script,
                                inputbox=[File(file1.name)._impl,
                                          File(file2.name)._impl,
                                          File(file3.name)._impl],
                                outputbox=['d','e','f'])
        def _addition_sandbox_content(subjobconfig):
            self.assertEqual(subjobconfig,sjc,'config objects not equal')
            return ['g']
        def _common_submit(dirac_script, server):
            #this needs to change to workerpool
            #from GangaDirac.Lib.Server.DiracClient import DiracClient
            #self.assertTrue(isinstance(server, DiracClient),'not a dirac client')
            f=open(dirac_script,'r')
            script = f.read()
            f.close()
            self.assertNotEqual(script,self.script,'script not changed')
            self.assertEqual(self.script.replace('##INPUT_SANDBOX##',
                                                 str(['a','b','c']+\
                                                     [os.path.join(j._impl.getInputWorkspace().getPath(),
                                                             '_input_sandbox_0.tgz')] +\
                                                     ['g'])),
                             script,'script not what it should be')
            
            return True

        setattr(self.db,'_addition_sandbox_content',_addition_sandbox_content)
        setattr(self.db,'_common_submit',_common_submit)

        
        self.assertTrue(self.db.submit(sjc,['a','b','c']),'didnt run')

        file1.close()
        file2.close()
        file3.close()

##     def test_master_auto_resubmit(self):
##         import inspect
##         print inspect.getsource(self.db.master_resubmit).replace('"""%s"""'%inspect.getdoc(self.db.master_resubmit),'')
##         print inspect.getsource(self.db.master_auto_resubmit)
    

    def test_resubmit(self):

        def _resubmit(server):
            #This needs to change to workerpool
            #from GangaDirac.Lib.Server.DiracClient import DiracClient
            #self.assertTrue(isinstance(server, DiracClient),'not a dirac client')
            return True

        setattr(self.db,'_resubmit',_resubmit)
        self.assertTrue(self.db.resubmit(),'did not run properly')


    def test__resubmit(self):
        from Ganga.Core import BackendError
 #       class server:
 #           def execute(this, dirac_cmd):
 #               return {}
        def _common_submit(dirac_script, server):
            
            return True
        setattr(self.db,'_common_submit',_common_submit)

        masterj = Job(backend=self.db)
        j=Job(backend=self.db)
        j._impl.master = masterj._impl

        # problem as keeps finding job 0 in main repository which has this 'dirac-script' file
        self.db._parent = masterj._impl        
        self.ts.returnObject={}
        self.assertRaises(BackendError,
                          self.db._resubmit,
                          self.ts)
#                          server())

##         self.db._parent = j._impl        
##         self.assertRaises(BackendError,
##                           self.db._resubmit,
##                           server())

        ## Come back to this

    def test_reset(self):
        j=Job(backend=self.db)._impl
        self.db._parent = j
        self.db.getJobObject().subjobs = [Job(backend=self.db)._impl,Job(backend=self.db)._impl]
        for j in self.db.getJobObject().subjobs: j.status='completing'

        disallowed_status = ['submitting','killed']
        for status in disallowed_status:
            self.db.getJobObject().status = status
            self.db.reset()
            self.assertEqual(self.db.getJobObject().status, status,'status shouldn\'t have changed')


        self.db.getJobObject().status = 'completing'
        self.db.reset()
        self.assertEqual(self.db.getJobObject().status,'submitted','didn\t reset job')
        self.assertNotEqual([j.status for j in self.db.getJobObject().subjobs],['submitted','submitted'], 'subjobs not reset properly')        

        self.db.reset(doSubjobs=True)
        self.assertEqual([j.status for j in self.db.getJobObject().subjobs],['submitted','submitted'], 'subjobs not reset properly')

        for j in self.db.getJobObject().subjobs: j.status='completed'
        self.db.reset(doSubjobs=True)
        self.assertNotEqual([j.status for j in self.db.getJobObject().subjobs],['submitted','submitted'], 'subjobs not supposed to reset')

    def test_kill(self):
#        class errorserver:
#            def execute(this, dirac_cmd):
#                return {}
#        setattr(DiracBase,'dirac_ganga_server',errorserver())
        self.ts.returnObject={}
        self.db.id=1234

        from Ganga.Core import BackendError
        self.assertRaises(BackendError,
                          self.db.kill)

#        class server:
#            def execute(this, dirac_cmd):
#                self.assertEqual(dirac_cmd,'kill(1234)','command not right')
#                return {'OK': True}
#        setattr(DiracBase,'dirac_ganga_server',server())
        self.ts.toCheck={'command':'kill(1234)'}
        self.ts.returnObject={'OK': True}
        self.assertTrue(self.db.kill(),'didn\'t run properly')

    def test_peek(self):
#        class server:
#            def execute(this, dirac_cmd):
#                self.assertEqual(dirac_cmd,'peek(1234)')
#                return {'OK':True,'Value':True}
#        setattr(DiracBase,'dirac_ganga_server',server())

        self.db.id=1234
        self.ts.toCheck={'command':'peek(1234)'}
        self.ts.returnObject={'OK':True,'Value':True}
        self.db.peek()

    def test_getOutputSandbox(self):
        j=Job(backend=self.db)
        self.db._parent=j._impl
        self.db.id=1234

        dir = j._impl.getOutputWorkspace().getPath()
#        class server:
#            def execute(this, dirac_cmd):
#                self.assertEqual(dirac_cmd,
#                                 "getOutputSandbox(1234,'%s')"%dir,
#                                 'command not right')
#                return {'OK':True}
#        setattr(DiracBase,'dirac_ganga_server',server())
        self.ts.toCheck={'command': "getOutputSandbox(1234,'%s')"%dir}
        self.ts.returnObject={'OK':True}
        self.assertTrue(self.db.getOutputSandbox(),'didn\'t run')

        dir = 'test_dir'
        self.ts.toCheck={'command': "getOutputSandbox(1234,'%s')"%dir}
        self.assertTrue(self.db.getOutputSandbox(dir),'didn\'t run with modified dir')

#        class errorserver:
#            def execute(this, dirac_cmd):
#                return {}
#        setattr(DiracBase,'dirac_ganga_server',errorserver())
 
        self.ts.toCheck={}
        self.ts.returnObject={}
        self.assertFalse(self.db.getOutputSandbox(dir)), 'didn\'t fail gracefully'


    def test_getOutputData(self):
        j=Job(backend=self.db)
        self.db._parent=j._impl
        self.db.id=1234
        names = ''
        dir   = j._impl.getOutputWorkspace().getPath()

#        class server:
#            def execute(this, dirac_cmd):
#                self.assertEqual(dirac_cmd,
#                                 "getOutputData(1234, '%s','%s')"%(names,dir))
#                if names =='': return {'OK':True}
#                return {'OK':True, 'Value':names+dir}
#        setattr(DiracBase,'dirac_ganga_server',server())
        self.ts.toCheck={'command': "getOutputData(1234, '%s','%s')"%(names,dir)}
        self.ts.returnObject={'OK':True}
        self.assertEqual(self.db.getOutputData(),[],'didn\'t run properly')
        self.assertEqual(self.db.getOutputData(dir, names),[],'should product same as default')
        
##        names = 'test_'
##        dir   = '_case'
##        self.assertEqual(self.db.getOutputData(dir,names),
##                         'test__case', 'output should match')
        

    def test_getOutputDataLFNs(self):
        pass
    
from toil.job import Job
from toil.common import Toil
from toil.lib.docker import apiDockerCall
from toil.wdl.wdl_functions import generate_docker_bashscript_file
from toil.wdl.wdl_functions import select_first
from toil.wdl.wdl_functions import sub
from toil.wdl.wdl_functions import size
from toil.wdl.wdl_functions import glob
from toil.wdl.wdl_functions import process_and_read_file
from toil.wdl.wdl_functions import process_infile
from toil.wdl.wdl_functions import process_outfile
from toil.wdl.wdl_functions import abspath_file
from toil.wdl.wdl_functions import combine_dicts
from toil.wdl.wdl_functions import parse_memory
from toil.wdl.wdl_functions import parse_cores
from toil.wdl.wdl_functions import parse_disk
from toil.wdl.wdl_functions import read_string
from toil.wdl.wdl_functions import read_int
from toil.wdl.wdl_functions import read_float
from toil.wdl.wdl_functions import read_tsv
from toil.wdl.wdl_functions import read_csv
from toil.wdl.wdl_functions import defined
import fnmatch
import textwrap
import subprocess
import os
import errno
import time
import shutil
import shlex
import uuid
import logging

asldijoiu23r8u34q89fho934t8u34fcurrentworkingdir = os.getcwd()

logger = logging.getLogger(__name__)


def handle_cmd_var(v, tempDir, fileStore, sep, default=''):
    if not v:
        return default
    if isinstance(v, tuple):
        return process_and_read_file(inputFile, tempDir, fileStore)
    if sep:
        return sep.join(v)
    return str(v).strip()


def initialize_jobs(job):
    job.fileStore.logToMaster("initialize_jobs")


class md5Cls(Job):
    def __init__(self, inputFile=None, *args, **kwargs):
        # memory=parse_memory('512 MB')
        # cores=parse_cores(1)
        # disk=parse_disk('local-disk 10 HDD')
        # Job.__init__(self, memory=memory, cores=cores, disk=disk)

        self.id_inputFile = inputFile
        super(md5Cls, self).__init__(*args, **kwargs)
    
    def run(self, fileStore):
        fileStore.logToMaster("md5")
        tempDir = fileStore.getLocalTempDir()
    
        try:
            os.makedirs(os.path.join(tempDir, 'execution'))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    
        inputFile = process_and_read_file(abspath_file(self.id_inputFile, asldijoiu23r8u34q89fho934t8u34fcurrentworkingdir), tempDir, fileStore, docker=True)


        try:
            # Intended to deal with "optional" inputs that may not exist
            # TODO: handle this better
            command0 = r'''
            /bin/my_md5sum '''
        except:
            command0 = ''
        

        try:
            # Intended to deal with "optional" inputs that may not exist
            # TODO: handle this better
            command1 = str(inputFile if not isinstance(inputFile, tuple) else process_and_read_file(inputFile, tempDir, fileStore)).strip("\n")
        except:
            command1 = ''
        

        try:
            # Intended to deal with "optional" inputs that may not exist
            # TODO: handle this better
            command2 = r'''
          '''
        except:
            command2 = ''
        

        cmd = command0 + command1 + command2
        cmd = textwrap.dedent(cmd.strip("\n"))
        generate_docker_bashscript_file(temp_dir=tempDir, docker_dir=tempDir, globs=[], cmd=cmd, job_name='md5')

        stdout = apiDockerCall(self, 
                               image='quay.io/briandoconnor/dockstore-tool-md5sum:1.0.4', 
                               working_dir=tempDir, 
                               parameters=[os.path.join(tempDir, "md5_script.sh")], 
                               entrypoint="/bin/bash", 
                               user='root', 
                               stderr=True, 
                               volumes={tempDir: {"bind": tempDir}})
        writetype = 'wb' if isinstance(stdout, bytes) else 'w'
        with open(os.path.join(asldijoiu23r8u34q89fho934t8u34fcurrentworkingdir, 'md5.log'), writetype) as f:
            f.write(stdout)
        
        # output-type: File
        output_filename = 'md5sum.txt'
        value = process_outfile(output_filename, fileStore, tempDir, '/home/lifeisaboutfishtacos/dockstore-workflow-md5sum')
        
        rvDict = {"value": value}
        return rvDict


if __name__=="__main__":
    options = Job.Runner.getDefaultOptions("./toilWorkflowRun")
    options.clean = 'always'
    with Toil(options) as fileStore:

        # WF Declarations
        inputFile = process_infile("md5sum.input", fileStore)

        job0 = Job.wrapJobFn(initialize_jobs)
        job0 = job0.encapsulate()
        md5 = job0.addChild(md5Cls(inputFile=inputFile))
        md5_value = md5.rv("value")

        fileStore.start(job0)

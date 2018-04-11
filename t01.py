
from toil.job import Job
from toil.common import Toil
from toil.lib.docker import apiDockerCall
from toil.wdl.toilwdl import generate_docker_bashscript_file
from toil.wdl.toilwdl import recursive_glob
import fnmatch
import subprocess
import os
import errno
import glob
import time
import shutil
import shlex
import uuid
import logging

logger = logging.getLogger(__name__)



def initialize_jobs(job):
    job.fileStore.logToMaster('''initialize_jobs''')



def haplotypeCaller(job, GATK, RefFasta, RefIndex, RefDict, sampleName, inputBAM, bamIndex):

    job.fileStore.logToMaster("haplotypeCaller")
    start = time.time()
    
    tempDir = job.fileStore.getLocalTempDir()
    
    

    try:
        GATK_fs = job.fileStore.readGlobalFile(GATK[0], userPath=os.path.join(tempDir, GATK[1]))
    except:
        GATK_fs = os.path.join(tempDir, GATK[1])
    
    

    try:
        RefFasta_fs = job.fileStore.readGlobalFile(RefFasta[0], userPath=os.path.join(tempDir, RefFasta[1]))
    except:
        RefFasta_fs = os.path.join(tempDir, RefFasta[1])
    
    

    try:
        RefIndex_fs = job.fileStore.readGlobalFile(RefIndex[0], userPath=os.path.join(tempDir, RefIndex[1]))
    except:
        RefIndex_fs = os.path.join(tempDir, RefIndex[1])
    
    

    try:
        RefDict_fs = job.fileStore.readGlobalFile(RefDict[0], userPath=os.path.join(tempDir, RefDict[1]))
    except:
        RefDict_fs = os.path.join(tempDir, RefDict[1])
    
    

    try:
        inputBAM_fs = job.fileStore.readGlobalFile(inputBAM[0], userPath=os.path.join(tempDir, inputBAM[1]))
    except:
        inputBAM_fs = os.path.join(tempDir, inputBAM[1])
    
    

    try:
        bamIndex_fs = job.fileStore.readGlobalFile(bamIndex[0], userPath=os.path.join(tempDir, bamIndex[1]))
    except:
        bamIndex_fs = os.path.join(tempDir, bamIndex[1])
    
    
    command0 = '''
    java -jar '''
    command1 = GATK_fs
    command2 = ''' \
        -T HaplotypeCaller \
        -R '''
    command3 = RefFasta_fs
    command4 = ''' \
        -I '''
    command5 = inputBAM_fs
    command6 = ''' \
        -o '''
    command7 = sampleName
    command8 = '''.raw.indels.snps.vcf
  '''

    cmd = command0 + command1 + command2 + command3 + command4 + command5 + command6 + command7 + command8


    this_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    this_process.communicate()
    

    output_filename = sampleName + '.raw.indels.snps.vcf'
    output_file = job.fileStore.writeGlobalFile(output_filename)
    job.fileStore.exportFile(output_file, "file:///home/quokka/Desktop/fretoil/toil/src/toil/wdl/" + output_filename)
    rawVCF = (output_file, output_filename)
    
    
    rvDict = {"rawVCF": rawVCF}


    end = time.time()
    with open("/home/quokka/Desktop/fretoil/toil/src/toil/wdl/wdl-stats.log", "a+") as f:
        f.write(str("haplotypeCaller") + " now being run.")
        f.write("\n\n")
        f.write("Outputs:\n")
        for rv in rvDict:
            f.write(str(rv) + ": " + str(rvDict[rv]))
            f.write("\n")
        f.write("Total runtime: %2.2f sec" % (end - start))
        f.write("\n\n")
    
    return rvDict



if __name__=="__main__":
    options = Job.Runner.getDefaultOptions("./toilWorkflowRun")
    with Toil(options) as toil:
        start = time.time()
        with open("/home/quokka/Desktop/fretoil/toil/src/toil/wdl/wdl-stats.log", "a+") as f:
            f.write("Starting WDL Job @ " + str(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())) + "\n\n")




        # JSON Variables
        RefIndex0 = toil.importFile("file:///home/quokka/Desktop/fretoil/toil/src/toil/test/wdl/GATK_data/ref/human_g1k_b37_20.fasta.fai")
        RefIndex0_preserveThisFilename = "human_g1k_b37_20.fasta.fai"
        RefIndex = (RefIndex0, RefIndex0_preserveThisFilename)
        sampleName = "WDL_tut1_output"
        inputBAM0 = toil.importFile("file:///home/quokka/Desktop/fretoil/toil/src/toil/test/wdl/GATK_data/inputs/NA12878_wgs_20.bam")
        inputBAM0_preserveThisFilename = "NA12878_wgs_20.bam"
        inputBAM = (inputBAM0, inputBAM0_preserveThisFilename)
        bamIndex0 = toil.importFile("file:///home/quokka/Desktop/fretoil/toil/src/toil/test/wdl/GATK_data/inputs/NA12878_wgs_20.bai")
        bamIndex0_preserveThisFilename = "NA12878_wgs_20.bai"
        bamIndex = (bamIndex0, bamIndex0_preserveThisFilename)
        GATK0 = toil.importFile("file:///home/quokka/Desktop/fretoil/toil/src/toil/test/wdl/GATK_data/GenomeAnalysisTK.jar")
        GATK0_preserveThisFilename = "GenomeAnalysisTK.jar"
        GATK = (GATK0, GATK0_preserveThisFilename)
        RefDict0 = toil.importFile("file:///home/quokka/Desktop/fretoil/toil/src/toil/test/wdl/GATK_data/ref/human_g1k_b37_20.dict")
        RefDict0_preserveThisFilename = "human_g1k_b37_20.dict"
        RefDict = (RefDict0, RefDict0_preserveThisFilename)
        RefFasta0 = toil.importFile("file:///home/quokka/Desktop/fretoil/toil/src/toil/test/wdl/GATK_data/ref/human_g1k_b37_20.fasta")
        RefFasta0_preserveThisFilename = "human_g1k_b37_20.fasta"
        RefFasta = (RefFasta0, RefFasta0_preserveThisFilename)


        # TSV Variables


        # CSV Variables

        job0 = Job.wrapJobFn(initialize_jobs)
        job1 = Job.wrapJobFn(haplotypeCaller, GATK=GATK, RefFasta=RefFasta, RefIndex=RefIndex, RefDict=RefDict, sampleName=sampleName, inputBAM=inputBAM, bamIndex=bamIndex)

        job0.addChild(job1)

        toil.start(job0)


        end = time.time()
        with open("/home/quokka/Desktop/fretoil/toil/src/toil/wdl/wdl-stats.log", "a+") as f:
            f.write("Ending WDL Job @ " + str(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())))
            f.write("\n")
            f.write("Total runtime: %2.2f sec" % (end - start))
            f.write("\n\n")
            f.write("\n" + "-"*80 + "\n")

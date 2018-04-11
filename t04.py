
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



def HaplotypeCallerERC(job, GATK, RefFasta, RefIndex, RefDict, sampleName, bamFile, bamIndex):

    job.fileStore.logToMaster("HaplotypeCallerERC")
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
        bamFile_fs = job.fileStore.readGlobalFile(bamFile[0], userPath=os.path.join(tempDir, bamFile[1]))
    except:
        bamFile_fs = os.path.join(tempDir, bamFile[1])
    
    

    try:
        bamIndex_fs = job.fileStore.readGlobalFile(bamIndex[0], userPath=os.path.join(tempDir, bamIndex[1]))
    except:
        bamIndex_fs = os.path.join(tempDir, bamIndex[1])
    
    
    command0 = '''
    java -jar '''
    command1 = GATK_fs
    command2 = ''' \
        -T HaplotypeCaller \
        -ERC GVCF \
        -R '''
    command3 = RefFasta_fs
    command4 = ''' \
        -I '''
    command5 = bamFile_fs
    command6 = ''' \
        -o '''
    command7 = sampleName
    command8 = '''_rawLikelihoods.g.vcf
  '''

    cmd = command0 + command1 + command2 + command3 + command4 + command5 + command6 + command7 + command8


    this_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    this_process.communicate()
    

    output_filename = sampleName + '_rawLikelihoods.g.vcf'
    output_file = job.fileStore.writeGlobalFile(output_filename)
    job.fileStore.exportFile(output_file, "file:///home/quokka/Desktop/fretoil/toil/src/toil/wdl/" + output_filename)
    GVCF = (output_file, output_filename)
    
    
    rvDict = {"GVCF": GVCF}


    end = time.time()
    with open("/home/quokka/Desktop/fretoil/toil/src/toil/wdl/wdl-stats.log", "a+") as f:
        f.write(str("HaplotypeCallerERC") + " now being run.")
        f.write("\n\n")
        f.write("Outputs:\n")
        for rv in rvDict:
            f.write(str(rv) + ": " + str(rvDict[rv]))
            f.write("\n")
        f.write("Total runtime: %2.2f sec" % (end - start))
        f.write("\n\n")
    
    return rvDict



def GenotypeGVCFs(job, GATK, RefFasta, RefIndex, RefDict, sampleName, GVCFs):

    job.fileStore.logToMaster("GenotypeGVCFs")
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
    
    
    GVCFs_list = []
    for i in GVCFs:
        try:
            j = job.fileStore.readGlobalFile(i["GVCF"][0], userPath=os.path.join(tempDir, i["GVCF"][1]))
            GVCFs_list.append(j)
        except:
            j = os.path.join(tempDir, i["GVCF"][1])
            GVCFs_list.append(j)
    GVCFs_sep = " -V ".join(GVCFs_list)

    command9 = '''
    java -jar '''
    command10 = GATK_fs
    command11 = ''' \
        -T GenotypeGVCFs \
        -R '''
    command12 = RefFasta_fs
    command13 = ''' \
        -V '''
    command14 = GVCFs_sep
    command15 = ''' \
        -o '''
    command16 = sampleName
    command17 = '''_rawVariants.vcf
  '''

    cmd = command9 + command10 + command11 + command12 + command13 + command14 + command15 + command16 + command17


    this_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    this_process.communicate()
    

    output_filename = sampleName + '_rawVariants.vcf'
    output_file = job.fileStore.writeGlobalFile(output_filename)
    job.fileStore.exportFile(output_file, "file:///home/quokka/Desktop/fretoil/toil/src/toil/wdl/" + output_filename)
    rawVCF = (output_file, output_filename)
    
    
    rvDict = {"rawVCF": rawVCF}


    end = time.time()
    with open("/home/quokka/Desktop/fretoil/toil/src/toil/wdl/wdl-stats.log", "a+") as f:
        f.write(str("GenotypeGVCFs") + " now being run.")
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
        refIndex0 = toil.importFile("file:///home/quokka/Desktop/fretoil/toil/src/toil/test/wdl/GATK_data/ref/human_g1k_b37_20.fasta.fai")
        refIndex0_preserveThisFilename = "human_g1k_b37_20.fasta.fai"
        refIndex = (refIndex0, refIndex0_preserveThisFilename)
        inputSamplesFile0 = toil.importFile("file:///home/quokka/Desktop/fretoil/toil/src/toil/test/wdl/GATK_data/inputsTSV.txt")
        inputSamplesFile0_preserveThisFilename = "inputsTSV.txt"
        inputSamplesFile = (inputSamplesFile0, inputSamplesFile0_preserveThisFilename)
        refDict0 = toil.importFile("file:///home/quokka/Desktop/fretoil/toil/src/toil/test/wdl/GATK_data/ref/human_g1k_b37_20.dict")
        refDict0_preserveThisFilename = "human_g1k_b37_20.dict"
        refDict = (refDict0, refDict0_preserveThisFilename)
        refFasta0 = toil.importFile("file:///home/quokka/Desktop/fretoil/toil/src/toil/test/wdl/GATK_data/ref/human_g1k_b37_20.fasta")
        refFasta0_preserveThisFilename = "human_g1k_b37_20.fasta"
        refFasta = (refFasta0, refFasta0_preserveThisFilename)
        gatk0 = toil.importFile("file:///home/quokka/Desktop/fretoil/toil/src/toil/test/wdl/GATK_data/GenomeAnalysisTK.jar")
        gatk0_preserveThisFilename = "GenomeAnalysisTK.jar"
        gatk = (gatk0, gatk0_preserveThisFilename)


        # TSV Variables

        inputSamples = []
        inputSamples0 = [['WDL_tut4a_output', 'src/toil/test/wdl/GATK_data/inputs/NA12878_wgs_20.bam', 'src/toil/test/wdl/GATK_data/inputs/NA12878_wgs_20.bai'], ['WDL_tut4b_output', 'src/toil/test/wdl/GATK_data/inputs/NA12878_wgs_20.bam', 'src/toil/test/wdl/GATK_data/inputs/NA12878_wgs_20.bai'], ['WDL_tut4c_output', 'src/toil/test/wdl/GATK_data/inputs/NA12878_wgs_20.bam', 'src/toil/test/wdl/GATK_data/inputs/NA12878_wgs_20.bai']]
        for sample0 in inputSamples0:
            sample = []
            for i in sample0:
                if os.path.isfile(str(i)):
                    sample0 = toil.importFile("file://" + os.path.abspath(i))
                    sample0_preserveThisFilename = os.path.basename(i)
                    sample.append((sample0, sample0_preserveThisFilename))
                else:
                    sample.append(i)
            inputSamples.append(sample)


        # CSV Variables

        job0 = Job.wrapJobFn(initialize_jobs)
        job1 = Job.wrapJobFn(HaplotypeCallerERC, GATK=gatk, RefFasta=refFasta, RefIndex=refIndex, RefDict=refDict, sampleName=inputSamples[0][0], bamFile=inputSamples[0][1], bamIndex=inputSamples[0][2])
        job2 = Job.wrapJobFn(HaplotypeCallerERC, GATK=gatk, RefFasta=refFasta, RefIndex=refIndex, RefDict=refDict, sampleName=inputSamples[1][0], bamFile=inputSamples[1][1], bamIndex=inputSamples[1][2])
        job3 = Job.wrapJobFn(HaplotypeCallerERC, GATK=gatk, RefFasta=refFasta, RefIndex=refIndex, RefDict=refDict, sampleName=inputSamples[2][0], bamFile=inputSamples[2][1], bamIndex=inputSamples[2][2])
        job4 = Job.wrapJobFn(GenotypeGVCFs, GATK=gatk, RefFasta=refFasta, RefIndex=refIndex, RefDict=refDict, sampleName='CEUtrio', GVCFs=[job3.rv(), job1.rv(), job2.rv()])

        job0.addChild(job3)
        job0.addChild(job1)
        job0.addChild(job2)

        toil.start(job0)


        end = time.time()
        with open("/home/quokka/Desktop/fretoil/toil/src/toil/wdl/wdl-stats.log", "a+") as f:
            f.write("Ending WDL Job @ " + str(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())))
            f.write("\n")
            f.write("Total runtime: %2.2f sec" % (end - start))
            f.write("\n\n")
            f.write("\n" + "-"*80 + "\n")

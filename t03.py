
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



def selectSNPs(job, GATK, RefFasta, RefIndex, RefDict, sampleName, type, rawVCF):

    job.fileStore.logToMaster("selectSNPs")
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
        rawVCF_fs = job.fileStore.readGlobalFile(rawVCF["rawVCF"][0], userPath=os.path.join(tempDir, rawVCF["rawVCF"][1]))
    except:
        rawVCF_fs = os.path.join(tempDir, rawVCF["rawVCF"][1])
    
    
    command9 = '''
    java -jar '''
    command10 = GATK_fs
    command11 = ''' \
      -T SelectVariants \
      -R '''
    command12 = RefFasta_fs
    command13 = ''' \
      -V '''
    command14 = rawVCF_fs
    command15 = ''' \
      -selectType '''
    command16 = type
    command17 = ''' \
      -o '''
    command18 = sampleName
    command19 = '''_raw.'''
    command20 = type
    command21 = '''.vcf
  '''

    cmd = command9 + command10 + command11 + command12 + command13 + command14 + command15 + command16 + command17 + command18 + command19 + command20 + command21


    this_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    this_process.communicate()
    

    output_filename = sampleName + '_raw.' + type + '.vcf'
    output_file = job.fileStore.writeGlobalFile(output_filename)
    job.fileStore.exportFile(output_file, "file:///home/quokka/Desktop/fretoil/toil/src/toil/wdl/" + output_filename)
    rawSubset = (output_file, output_filename)
    
    
    rvDict = {"rawSubset": rawSubset}


    end = time.time()
    with open("/home/quokka/Desktop/fretoil/toil/src/toil/wdl/wdl-stats.log", "a+") as f:
        f.write(str("selectSNPs") + " now being run.")
        f.write("\n\n")
        f.write("Outputs:\n")
        for rv in rvDict:
            f.write(str(rv) + ": " + str(rvDict[rv]))
            f.write("\n")
        f.write("Total runtime: %2.2f sec" % (end - start))
        f.write("\n\n")
    
    return rvDict



def selectIndels(job, GATK, RefFasta, RefIndex, RefDict, sampleName, type, rawVCF):

    job.fileStore.logToMaster("selectIndels")
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
        rawVCF_fs = job.fileStore.readGlobalFile(rawVCF["rawVCF"][0], userPath=os.path.join(tempDir, rawVCF["rawVCF"][1]))
    except:
        rawVCF_fs = os.path.join(tempDir, rawVCF["rawVCF"][1])
    
    
    command22 = '''
    java -jar '''
    command23 = GATK_fs
    command24 = ''' \
      -T SelectVariants \
      -R '''
    command25 = RefFasta_fs
    command26 = ''' \
      -V '''
    command27 = rawVCF_fs
    command28 = ''' \
      -selectType '''
    command29 = type
    command30 = ''' \
      -o '''
    command31 = sampleName
    command32 = '''_raw.'''
    command33 = type
    command34 = '''.vcf
  '''

    cmd = command22 + command23 + command24 + command25 + command26 + command27 + command28 + command29 + command30 + command31 + command32 + command33 + command34


    this_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    this_process.communicate()
    

    output_filename = sampleName + '_raw.' + type + '.vcf'
    output_file = job.fileStore.writeGlobalFile(output_filename)
    job.fileStore.exportFile(output_file, "file:///home/quokka/Desktop/fretoil/toil/src/toil/wdl/" + output_filename)
    rawSubset = (output_file, output_filename)
    
    
    rvDict = {"rawSubset": rawSubset}


    end = time.time()
    with open("/home/quokka/Desktop/fretoil/toil/src/toil/wdl/wdl-stats.log", "a+") as f:
        f.write(str("selectIndels") + " now being run.")
        f.write("\n\n")
        f.write("Outputs:\n")
        for rv in rvDict:
            f.write(str(rv) + ": " + str(rvDict[rv]))
            f.write("\n")
        f.write("Total runtime: %2.2f sec" % (end - start))
        f.write("\n\n")
    
    return rvDict



def hardFilterSNP(job, GATK, RefFasta, RefIndex, RefDict, sampleName, rawSNPs):

    job.fileStore.logToMaster("hardFilterSNP")
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
        rawSNPs_fs = job.fileStore.readGlobalFile(rawSNPs["rawSubset"][0], userPath=os.path.join(tempDir, rawSNPs["rawSubset"][1]))
    except:
        rawSNPs_fs = os.path.join(tempDir, rawSNPs["rawSubset"][1])
    
    
    command35 = '''
    java -jar '''
    command36 = GATK_fs
    command37 = ''' \
      -T VariantFiltration \
      -R '''
    command38 = RefFasta_fs
    command39 = ''' \
      -V '''
    command40 = rawSNPs_fs
    command41 = ''' \
      --filterExpression "FS > 60.0" \
      --filterName "snp_filter" \
      -o '''
    command42 = sampleName
    command43 = '''.filtered.snps.vcf
  '''

    cmd = command35 + command36 + command37 + command38 + command39 + command40 + command41 + command42 + command43


    this_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    this_process.communicate()
    

    output_filename = sampleName + '.filtered.snps.vcf'
    output_file = job.fileStore.writeGlobalFile(output_filename)
    job.fileStore.exportFile(output_file, "file:///home/quokka/Desktop/fretoil/toil/src/toil/wdl/" + output_filename)
    filteredSNPs = (output_file, output_filename)
    
    
    rvDict = {"filteredSNPs": filteredSNPs}


    end = time.time()
    with open("/home/quokka/Desktop/fretoil/toil/src/toil/wdl/wdl-stats.log", "a+") as f:
        f.write(str("hardFilterSNP") + " now being run.")
        f.write("\n\n")
        f.write("Outputs:\n")
        for rv in rvDict:
            f.write(str(rv) + ": " + str(rvDict[rv]))
            f.write("\n")
        f.write("Total runtime: %2.2f sec" % (end - start))
        f.write("\n\n")
    
    return rvDict



def hardFilterIndel(job, GATK, RefFasta, RefIndex, RefDict, sampleName, rawIndels):

    job.fileStore.logToMaster("hardFilterIndel")
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
        rawIndels_fs = job.fileStore.readGlobalFile(rawIndels["rawSubset"][0], userPath=os.path.join(tempDir, rawIndels["rawSubset"][1]))
    except:
        rawIndels_fs = os.path.join(tempDir, rawIndels["rawSubset"][1])
    
    
    command44 = '''
    java -jar '''
    command45 = GATK_fs
    command46 = ''' \
      -T VariantFiltration \
      -R '''
    command47 = RefFasta_fs
    command48 = ''' \
      -V '''
    command49 = rawIndels_fs
    command50 = ''' \
      --filterExpression "FS > 200.0" \
      --filterName "indel_filter" \
      -o '''
    command51 = sampleName
    command52 = '''.filtered.indels.vcf
  '''

    cmd = command44 + command45 + command46 + command47 + command48 + command49 + command50 + command51 + command52


    this_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    this_process.communicate()
    

    output_filename = sampleName + '.filtered.indels.vcf'
    output_file = job.fileStore.writeGlobalFile(output_filename)
    job.fileStore.exportFile(output_file, "file:///home/quokka/Desktop/fretoil/toil/src/toil/wdl/" + output_filename)
    filteredIndels = (output_file, output_filename)
    
    
    rvDict = {"filteredIndels": filteredIndels}


    end = time.time()
    with open("/home/quokka/Desktop/fretoil/toil/src/toil/wdl/wdl-stats.log", "a+") as f:
        f.write(str("hardFilterIndel") + " now being run.")
        f.write("\n\n")
        f.write("Outputs:\n")
        for rv in rvDict:
            f.write(str(rv) + ": " + str(rvDict[rv]))
            f.write("\n")
        f.write("Total runtime: %2.2f sec" % (end - start))
        f.write("\n\n")
    
    return rvDict



def combine(job, GATK, RefFasta, RefIndex, RefDict, sampleName, filteredSNPs, filteredIndels):

    job.fileStore.logToMaster("combine")
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
        filteredSNPs_fs = job.fileStore.readGlobalFile(filteredSNPs["filteredSNPs"][0], userPath=os.path.join(tempDir, filteredSNPs["filteredSNPs"][1]))
    except:
        filteredSNPs_fs = os.path.join(tempDir, filteredSNPs["filteredSNPs"][1])
    
    

    try:
        filteredIndels_fs = job.fileStore.readGlobalFile(filteredIndels["filteredIndels"][0], userPath=os.path.join(tempDir, filteredIndels["filteredIndels"][1]))
    except:
        filteredIndels_fs = os.path.join(tempDir, filteredIndels["filteredIndels"][1])
    
    
    command53 = '''
    java -jar '''
    command54 = GATK_fs
    command55 = ''' \
      -T CombineVariants \
      -R '''
    command56 = RefFasta_fs
    command57 = ''' \
      -V '''
    command58 = filteredSNPs_fs
    command59 = ''' \
      -V '''
    command60 = filteredIndels_fs
    command61 = ''' \
      --genotypemergeoption UNSORTED \
      -o '''
    command62 = sampleName
    command63 = '''.filtered.snps.indels.vcf
  '''

    cmd = command53 + command54 + command55 + command56 + command57 + command58 + command59 + command60 + command61 + command62 + command63


    this_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    this_process.communicate()
    

    output_filename = sampleName + '.filtered.snps.indels.vcf'
    output_file = job.fileStore.writeGlobalFile(output_filename)
    job.fileStore.exportFile(output_file, "file:///home/quokka/Desktop/fretoil/toil/src/toil/wdl/" + output_filename)
    filteredVCF = (output_file, output_filename)
    
    
    rvDict = {"filteredVCF": filteredVCF}


    end = time.time()
    with open("/home/quokka/Desktop/fretoil/toil/src/toil/wdl/wdl-stats.log", "a+") as f:
        f.write(str("combine") + " now being run.")
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
        name = "WDL_tut3_output"
        refIndex0 = toil.importFile("file:///home/quokka/Desktop/fretoil/toil/src/toil/test/wdl/GATK_data/ref/human_g1k_b37_20.fasta.fai")
        refIndex0_preserveThisFilename = "human_g1k_b37_20.fasta.fai"
        refIndex = (refIndex0, refIndex0_preserveThisFilename)
        inputBAM0 = toil.importFile("file:///home/quokka/Desktop/fretoil/toil/src/toil/test/wdl/GATK_data/inputs/NA12878_wgs_20.bam")
        inputBAM0_preserveThisFilename = "NA12878_wgs_20.bam"
        inputBAM = (inputBAM0, inputBAM0_preserveThisFilename)
        bamIndex0 = toil.importFile("file:///home/quokka/Desktop/fretoil/toil/src/toil/test/wdl/GATK_data/inputs/NA12878_wgs_20.bai")
        bamIndex0_preserveThisFilename = "NA12878_wgs_20.bai"
        bamIndex = (bamIndex0, bamIndex0_preserveThisFilename)
        gatk0 = toil.importFile("file:///home/quokka/Desktop/fretoil/toil/src/toil/test/wdl/GATK_data/GenomeAnalysisTK.jar")
        gatk0_preserveThisFilename = "GenomeAnalysisTK.jar"
        gatk = (gatk0, gatk0_preserveThisFilename)
        refDict0 = toil.importFile("file:///home/quokka/Desktop/fretoil/toil/src/toil/test/wdl/GATK_data/ref/human_g1k_b37_20.dict")
        refDict0_preserveThisFilename = "human_g1k_b37_20.dict"
        refDict = (refDict0, refDict0_preserveThisFilename)
        refFasta0 = toil.importFile("file:///home/quokka/Desktop/fretoil/toil/src/toil/test/wdl/GATK_data/ref/human_g1k_b37_20.fasta")
        refFasta0_preserveThisFilename = "human_g1k_b37_20.fasta"
        refFasta = (refFasta0, refFasta0_preserveThisFilename)


        # TSV Variables


        # CSV Variables

        job0 = Job.wrapJobFn(initialize_jobs)
        job1 = Job.wrapJobFn(haplotypeCaller, GATK=gatk, RefFasta=refFasta, RefIndex=refIndex, RefDict=refDict, sampleName=name, inputBAM=inputBAM, bamIndex=bamIndex)
        job2 = Job.wrapJobFn(selectSNPs, GATK=gatk, RefFasta=refFasta, RefIndex=refIndex, RefDict=refDict, sampleName=name, type='SNP', rawVCF=job1.rv())
        job3 = Job.wrapJobFn(selectIndels, GATK=gatk, RefFasta=refFasta, RefIndex=refIndex, RefDict=refDict, sampleName=name, type='INDEL', rawVCF=job1.rv())
        job4 = Job.wrapJobFn(hardFilterSNP, GATK=gatk, RefFasta=refFasta, RefIndex=refIndex, RefDict=refDict, sampleName=name, rawSNPs=job2.rv())
        job5 = Job.wrapJobFn(hardFilterIndel, GATK=gatk, RefFasta=refFasta, RefIndex=refIndex, RefDict=refDict, sampleName=name, rawIndels=job3.rv())
        job6 = Job.wrapJobFn(combine, GATK=gatk, RefFasta=refFasta, RefIndex=refIndex, RefDict=refDict, sampleName=name, filteredSNPs=job4.rv(), filteredIndels=job5.rv())

        job0.addChild(job1)

        toil.start(job0)


        end = time.time()
        with open("/home/quokka/Desktop/fretoil/toil/src/toil/wdl/wdl-stats.log", "a+") as f:
            f.write("Ending WDL Job @ " + str(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())))
            f.write("\n")
            f.write("Total runtime: %2.2f sec" % (end - start))
            f.write("\n\n")
            f.write("\n" + "-"*80 + "\n")

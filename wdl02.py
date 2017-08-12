from toil.job import Job
from toil.common import Toil
import subprocess
import os


def initialize_jobs(job):
    job.fileStore.logToMaster('initialize_jobs')


def haplotypeCaller(job, gatk, gatk_og, refFasta, refFasta_og, refIndex, refIndex_og, refDict, refDict_og, name, inputBAM, inputBAM_og, bamIndex, bamIndex_og):
    job.fileStore.logToMaster("haplotypeCaller")
    tempDir = job.fileStore.getLocalTempDir()

    gatk_filepath = os.path.join(tempDir, gatk_og)
    gatk = job.fileStore.readGlobalFile(gatk, userPath=gatk_filepath)
    refFasta_filepath = os.path.join(tempDir, refFasta_og)
    refFasta = job.fileStore.readGlobalFile(refFasta, userPath=refFasta_filepath)
    refIndex_filepath = os.path.join(tempDir, refIndex_og)
    refIndex = job.fileStore.readGlobalFile(refIndex, userPath=refIndex_filepath)
    refDict_filepath = os.path.join(tempDir, refDict_og)
    refDict = job.fileStore.readGlobalFile(refDict, userPath=refDict_filepath)
    inputBAM_filepath = os.path.join(tempDir, inputBAM_og)
    inputBAM = job.fileStore.readGlobalFile(inputBAM, userPath=inputBAM_filepath)
    bamIndex_filepath = os.path.join(tempDir, bamIndex_og)
    bamIndex = job.fileStore.readGlobalFile(bamIndex, userPath=bamIndex_filepath)

    command0 = 'java'
    command1 = '-jar'
    command2 = gatk
    command3 = '-T'
    command4 = 'HaplotypeCaller'
    command5 = '-R'
    command6 = refFasta
    command7 = '-I'
    command8 = inputBAM
    command9 = '-o'
    command10 = name + '.raw.indels.snps.vcf'

    subprocess.check_call([command0, command1, command2, command3, command4, command5, command6, command7, command8, command9, command10])

    output_filename0 = name + '.raw.indels.snps.vcf'
    output_file0 = job.fileStore.writeGlobalFile(output_filename0)
    return output_file0

def selectSNPs(job, gatk, gatk_og, refFasta, refFasta_og, refIndex, refIndex_og, refDict, refDict_og, name, type, rawVCF1, rawVCF1_og):
    job.fileStore.logToMaster("selectSNPs")
    tempDir = job.fileStore.getLocalTempDir()

    gatk_filepath = os.path.join(tempDir, gatk_og)
    gatk = job.fileStore.readGlobalFile(gatk, userPath=gatk_filepath)
    refFasta_filepath = os.path.join(tempDir, refFasta_og)
    refFasta = job.fileStore.readGlobalFile(refFasta, userPath=refFasta_filepath)
    refIndex_filepath = os.path.join(tempDir, refIndex_og)
    refIndex = job.fileStore.readGlobalFile(refIndex, userPath=refIndex_filepath)
    refDict_filepath = os.path.join(tempDir, refDict_og)
    refDict = job.fileStore.readGlobalFile(refDict, userPath=refDict_filepath)
    rawVCF1_filepath = os.path.join(tempDir, rawVCF1_og)
    rawVCF1 = job.fileStore.readGlobalFile(rawVCF1, userPath=rawVCF1_filepath)

    command11 = 'java'
    command12 = '-jar'
    command13 = gatk
    command14 = '-T'
    command15 = 'SelectVariants'
    command16 = '-R'
    command17 = refFasta
    command18 = '-V'
    command19 = rawVCF1
    command20 = '-selectType'
    command21 = type
    command22 = '-o'
    command23 = name + '_raw.' + type + '.vcf'

    subprocess.check_call([command11, command12, command13, command14, command15, command16, command17, command18, command19, command20, command21, command22, command23])

    output_filename1 = name + '_raw.' + type + '.vcf'
    output_file1 = job.fileStore.writeGlobalFile(output_filename1)
    return output_file1

def selectIndels(job, gatk, gatk_og, refFasta, refFasta_og, refIndex, refIndex_og, refDict, refDict_og, name, type, rawVCF1, rawVCF1_og):
    job.fileStore.logToMaster("selectIndels")
    tempDir = job.fileStore.getLocalTempDir()

    gatk_filepath = os.path.join(tempDir, gatk_og)
    gatk = job.fileStore.readGlobalFile(gatk, userPath=gatk_filepath)
    refFasta_filepath = os.path.join(tempDir, refFasta_og)
    refFasta = job.fileStore.readGlobalFile(refFasta, userPath=refFasta_filepath)
    refIndex_filepath = os.path.join(tempDir, refIndex_og)
    refIndex = job.fileStore.readGlobalFile(refIndex, userPath=refIndex_filepath)
    refDict_filepath = os.path.join(tempDir, refDict_og)
    refDict = job.fileStore.readGlobalFile(refDict, userPath=refDict_filepath)
    rawVCF1_filepath = os.path.join(tempDir, rawVCF1_og)
    rawVCF1 = job.fileStore.readGlobalFile(rawVCF1, userPath=rawVCF1_filepath)

    command24 = 'java'
    command25 = '-jar'
    command26 = gatk
    command27 = '-T'
    command28 = 'SelectVariants'
    command29 = '-R'
    command30 = refFasta
    command31 = '-V'
    command32 = rawVCF1
    command33 = '-selectType'
    command34 = type
    command35 = '-o'
    command36 = name + '_raw.' + type + '.vcf'

    subprocess.check_call([command24, command25, command26, command27, command28, command29, command30, command31, command32, command33, command34, command35, command36])

    output_filename2 = name + '_raw.' + type + '.vcf'
    output_file2 = job.fileStore.writeGlobalFile(output_filename2)
    return output_file2


if __name__=="__main__":
    options = Job.Runner.getDefaultOptions("./toilWorkflowRun")
    options.logLevel = "DEBUG"
    with Toil(options) as toil:
        # Scatter Variables

        # JSON/YML Variables
        name = "WDL_tut2_output"
        refIndex = toil.importFile("file:///home/lifeisaboutfishtacos/Desktop/wdl-tutorials/data/ref/human_g1k_b37_20.fasta.fai")
        refIndex_og = "human_g1k_b37_20.fasta.fai"
        inputBAM = toil.importFile("file:///home/lifeisaboutfishtacos/Desktop/wdl-tutorials/data/inputs/NA12878_wgs_20.bam")
        inputBAM_og = "NA12878_wgs_20.bam"
        bamIndex = toil.importFile("file:///home/lifeisaboutfishtacos/Desktop/wdl-tutorials/data/inputs/NA12878_wgs_20.bai")
        bamIndex_og = "NA12878_wgs_20.bai"
        gatk = toil.importFile("file:///home/lifeisaboutfishtacos/Desktop/wdl-tutorials/GenomeAnalysisTK.jar")
        gatk_og = "GenomeAnalysisTK.jar"
        refDict = toil.importFile("file:///home/lifeisaboutfishtacos/Desktop/wdl-tutorials/data/ref/human_g1k_b37_20.dict")
        refDict_og = "human_g1k_b37_20.dict"
        refFasta = toil.importFile("file:///home/lifeisaboutfishtacos/Desktop/wdl-tutorials/data/ref/human_g1k_b37_20.fasta")
        refFasta_og = "human_g1k_b37_20.fasta"

        # Output Variables
        rawVCF1_og = "rawVCF1.raw.indels.snps.vcf"

        job0 = Job.wrapJobFn(initialize_jobs)
        job1 = Job.wrapJobFn(haplotypeCaller, gatk, gatk_og, refFasta, refFasta_og, refIndex, refIndex_og, refDict, refDict_og, name, inputBAM, inputBAM_og, bamIndex, bamIndex_og)
        job2 = Job.wrapJobFn(selectSNPs, gatk, gatk_og, refFasta, refFasta_og, refIndex, refIndex_og, refDict, refDict_og, name, 'SNP', job1.rv(), rawVCF1_og)
        job3 = Job.wrapJobFn(selectIndels, gatk, gatk_og, refFasta, refFasta_og, refIndex, refIndex_og, refDict, refDict_og, name, 'INDEL', job1.rv(), rawVCF1_og)

        job0 = job0.encapsulate()
        job0.addChild(job1)

        job0 = job0.encapsulate()
        job0.addChild(job2)

        job0 = job0.encapsulate()
        job0.addChild(job3)

        toil.start(job0)
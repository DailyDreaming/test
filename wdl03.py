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

def hardFilterSNP(job, gatk, gatk_og, refFasta, refFasta_og, refIndex, refIndex_og, refDict, refDict_og, name, rawSubset2, rawSubset2_og):
    job.fileStore.logToMaster("hardFilterSNP")
    tempDir = job.fileStore.getLocalTempDir()

    gatk_filepath = os.path.join(tempDir, gatk_og)
    gatk = job.fileStore.readGlobalFile(gatk, userPath=gatk_filepath)
    refFasta_filepath = os.path.join(tempDir, refFasta_og)
    refFasta = job.fileStore.readGlobalFile(refFasta, userPath=refFasta_filepath)
    refIndex_filepath = os.path.join(tempDir, refIndex_og)
    refIndex = job.fileStore.readGlobalFile(refIndex, userPath=refIndex_filepath)
    refDict_filepath = os.path.join(tempDir, refDict_og)
    refDict = job.fileStore.readGlobalFile(refDict, userPath=refDict_filepath)
    rawSubset2_filepath = os.path.join(tempDir, rawSubset2_og)
    rawSubset2 = job.fileStore.readGlobalFile(rawSubset2, userPath=rawSubset2_filepath)

    command37 = 'java'
    command38 = '-jar'
    command39 = gatk
    command40 = '-T'
    command41 = 'VariantFiltration'
    command42 = '-R'
    command43 = refFasta
    command44 = '-V'
    command45 = rawSubset2
    command46 = '--filterExpression'
    command47 = 'FS > 60.0'
    command48 = '--filterName'
    command49 = 'snp_filter'
    command50 = '-o'
    command51 = name + '.filtered.snps.vcf'

    subprocess.check_call([command37, command38, command39, command40, command41, command42, command43, command44, command45, command46, command47, command48, command49, command50, command51])

    output_filename3 = name + '.filtered.snps.vcf'
    output_file3 = job.fileStore.writeGlobalFile(output_filename3)
    return output_file3

def hardFilterIndel(job, gatk, gatk_og, refFasta, refFasta_og, refIndex, refIndex_og, refDict, refDict_og, name, rawSubset3, rawSubset3_og):
    job.fileStore.logToMaster("hardFilterIndel")
    tempDir = job.fileStore.getLocalTempDir()

    gatk_filepath = os.path.join(tempDir, gatk_og)
    gatk = job.fileStore.readGlobalFile(gatk, userPath=gatk_filepath)
    refFasta_filepath = os.path.join(tempDir, refFasta_og)
    refFasta = job.fileStore.readGlobalFile(refFasta, userPath=refFasta_filepath)
    refIndex_filepath = os.path.join(tempDir, refIndex_og)
    refIndex = job.fileStore.readGlobalFile(refIndex, userPath=refIndex_filepath)
    refDict_filepath = os.path.join(tempDir, refDict_og)
    refDict = job.fileStore.readGlobalFile(refDict, userPath=refDict_filepath)
    rawSubset3_filepath = os.path.join(tempDir, rawSubset3_og)
    rawSubset3 = job.fileStore.readGlobalFile(rawSubset3, userPath=rawSubset3_filepath)

    command52 = 'java'
    command53 = '-jar'
    command54 = gatk
    command55 = '-T'
    command56 = 'VariantFiltration'
    command57 = '-R'
    command58 = refFasta
    command59 = '-V'
    command60 = rawSubset3
    command61 = '--filterExpression'
    command62 = 'FS > 200.0'
    command63 = '--filterName'
    command64 = 'indel_filter'
    command65 = '-o'
    command66 = name + '.filtered.indels.vcf'

    subprocess.check_call([command52, command53, command54, command55, command56, command57, command58, command59, command60, command61, command62, command63, command64, command65, command66])

    output_filename4 = name + '.filtered.indels.vcf'
    output_file4 = job.fileStore.writeGlobalFile(output_filename4)
    return output_file4

def combine(job, gatk, gatk_og, refFasta, refFasta_og, refIndex, refIndex_og, refDict, refDict_og, name, filteredSNPs4, filteredSNPs4_og, filteredIndels5, filteredIndels5_og):
    job.fileStore.logToMaster("combine")
    tempDir = job.fileStore.getLocalTempDir()

    gatk_filepath = os.path.join(tempDir, gatk_og)
    gatk = job.fileStore.readGlobalFile(gatk, userPath=gatk_filepath)
    refFasta_filepath = os.path.join(tempDir, refFasta_og)
    refFasta = job.fileStore.readGlobalFile(refFasta, userPath=refFasta_filepath)
    refIndex_filepath = os.path.join(tempDir, refIndex_og)
    refIndex = job.fileStore.readGlobalFile(refIndex, userPath=refIndex_filepath)
    refDict_filepath = os.path.join(tempDir, refDict_og)
    refDict = job.fileStore.readGlobalFile(refDict, userPath=refDict_filepath)
    filteredSNPs4_filepath = os.path.join(tempDir, filteredSNPs4_og)
    filteredSNPs4 = job.fileStore.readGlobalFile(filteredSNPs4, userPath=filteredSNPs4_filepath)
    filteredIndels5_filepath = os.path.join(tempDir, filteredIndels5_og)
    filteredIndels5 = job.fileStore.readGlobalFile(filteredIndels5, userPath=filteredIndels5_filepath)

    command67 = 'java'
    command68 = '-jar'
    command69 = gatk
    command70 = '-T'
    command71 = 'CombineVariants'
    command72 = '-R'
    command73 = refFasta
    command74 = '-V'
    command75 = filteredSNPs4
    command76 = '-V'
    command77 = filteredIndels5
    command78 = '--genotypemergeoption'
    command79 = 'UNSORTED'
    command80 = '-o'
    command81 = name + '.filtered.snps.indels.vcf'

    subprocess.check_call([command67, command68, command69, command70, command71, command72, command73, command74, command75, command76, command77, command78, command79, command80, command81])

    output_filename5 = name + '.filtered.snps.indels.vcf'
    output_file5 = job.fileStore.writeGlobalFile(output_filename5)
    return output_file5


if __name__=="__main__":
    options = Job.Runner.getDefaultOptions("./toilWorkflowRun")
    options.logLevel = "DEBUG"
    with Toil(options) as toil:
        # Scatter Variables

        # JSON/YML Variables
        name = "WDL_tut3_output"
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
        filteredIndels5_og = "filteredIndels5.filtered.indels.vcf"
        rawVCF1_og = "rawVCF1.raw.indels.snps.vcf"
        rawSubset3_og = "rawSubset3.vcf"
        rawSubset2_og = "rawSubset2.vcf"
        filteredSNPs4_og = "filteredSNPs4.filtered.snps.vcf"

        job0 = Job.wrapJobFn(initialize_jobs)
        job1 = Job.wrapJobFn(haplotypeCaller, gatk, gatk_og, refFasta, refFasta_og, refIndex, refIndex_og, refDict, refDict_og, name, inputBAM, inputBAM_og, bamIndex, bamIndex_og)
        job2 = Job.wrapJobFn(selectSNPs, gatk, gatk_og, refFasta, refFasta_og, refIndex, refIndex_og, refDict, refDict_og, name, 'SNP', job1.rv(), rawVCF1_og)
        job3 = Job.wrapJobFn(selectIndels, gatk, gatk_og, refFasta, refFasta_og, refIndex, refIndex_og, refDict, refDict_og, name, 'INDEL', job1.rv(), rawVCF1_og)
        job4 = Job.wrapJobFn(hardFilterSNP, gatk, gatk_og, refFasta, refFasta_og, refIndex, refIndex_og, refDict, refDict_og, name, job2.rv(), rawSubset2_og)
        job5 = Job.wrapJobFn(hardFilterIndel, gatk, gatk_og, refFasta, refFasta_og, refIndex, refIndex_og, refDict, refDict_og, name, job3.rv(), rawSubset3_og)
        job6 = Job.wrapJobFn(combine, gatk, gatk_og, refFasta, refFasta_og, refIndex, refIndex_og, refDict, refDict_og, name, job4.rv(), filteredSNPs4_og, job5.rv(), filteredIndels5_og)

        job0 = job0.encapsulate()
        job0.addChild(job1)

        job0 = job0.encapsulate()
        job0.addChild(job2)

        job0 = job0.encapsulate()
        job0.addChild(job3)

        job0 = job0.encapsulate()
        job0.addChild(job4)

        job0 = job0.encapsulate()
        job0.addChild(job5)

        job0 = job0.encapsulate()
        job0.addChild(job6)

        toil.start(job0)
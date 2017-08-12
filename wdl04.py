from toil.job import Job
from toil.common import Toil
import subprocess
import os


def initialize_jobs(job):
    job.fileStore.logToMaster('initialize_jobs')


def HaplotypeCallerERC(job, gatk, gatk_og, refFasta, refFasta_og, refIndex, refIndex_og, refDict, refDict_og, sample0, sample1, sample1_og, sample2, sample2_og):
    job.fileStore.logToMaster("HaplotypeCallerERC")
    tempDir = job.fileStore.getLocalTempDir()

    gatk_filepath = os.path.join(tempDir, gatk_og)
    gatk = job.fileStore.readGlobalFile(gatk, userPath=gatk_filepath)
    refFasta_filepath = os.path.join(tempDir, refFasta_og)
    refFasta = job.fileStore.readGlobalFile(refFasta, userPath=refFasta_filepath)
    refIndex_filepath = os.path.join(tempDir, refIndex_og)
    refIndex = job.fileStore.readGlobalFile(refIndex, userPath=refIndex_filepath)
    refDict_filepath = os.path.join(tempDir, refDict_og)
    refDict = job.fileStore.readGlobalFile(refDict, userPath=refDict_filepath)
    sample1_filepath = os.path.join(tempDir, sample1_og)
    sample1 = job.fileStore.readGlobalFile(sample1, userPath=sample1_filepath)
    sample2_filepath = os.path.join(tempDir, sample2_og)
    sample2 = job.fileStore.readGlobalFile(sample2, userPath=sample2_filepath)

    command0 = 'java'
    command1 = '-jar'
    command2 = gatk
    command3 = '-T'
    command4 = 'HaplotypeCaller'
    command5 = '-ERC'
    command6 = 'GVCF'
    command7 = '-R'
    command8 = refFasta
    command9 = '-I'
    command10 = sample1
    command11 = '-o'
    command12 = sample0 + '_rawLikelihoods.g.vcf'

    subprocess.check_call([command0, command1, command2, command3, command4, command5, command6, command7, command8, command9, command10, command11, command12])

    output_filename0 = sample0 + '_rawLikelihoods.g.vcf'
    output_file0 = job.fileStore.writeGlobalFile(output_filename0)
    return output_file0

def GenotypeGVCFs(job, gatk, gatk_og, refFasta, refFasta_og, refIndex, refIndex_og, refDict, refDict_og, sampleName, GVCF2, GVCF2_og, GVCF3, GVCF3_og, GVCF1, GVCF1_og):
    job.fileStore.logToMaster("GenotypeGVCFs")
    tempDir = job.fileStore.getLocalTempDir()

    gatk_filepath = os.path.join(tempDir, gatk_og)
    gatk = job.fileStore.readGlobalFile(gatk, userPath=gatk_filepath)
    refFasta_filepath = os.path.join(tempDir, refFasta_og)
    refFasta = job.fileStore.readGlobalFile(refFasta, userPath=refFasta_filepath)
    refIndex_filepath = os.path.join(tempDir, refIndex_og)
    refIndex = job.fileStore.readGlobalFile(refIndex, userPath=refIndex_filepath)
    refDict_filepath = os.path.join(tempDir, refDict_og)
    refDict = job.fileStore.readGlobalFile(refDict, userPath=refDict_filepath)
    GVCF2_filepath = os.path.join(tempDir, GVCF2_og)
    GVCF2 = job.fileStore.readGlobalFile(GVCF2, userPath=GVCF2_filepath)
    GVCF3_filepath = os.path.join(tempDir, GVCF3_og)
    GVCF3 = job.fileStore.readGlobalFile(GVCF3, userPath=GVCF3_filepath)
    GVCF1_filepath = os.path.join(tempDir, GVCF1_og)
    GVCF1 = job.fileStore.readGlobalFile(GVCF1, userPath=GVCF1_filepath)

    command13 = 'java'
    command14 = '-jar'
    command15 = gatk
    command16 = '-T'
    command17 = 'GenotypeGVCFs'
    command18 = '-R'
    command19 = refFasta
    command20 = '-V'
    command21 = GVCF2
    command22 = '-V'
    command23 = GVCF3
    command24 = '-V'
    command25 = GVCF1
    command26 = '-o'
    command27 = sampleName + '_rawVariants.vcf'

    subprocess.check_call([command13, command14, command15, command16, command17, command18, command19, command20, command21, command22, command23, command24, command25, command26, command27])

    output_filename1 = sampleName + '_rawVariants.vcf'
    output_file1 = job.fileStore.writeGlobalFile(output_filename1)
    return output_file1


if __name__=="__main__":
    options = Job.Runner.getDefaultOptions("./toilWorkflowRun")
    options.logLevel = "DEBUG"
    with Toil(options) as toil:
        # Scatter Variables
        sample0_2 = "WDL_tut4b_output"
        sample1_2 = toil.importFile("file:///home/lifeisaboutfishtacos/Desktop/wdl-tutorials/data/inputs/NA12878_wgs_20.bam")
        sample1_2_og = "NA12878_wgs_20.bam"
        sample2_2 = toil.importFile("file:///home/lifeisaboutfishtacos/Desktop/wdl-tutorials/data/inputs/NA12878_wgs_20.bai")
        sample2_2_og = "NA12878_wgs_20.bai"
        sample0_1 = "WDL_tut4a_output"
        sample1_1 = toil.importFile("file:///home/lifeisaboutfishtacos/Desktop/wdl-tutorials/data/inputs/NA12878_wgs_20.bam")
        sample1_1_og = "NA12878_wgs_20.bam"
        sample2_1 = toil.importFile("file:///home/lifeisaboutfishtacos/Desktop/wdl-tutorials/data/inputs/NA12878_wgs_20.bai")
        sample2_1_og = "NA12878_wgs_20.bai"
        sample0_3 = "WDL_tut4c_output"
        sample1_3 = toil.importFile("file:///home/lifeisaboutfishtacos/Desktop/wdl-tutorials/data/inputs/NA12878_wgs_20.bam")
        sample1_3_og = "NA12878_wgs_20.bam"
        sample2_3 = toil.importFile("file:///home/lifeisaboutfishtacos/Desktop/wdl-tutorials/data/inputs/NA12878_wgs_20.bai")
        sample2_3_og = "NA12878_wgs_20.bai"

        # JSON/YML Variables
        refIndex = toil.importFile("file:///home/lifeisaboutfishtacos/Desktop/wdl-tutorials/data/ref/human_g1k_b37_20.fasta.fai")
        refIndex_og = "human_g1k_b37_20.fasta.fai"
        inputSamplesFile = toil.importFile("file:///home/lifeisaboutfishtacos/Desktop/wdl-tutorials/t04/inputsTSV.txt")
        inputSamplesFile_og = "inputsTSV.txt"
        refDict = toil.importFile("file:///home/lifeisaboutfishtacos/Desktop/wdl-tutorials/data/ref/human_g1k_b37_20.dict")
        refDict_og = "human_g1k_b37_20.dict"
        refFasta = toil.importFile("file:///home/lifeisaboutfishtacos/Desktop/wdl-tutorials/data/ref/human_g1k_b37_20.fasta")
        refFasta_og = "human_g1k_b37_20.fasta"
        gatk = toil.importFile("file:///home/lifeisaboutfishtacos/Desktop/wdl-tutorials/GenomeAnalysisTK.jar")
        gatk_og = "GenomeAnalysisTK.jar"

        # Output Variables
        GVCF2_og = "GVCF2_rawLikelihoods.g.vcf"
        GVCF3_og = "GVCF3_rawLikelihoods.g.vcf"
        GVCF1_og = "GVCF1_rawLikelihoods.g.vcf"

        job0 = Job.wrapJobFn(initialize_jobs)
        job1 = Job.wrapJobFn(HaplotypeCallerERC, gatk, gatk_og, refFasta, refFasta_og, refIndex, refIndex_og, refDict, refDict_og, sample0_1, sample1_1, sample1_1_og, sample2_1, sample2_1_og)
        job2 = Job.wrapJobFn(HaplotypeCallerERC, gatk, gatk_og, refFasta, refFasta_og, refIndex, refIndex_og, refDict, refDict_og, sample0_2, sample1_2, sample1_2_og, sample2_2, sample2_2_og)
        job3 = Job.wrapJobFn(HaplotypeCallerERC, gatk, gatk_og, refFasta, refFasta_og, refIndex, refIndex_og, refDict, refDict_og, sample0_3, sample1_3, sample1_3_og, sample2_3, sample2_3_og)
        job4 = Job.wrapJobFn(GenotypeGVCFs, gatk, gatk_og, refFasta, refFasta_og, refIndex, refIndex_og, refDict, refDict_og, 'CEUtrio', job2.rv(), GVCF2_og, job3.rv(), GVCF3_og, job1.rv(), GVCF1_og)

        job0 = job0.encapsulate()
        job0.addChild(job2)
        job0.addChild(job3)
        job0.addChild(job1)

        job0 = job0.encapsulate()
        job0.addChild(job4)

        toil.start(job0)
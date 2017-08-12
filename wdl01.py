from toil.job import Job
from toil.common import Toil
import subprocess
import os


def initialize_jobs(job):
    job.fileStore.logToMaster('initialize_jobs')


def haplotypeCaller(job, GATK, GATK_og, RefFasta, RefFasta_og, RefIndex, RefIndex_og, RefDict, RefDict_og, sampleName, inputBAM, inputBAM_og, bamIndex, bamIndex_og):
    job.fileStore.logToMaster("haplotypeCaller")
    tempDir = job.fileStore.getLocalTempDir()

    GATK_filepath = os.path.join(tempDir, GATK_og)
    GATK = job.fileStore.readGlobalFile(GATK, userPath=GATK_filepath)
    RefFasta_filepath = os.path.join(tempDir, RefFasta_og)
    RefFasta = job.fileStore.readGlobalFile(RefFasta, userPath=RefFasta_filepath)
    RefIndex_filepath = os.path.join(tempDir, RefIndex_og)
    RefIndex = job.fileStore.readGlobalFile(RefIndex, userPath=RefIndex_filepath)
    RefDict_filepath = os.path.join(tempDir, RefDict_og)
    RefDict = job.fileStore.readGlobalFile(RefDict, userPath=RefDict_filepath)
    inputBAM_filepath = os.path.join(tempDir, inputBAM_og)
    inputBAM = job.fileStore.readGlobalFile(inputBAM, userPath=inputBAM_filepath)
    bamIndex_filepath = os.path.join(tempDir, bamIndex_og)
    bamIndex = job.fileStore.readGlobalFile(bamIndex, userPath=bamIndex_filepath)

    command0 = 'java'
    command1 = '-jar'
    command2 = GATK
    command3 = '-T'
    command4 = 'HaplotypeCaller'
    command5 = '-R'
    command6 = RefFasta
    command7 = '-I'
    command8 = inputBAM
    command9 = '-o'
    command10 = sampleName + '.raw.indels.snps.vcf'

    subprocess.check_call([command0, command1, command2, command3, command4, command5, command6, command7, command8, command9, command10])

    output_filename0 = sampleName + '.raw.indels.snps.vcf'
    output_file0 = job.fileStore.writeGlobalFile(output_filename0)
    return output_file0


if __name__=="__main__":
    options = Job.Runner.getDefaultOptions("./toilWorkflowRun")
    options.logLevel = "DEBUG"
    with Toil(options) as toil:
        # Scatter Variables

        # JSON/YML Variables
        RefIndex = toil.importFile("file:///home/lifeisaboutfishtacos/Desktop/wdl-tutorials/data/ref/human_g1k_b37_20.fasta.fai")
        RefIndex_og = "human_g1k_b37_20.fasta.fai"
        sampleName = "/home/lifeisaboutfishtacos/Desktop/WDL_tut_output"
        inputBAM = toil.importFile("file:///home/lifeisaboutfishtacos/Desktop/wdl-tutorials/data/inputs/NA12878_wgs_20.bam")
        inputBAM_og = "NA12878_wgs_20.bam"
        bamIndex = toil.importFile("file:///home/lifeisaboutfishtacos/Desktop/wdl-tutorials/data/inputs/NA12878_wgs_20.bai")
        bamIndex_og = "NA12878_wgs_20.bai"
        GATK = toil.importFile("file:///home/lifeisaboutfishtacos/Desktop/wdl-tutorials/GenomeAnalysisTK.jar")
        GATK_og = "GenomeAnalysisTK.jar"
        RefDict = toil.importFile("file:///home/lifeisaboutfishtacos/Desktop/wdl-tutorials/data/ref/human_g1k_b37_20.dict")
        RefDict_og = "human_g1k_b37_20.dict"
        RefFasta = toil.importFile("file:///home/lifeisaboutfishtacos/Desktop/wdl-tutorials/data/ref/human_g1k_b37_20.fasta")
        RefFasta_og = "human_g1k_b37_20.fasta"

        # Output Variables

        job0 = Job.wrapJobFn(initialize_jobs)
        job1 = Job.wrapJobFn(haplotypeCaller, GATK, GATK_og, RefFasta, RefFasta_og, RefIndex, RefIndex_og, RefDict, RefDict_og, sampleName, inputBAM, inputBAM_og, bamIndex, bamIndex_og)

        job0 = job0.encapsulate()
        job0.addChild(job1)

        toil.start(job0)

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



def mapping(job, fastq_files, reference_file, trimming_length):

    job.fileStore.logToMaster("mapping")
    start = time.time()
    
    tempDir = job.fileStore.getLocalTempDir()
    
    try:
        os.makedirs(tempDir + '/execution')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    try:
        reference_file_fs = job.fileStore.readGlobalFile(reference_file[0], userPath=os.path.join(tempDir, reference_file[1]))
    except:
        reference_file_fs = os.path.join(tempDir, reference_file[1])
    
    
    fastq_files_list = []
    for i in fastq_files:
        try:
            j = job.fileStore.readGlobalFile(i[0], userPath=os.path.join(tempDir, i[1]))
            fastq_files_list.append("/root/" + i[1])
        except:
            j = os.path.join(tempDir, i[1])
            fastq_files_list.append("/root/" + i[1])
    fastq_files_sep = " ".join(fastq_files_list)

    command0 = '''
        python /image_software/pipeline-container/src/encode_map.py \
        '''
    command1 = "/root/" + reference_file[1]
    command2 = ''' \
        '''
    command3 = trimming_length
    command4 = ''' \
        '''
    command5 = fastq_files_sep
    command6 = '''
    '''

    cmd = command0 + command1 + command2 + command3 + command4 + command5 + command6

    generate_docker_bashscript_file(temp_dir=tempDir, docker_dir='/root', globs=['*.sai', '*.gz', 'mapping.log', 'mapping.json'], cmd=cmd, job_name='mapping')


    apiDockerCall(job, 
                  image="quay.io/encode-dcc/mapping:v1.0", 
                  working_dir=tempDir, 
                  parameters=["/root/mapping_script.sh"], 
                  entrypoint="/bin/bash", 
                  volumes={tempDir: {"bind": "/root"}})
    
    

    sai_files = []
    for x in recursive_glob(job, directoryname=tempDir, glob_pattern="*.sai"):
        output_file = job.fileStore.writeGlobalFile(x)
        output_filename = os.path.basename(x)
        job.fileStore.exportFile(output_file, "file:///home/quokka/Desktop/fretoil/toil/src/toil/wdl/" + output_filename)
        sai_files.append((output_file, output_filename))
    
    


    unmapped_files = []
    for x in recursive_glob(job, directoryname=tempDir, glob_pattern="*.gz"):
        output_file = job.fileStore.writeGlobalFile(x)
        output_filename = os.path.basename(x)
        job.fileStore.exportFile(output_file, "file:///home/quokka/Desktop/fretoil/toil/src/toil/wdl/" + output_filename)
        unmapped_files.append((output_file, output_filename))
    
    


    mapping_log_il = []
    for x in recursive_glob(job, directoryname=tempDir, glob_pattern="mapping.log"):
        output_file = job.fileStore.writeGlobalFile(x)
        output_filename = os.path.basename(x)
        job.fileStore.exportFile(output_file, "file:///home/quokka/Desktop/fretoil/toil/src/toil/wdl/" + output_filename)
        mapping_log_il.append((output_file, output_filename))
    
    

    mapping_log = mapping_log_il[0]
    

    mapping_results_il = []
    for x in recursive_glob(job, directoryname=tempDir, glob_pattern="mapping.json"):
        output_file = job.fileStore.writeGlobalFile(x)
        output_filename = os.path.basename(x)
        job.fileStore.exportFile(output_file, "file:///home/quokka/Desktop/fretoil/toil/src/toil/wdl/" + output_filename)
        mapping_results_il.append((output_file, output_filename))
    
    

    mapping_results = mapping_results_il[0]
    
    rvDict = {"sai_files": sai_files, "unmapped_files": unmapped_files, "mapping_log": mapping_log, "mapping_results": mapping_results}


    end = time.time()
    with open("/home/quokka/Desktop/fretoil/toil/src/toil/wdl/wdl-stats.log", "a+") as f:
        f.write(str("mapping") + " now being run.")
        f.write("\n\n")
        f.write("Outputs:\n")
        for rv in rvDict:
            f.write(str(rv) + ": " + str(rvDict[rv]))
            f.write("\n")
        f.write("Total runtime: %2.2f sec" % (end - start))
        f.write("\n\n")
    
    return rvDict



def post_processing(job, initial_fastqs, reference_file, sai_files, trimming_length, unmapped_fastqs):

    job.fileStore.logToMaster("post_processing")
    start = time.time()
    
    tempDir = job.fileStore.getLocalTempDir()
    
    try:
        os.makedirs(tempDir + '/execution')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    try:
        reference_file_fs = job.fileStore.readGlobalFile(reference_file[0], userPath=os.path.join(tempDir, reference_file[1]))
    except:
        reference_file_fs = os.path.join(tempDir, reference_file[1])
    
    
    unmapped_fastqs_list = []
    for i in unmapped_fastqs["unmapped_files"]:
        try:
            j = job.fileStore.readGlobalFile(i[0], userPath=os.path.join(tempDir, i[1]))
            unmapped_fastqs_list.append("/root/" + i[1])
        except:
            j = os.path.join(tempDir, i[1])
            unmapped_fastqs_list.append("/root/" + i[1])
    unmapped_fastqs_sep = " ".join(unmapped_fastqs_list)

    sai_files_list = []
    for i in sai_files["sai_files"]:
        try:
            j = job.fileStore.readGlobalFile(i[0], userPath=os.path.join(tempDir, i[1]))
            sai_files_list.append("/root/" + i[1])
        except:
            j = os.path.join(tempDir, i[1])
            sai_files_list.append("/root/" + i[1])
    sai_files_sep = " ".join(sai_files_list)

    initial_fastqs_list = []
    for i in initial_fastqs:
        try:
            j = job.fileStore.readGlobalFile(i[0], userPath=os.path.join(tempDir, i[1]))
            initial_fastqs_list.append("/root/" + i[1])
        except:
            j = os.path.join(tempDir, i[1])
            initial_fastqs_list.append("/root/" + i[1])
    initial_fastqs_sep = " ".join(initial_fastqs_list)

    command7 = '''

        python /image_software/pipeline-container/src/encode_post_map.py \
         '''
    command8 = trimming_length
    command9 = ''' \
         '''
    command10 = "/root/" + reference_file[1]
    command11 = ''' \
         '''
    command12 = unmapped_fastqs_sep
    command13 = ''' \
         '''
    command14 = sai_files_sep
    command15 = ''' \
         '''
    command16 = initial_fastqs_sep
    command17 = '''
    '''

    cmd = command7 + command8 + command9 + command10 + command11 + command12 + command13 + command14 + command15 + command16 + command17

    generate_docker_bashscript_file(temp_dir=tempDir, docker_dir='/root', globs=['*.raw.srt.bam', '*.raw.srt.bam.flagstat.qc', 'post_mapping.log', 'post_mapping.json'], cmd=cmd, job_name='post_processing')


    apiDockerCall(job, 
                  image="quay.io/encode-dcc/post_mapping:v1.0", 
                  working_dir=tempDir, 
                  parameters=["/root/post_processing_script.sh"], 
                  entrypoint="/bin/bash", 
                  volumes={tempDir: {"bind": "/root"}})
    
    

    unfiltered_bam_il = []
    for x in recursive_glob(job, directoryname=tempDir, glob_pattern="*.raw.srt.bam"):
        output_file = job.fileStore.writeGlobalFile(x)
        output_filename = os.path.basename(x)
        job.fileStore.exportFile(output_file, "file:///home/quokka/Desktop/fretoil/toil/src/toil/wdl/" + output_filename)
        unfiltered_bam_il.append((output_file, output_filename))
    
    

    unfiltered_bam = unfiltered_bam_il[0]
    

    unfiltered_flagstats_il = []
    for x in recursive_glob(job, directoryname=tempDir, glob_pattern="*.raw.srt.bam.flagstat.qc"):
        output_file = job.fileStore.writeGlobalFile(x)
        output_filename = os.path.basename(x)
        job.fileStore.exportFile(output_file, "file:///home/quokka/Desktop/fretoil/toil/src/toil/wdl/" + output_filename)
        unfiltered_flagstats_il.append((output_file, output_filename))
    
    

    unfiltered_flagstats = unfiltered_flagstats_il[0]
    

    post_mapping_log_il = []
    for x in recursive_glob(job, directoryname=tempDir, glob_pattern="post_mapping.log"):
        output_file = job.fileStore.writeGlobalFile(x)
        output_filename = os.path.basename(x)
        job.fileStore.exportFile(output_file, "file:///home/quokka/Desktop/fretoil/toil/src/toil/wdl/" + output_filename)
        post_mapping_log_il.append((output_file, output_filename))
    
    

    post_mapping_log = post_mapping_log_il[0]
    

    post_mapping_results_il = []
    for x in recursive_glob(job, directoryname=tempDir, glob_pattern="post_mapping.json"):
        output_file = job.fileStore.writeGlobalFile(x)
        output_filename = os.path.basename(x)
        job.fileStore.exportFile(output_file, "file:///home/quokka/Desktop/fretoil/toil/src/toil/wdl/" + output_filename)
        post_mapping_results_il.append((output_file, output_filename))
    
    

    post_mapping_results = post_mapping_results_il[0]
    
    rvDict = {"unfiltered_bam": unfiltered_bam, "unfiltered_flagstats": unfiltered_flagstats, "post_mapping_log": post_mapping_log, "post_mapping_results": post_mapping_results}


    end = time.time()
    with open("/home/quokka/Desktop/fretoil/toil/src/toil/wdl/wdl-stats.log", "a+") as f:
        f.write(str("post_processing") + " now being run.")
        f.write("\n\n")
        f.write("Outputs:\n")
        for rv in rvDict:
            f.write(str(rv) + ": " + str(rvDict[rv]))
            f.write("\n")
        f.write("Total runtime: %2.2f sec" % (end - start))
        f.write("\n\n")
    
    return rvDict



def filter_qc(job, bam_file, fastq_files):

    job.fileStore.logToMaster("filter_qc")
    start = time.time()
    
    tempDir = job.fileStore.getLocalTempDir()
    
    try:
        os.makedirs(tempDir + '/execution')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    try:
        bam_file_fs = job.fileStore.readGlobalFile(bam_file["unfiltered_bam"][0], userPath=os.path.join(tempDir, bam_file["unfiltered_bam"][1]))
    except:
        bam_file_fs = os.path.join(tempDir, bam_file["unfiltered_bam"][1])
    
    
    fastq_files_list = []
    for i in fastq_files:
        try:
            j = job.fileStore.readGlobalFile(i[0], userPath=os.path.join(tempDir, i[1]))
            fastq_files_list.append("/root/" + i[1])
        except:
            j = os.path.join(tempDir, i[1])
            fastq_files_list.append("/root/" + i[1])
    fastq_files_sep = " ".join(fastq_files_list)

    command18 = '''

        python /image_software/pipeline-container/src/filter_qc.py \
         '''
    command19 = "/root/" + bam_file["unfiltered_bam"][1]
    command20 = ''' \
         '''
    command21 = fastq_files_sep
    command22 = '''
    '''

    cmd = command18 + command19 + command20 + command21 + command22

    generate_docker_bashscript_file(temp_dir=tempDir, docker_dir='/root', globs=['*.dup.qc', '*final.bam', '*final.bam.bai', '*final.flagstat.qc', '*.pbc.qc', 'filter_qc.log', 'filter_qc.json'], cmd=cmd, job_name='filter_qc')


    apiDockerCall(job, 
                  image="quay.io/encode-dcc/filter:v1.0", 
                  working_dir=tempDir, 
                  parameters=["/root/filter_qc_script.sh"], 
                  entrypoint="/bin/bash", 
                  volumes={tempDir: {"bind": "/root"}})
    
    

    dup_file_qc_il = []
    for x in recursive_glob(job, directoryname=tempDir, glob_pattern="*.dup.qc"):
        output_file = job.fileStore.writeGlobalFile(x)
        output_filename = os.path.basename(x)
        job.fileStore.exportFile(output_file, "file:///home/quokka/Desktop/fretoil/toil/src/toil/wdl/" + output_filename)
        dup_file_qc_il.append((output_file, output_filename))
    
    

    dup_file_qc = dup_file_qc_il[0]
    

    filtered_bam_il = []
    for x in recursive_glob(job, directoryname=tempDir, glob_pattern="*final.bam"):
        output_file = job.fileStore.writeGlobalFile(x)
        output_filename = os.path.basename(x)
        job.fileStore.exportFile(output_file, "file:///home/quokka/Desktop/fretoil/toil/src/toil/wdl/" + output_filename)
        filtered_bam_il.append((output_file, output_filename))
    
    

    filtered_bam = filtered_bam_il[0]
    

    filtered_bam_bai_il = []
    for x in recursive_glob(job, directoryname=tempDir, glob_pattern="*final.bam.bai"):
        output_file = job.fileStore.writeGlobalFile(x)
        output_filename = os.path.basename(x)
        job.fileStore.exportFile(output_file, "file:///home/quokka/Desktop/fretoil/toil/src/toil/wdl/" + output_filename)
        filtered_bam_bai_il.append((output_file, output_filename))
    
    

    filtered_bam_bai = filtered_bam_bai_il[0]
    

    filtered_map_stats_il = []
    for x in recursive_glob(job, directoryname=tempDir, glob_pattern="*final.flagstat.qc"):
        output_file = job.fileStore.writeGlobalFile(x)
        output_filename = os.path.basename(x)
        job.fileStore.exportFile(output_file, "file:///home/quokka/Desktop/fretoil/toil/src/toil/wdl/" + output_filename)
        filtered_map_stats_il.append((output_file, output_filename))
    
    

    filtered_map_stats = filtered_map_stats_il[0]
    

    pbc_file_qc_il = []
    for x in recursive_glob(job, directoryname=tempDir, glob_pattern="*.pbc.qc"):
        output_file = job.fileStore.writeGlobalFile(x)
        output_filename = os.path.basename(x)
        job.fileStore.exportFile(output_file, "file:///home/quokka/Desktop/fretoil/toil/src/toil/wdl/" + output_filename)
        pbc_file_qc_il.append((output_file, output_filename))
    
    

    pbc_file_qc = pbc_file_qc_il[0]
    

    filter_qc_log_il = []
    for x in recursive_glob(job, directoryname=tempDir, glob_pattern="filter_qc.log"):
        output_file = job.fileStore.writeGlobalFile(x)
        output_filename = os.path.basename(x)
        job.fileStore.exportFile(output_file, "file:///home/quokka/Desktop/fretoil/toil/src/toil/wdl/" + output_filename)
        filter_qc_log_il.append((output_file, output_filename))
    
    

    filter_qc_log = filter_qc_log_il[0]
    

    filter_qc_results_il = []
    for x in recursive_glob(job, directoryname=tempDir, glob_pattern="filter_qc.json"):
        output_file = job.fileStore.writeGlobalFile(x)
        output_filename = os.path.basename(x)
        job.fileStore.exportFile(output_file, "file:///home/quokka/Desktop/fretoil/toil/src/toil/wdl/" + output_filename)
        filter_qc_results_il.append((output_file, output_filename))
    
    

    filter_qc_results = filter_qc_results_il[0]
    
    rvDict = {"dup_file_qc": dup_file_qc, "filtered_bam": filtered_bam, "filtered_bam_bai": filtered_bam_bai, "filtered_map_stats": filtered_map_stats, "pbc_file_qc": pbc_file_qc, "filter_qc_log": filter_qc_log, "filter_qc_results": filter_qc_results}


    end = time.time()
    with open("/home/quokka/Desktop/fretoil/toil/src/toil/wdl/wdl-stats.log", "a+") as f:
        f.write(str("filter_qc") + " now being run.")
        f.write("\n\n")
        f.write("Outputs:\n")
        for rv in rvDict:
            f.write(str(rv) + ": " + str(rvDict[rv]))
            f.write("\n")
        f.write("Total runtime: %2.2f sec" % (end - start))
        f.write("\n\n")
    
    return rvDict



def xcor(job, bam_file, fastq_files):

    job.fileStore.logToMaster("xcor")
    start = time.time()
    
    tempDir = job.fileStore.getLocalTempDir()
    
    try:
        os.makedirs(tempDir + '/execution')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    try:
        bam_file_fs = job.fileStore.readGlobalFile(bam_file["filtered_bam"][0], userPath=os.path.join(tempDir, bam_file["filtered_bam"][1]))
    except:
        bam_file_fs = os.path.join(tempDir, bam_file["filtered_bam"][1])
    
    
    fastq_files_list = []
    for i in fastq_files:
        try:
            j = job.fileStore.readGlobalFile(i[0], userPath=os.path.join(tempDir, i[1]))
            fastq_files_list.append("/root/" + i[1])
        except:
            j = os.path.join(tempDir, i[1])
            fastq_files_list.append("/root/" + i[1])
    fastq_files_sep = " ".join(fastq_files_list)

    command23 = '''

        python /image_software/pipeline-container/src/xcor.py \
         '''
    command24 = "/root/" + bam_file["filtered_bam"][1]
    command25 = ''' \
         '''
    command26 = fastq_files_sep
    command27 = '''
    '''

    cmd = command23 + command24 + command25 + command26 + command27

    generate_docker_bashscript_file(temp_dir=tempDir, docker_dir='/root', globs=['*.cc.qc', '*.cc.plot.pdf', '*tagAlign.gz', 'xcor.log', 'xcor.json'], cmd=cmd, job_name='xcor')


    apiDockerCall(job, 
                  image="quay.io/encode-dcc/xcor:v1.0", 
                  working_dir=tempDir, 
                  parameters=["/root/xcor_script.sh"], 
                  entrypoint="/bin/bash", 
                  volumes={tempDir: {"bind": "/root"}})
    
    

    cc_file_il = []
    for x in recursive_glob(job, directoryname=tempDir, glob_pattern="*.cc.qc"):
        output_file = job.fileStore.writeGlobalFile(x)
        output_filename = os.path.basename(x)
        job.fileStore.exportFile(output_file, "file:///home/quokka/Desktop/fretoil/toil/src/toil/wdl/" + output_filename)
        cc_file_il.append((output_file, output_filename))
    
    

    cc_file = cc_file_il[0]
    

    cc_plot_il = []
    for x in recursive_glob(job, directoryname=tempDir, glob_pattern="*.cc.plot.pdf"):
        output_file = job.fileStore.writeGlobalFile(x)
        output_filename = os.path.basename(x)
        job.fileStore.exportFile(output_file, "file:///home/quokka/Desktop/fretoil/toil/src/toil/wdl/" + output_filename)
        cc_plot_il.append((output_file, output_filename))
    
    

    cc_plot = cc_plot_il[0]
    

    tag_align = []
    for x in recursive_glob(job, directoryname=tempDir, glob_pattern="*tagAlign.gz"):
        output_file = job.fileStore.writeGlobalFile(x)
        output_filename = os.path.basename(x)
        job.fileStore.exportFile(output_file, "file:///home/quokka/Desktop/fretoil/toil/src/toil/wdl/" + output_filename)
        tag_align.append((output_file, output_filename))
    
    


    xcor_log_il = []
    for x in recursive_glob(job, directoryname=tempDir, glob_pattern="xcor.log"):
        output_file = job.fileStore.writeGlobalFile(x)
        output_filename = os.path.basename(x)
        job.fileStore.exportFile(output_file, "file:///home/quokka/Desktop/fretoil/toil/src/toil/wdl/" + output_filename)
        xcor_log_il.append((output_file, output_filename))
    
    

    xcor_log = xcor_log_il[0]
    

    xcor_results_il = []
    for x in recursive_glob(job, directoryname=tempDir, glob_pattern="xcor.json"):
        output_file = job.fileStore.writeGlobalFile(x)
        output_filename = os.path.basename(x)
        job.fileStore.exportFile(output_file, "file:///home/quokka/Desktop/fretoil/toil/src/toil/wdl/" + output_filename)
        xcor_results_il.append((output_file, output_filename))
    
    

    xcor_results = xcor_results_il[0]
    
    rvDict = {"cc_file": cc_file, "cc_plot": cc_plot, "tag_align": tag_align, "xcor_log": xcor_log, "xcor_results": xcor_results}


    end = time.time()
    with open("/home/quokka/Desktop/fretoil/toil/src/toil/wdl/wdl-stats.log", "a+") as f:
        f.write(str("xcor") + " now being run.")
        f.write("\n\n")
        f.write("Outputs:\n")
        for rv in rvDict:
            f.write(str(rv) + ": " + str(rvDict[rv]))
            f.write("\n")
        f.write("Total runtime: %2.2f sec" % (end - start))
        f.write("\n\n")
    
    return rvDict



def gather_the_outputs(job, unfiltered_bam, filtered_bam, unfiltered_flagstat, filtered_flagstat, dup_qc, pbc_qc, mapping_log, post_mapping_log, filter_qc_log, xcor_log, mapping_results, post_mapping_results, filter_qc_results, xcor_results, cc, cc_pdf, tag_align):

    job.fileStore.logToMaster("gather_the_outputs")
    start = time.time()
    
    tempDir = job.fileStore.getLocalTempDir()
    
    

    try:
        unfiltered_bam_fs = job.fileStore.readGlobalFile(unfiltered_bam["unfiltered_bam"][0], userPath=os.path.join(tempDir, unfiltered_bam["unfiltered_bam"][1]))
    except:
        unfiltered_bam_fs = os.path.join(tempDir, unfiltered_bam["unfiltered_bam"][1])
    
    

    try:
        filtered_bam_fs = job.fileStore.readGlobalFile(filtered_bam["filtered_bam"][0], userPath=os.path.join(tempDir, filtered_bam["filtered_bam"][1]))
    except:
        filtered_bam_fs = os.path.join(tempDir, filtered_bam["filtered_bam"][1])
    
    

    try:
        unfiltered_flagstat_fs = job.fileStore.readGlobalFile(unfiltered_flagstat["unfiltered_flagstats"][0], userPath=os.path.join(tempDir, unfiltered_flagstat["unfiltered_flagstats"][1]))
    except:
        unfiltered_flagstat_fs = os.path.join(tempDir, unfiltered_flagstat["unfiltered_flagstats"][1])
    
    

    try:
        filtered_flagstat_fs = job.fileStore.readGlobalFile(filtered_flagstat["filtered_map_stats"][0], userPath=os.path.join(tempDir, filtered_flagstat["filtered_map_stats"][1]))
    except:
        filtered_flagstat_fs = os.path.join(tempDir, filtered_flagstat["filtered_map_stats"][1])
    
    

    try:
        dup_qc_fs = job.fileStore.readGlobalFile(dup_qc["dup_file_qc"][0], userPath=os.path.join(tempDir, dup_qc["dup_file_qc"][1]))
    except:
        dup_qc_fs = os.path.join(tempDir, dup_qc["dup_file_qc"][1])
    
    

    try:
        pbc_qc_fs = job.fileStore.readGlobalFile(pbc_qc["pbc_file_qc"][0], userPath=os.path.join(tempDir, pbc_qc["pbc_file_qc"][1]))
    except:
        pbc_qc_fs = os.path.join(tempDir, pbc_qc["pbc_file_qc"][1])
    
    

    try:
        mapping_log_fs = job.fileStore.readGlobalFile(mapping_log["mapping_log"][0], userPath=os.path.join(tempDir, mapping_log["mapping_log"][1]))
    except:
        mapping_log_fs = os.path.join(tempDir, mapping_log["mapping_log"][1])
    
    

    try:
        post_mapping_log_fs = job.fileStore.readGlobalFile(post_mapping_log["post_mapping_log"][0], userPath=os.path.join(tempDir, post_mapping_log["post_mapping_log"][1]))
    except:
        post_mapping_log_fs = os.path.join(tempDir, post_mapping_log["post_mapping_log"][1])
    
    

    try:
        filter_qc_log_fs = job.fileStore.readGlobalFile(filter_qc_log["filter_qc_log"][0], userPath=os.path.join(tempDir, filter_qc_log["filter_qc_log"][1]))
    except:
        filter_qc_log_fs = os.path.join(tempDir, filter_qc_log["filter_qc_log"][1])
    
    

    try:
        xcor_log_fs = job.fileStore.readGlobalFile(xcor_log["xcor_log"][0], userPath=os.path.join(tempDir, xcor_log["xcor_log"][1]))
    except:
        xcor_log_fs = os.path.join(tempDir, xcor_log["xcor_log"][1])
    
    

    try:
        mapping_results_fs = job.fileStore.readGlobalFile(mapping_results["mapping_results"][0], userPath=os.path.join(tempDir, mapping_results["mapping_results"][1]))
    except:
        mapping_results_fs = os.path.join(tempDir, mapping_results["mapping_results"][1])
    
    

    try:
        post_mapping_results_fs = job.fileStore.readGlobalFile(post_mapping_results["post_mapping_results"][0], userPath=os.path.join(tempDir, post_mapping_results["post_mapping_results"][1]))
    except:
        post_mapping_results_fs = os.path.join(tempDir, post_mapping_results["post_mapping_results"][1])
    
    

    try:
        filter_qc_results_fs = job.fileStore.readGlobalFile(filter_qc_results["filter_qc_results"][0], userPath=os.path.join(tempDir, filter_qc_results["filter_qc_results"][1]))
    except:
        filter_qc_results_fs = os.path.join(tempDir, filter_qc_results["filter_qc_results"][1])
    
    

    try:
        xcor_results_fs = job.fileStore.readGlobalFile(xcor_results["xcor_results"][0], userPath=os.path.join(tempDir, xcor_results["xcor_results"][1]))
    except:
        xcor_results_fs = os.path.join(tempDir, xcor_results["xcor_results"][1])
    
    

    try:
        cc_fs = job.fileStore.readGlobalFile(cc["cc_file"][0], userPath=os.path.join(tempDir, cc["cc_file"][1]))
    except:
        cc_fs = os.path.join(tempDir, cc["cc_file"][1])
    
    

    try:
        cc_pdf_fs = job.fileStore.readGlobalFile(cc_pdf["cc_plot"][0], userPath=os.path.join(tempDir, cc_pdf["cc_plot"][1]))
    except:
        cc_pdf_fs = os.path.join(tempDir, cc_pdf["cc_plot"][1])
    
    
    tag_align_list = []
    for i in tag_align["tag_align"]:
        try:
            j = job.fileStore.readGlobalFile(i[0], userPath=os.path.join(tempDir, i[1]))
            tag_align_list.append(j)
        except:
            j = os.path.join(tempDir, i[1])
            tag_align_list.append(j)
    tag_align_sep = " ".join(tag_align_list)

    command28 = '''
        cp '''
    command29 = unfiltered_bam_fs
    command30 = ''' .
        cp '''
    command31 = filtered_bam_fs
    command32 = ''' .
        cp '''
    command33 = unfiltered_flagstat_fs
    command34 = ''' .
        cp '''
    command35 = filtered_flagstat_fs
    command36 = ''' .
        cp '''
    command37 = dup_qc_fs
    command38 = ''' .
        cp '''
    command39 = pbc_qc_fs
    command40 = ''' .
        cp '''
    command41 = mapping_log_fs
    command42 = ''' .
        cp '''
    command43 = post_mapping_log_fs
    command44 = ''' .
        cp '''
    command45 = filter_qc_log_fs
    command46 = ''' .
        cp '''
    command47 = xcor_log_fs
    command48 = ''' .
        cp '''
    command49 = mapping_results_fs
    command50 = ''' .
        cp '''
    command51 = post_mapping_results_fs
    command52 = ''' .
        cp '''
    command53 = filter_qc_results_fs
    command54 = ''' .
        cp '''
    command55 = xcor_results_fs
    command56 = ''' .
        cp '''
    command57 = cc_fs
    command58 = ''' .
        cp '''
    command59 = cc_pdf_fs
    command60 = ''' .
        cp '''
    command61 = tag_align_sep
    command62 = ''' .
    '''

    cmd = command28 + command29 + command30 + command31 + command32 + command33 + command34 + command35 + command36 + command37 + command38 + command39 + command40 + command41 + command42 + command43 + command44 + command45 + command46 + command47 + command48 + command49 + command50 + command51 + command52 + command53 + command54 + command55 + command56 + command57 + command58 + command59 + command60 + command61 + command62


    this_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    this_process.communicate()
    


if __name__=="__main__":
    options = Job.Runner.getDefaultOptions("./toilWorkflowRun")
    with Toil(options) as toil:
        start = time.time()
        with open("/home/quokka/Desktop/fretoil/toil/src/toil/wdl/wdl-stats.log", "a+") as f:
            f.write("Starting WDL Job @ " + str(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())) + "\n\n")




        # JSON Variables
        fastqs0 = toil.importFile("file:///home/quokka/Desktop/fretoil/toil/src/toil/test/wdl/ENCODE_data/ENCFF000VOL_chr21.fq.gz")
        fastqs0_preserveThisFilename = "ENCFF000VOL_chr21.fq.gz"
        fastqs = [(fastqs0, fastqs0_preserveThisFilename)]
        trimming_parameter = "native"
        reference0 = toil.importFile("file:///home/quokka/Desktop/fretoil/toil/src/toil/test/wdl/ENCODE_data/reference/GRCh38_chr21_bwa.tar.gz")
        reference0_preserveThisFilename = "GRCh38_chr21_bwa.tar.gz"
        reference = (reference0, reference0_preserveThisFilename)


        # TSV Variables


        # CSV Variables

        job0 = Job.wrapJobFn(initialize_jobs)
        job1 = Job.wrapJobFn(mapping, fastq_files=fastqs, reference_file=reference, trimming_length=trimming_parameter)
        job2 = Job.wrapJobFn(post_processing, initial_fastqs=fastqs, reference_file=reference, sai_files=job1.rv(), trimming_length=trimming_parameter, unmapped_fastqs=job1.rv())
        job3 = Job.wrapJobFn(filter_qc, bam_file=job2.rv(), fastq_files=fastqs)
        job4 = Job.wrapJobFn(xcor, bam_file=job3.rv(), fastq_files=fastqs)
        job5 = Job.wrapJobFn(gather_the_outputs, unfiltered_bam=job2.rv(), filtered_bam=job3.rv(), unfiltered_flagstat=job2.rv(), filtered_flagstat=job3.rv(), dup_qc=job3.rv(), pbc_qc=job3.rv(), mapping_log=job1.rv(), post_mapping_log=job2.rv(), filter_qc_log=job3.rv(), xcor_log=job4.rv(), mapping_results=job1.rv(), post_mapping_results=job2.rv(), filter_qc_results=job3.rv(), xcor_results=job4.rv(), cc=job4.rv(), cc_pdf=job4.rv(), tag_align=job4.rv())

        job0.addChild(job1)

        toil.start(job0)


        end = time.time()
        with open("/home/quokka/Desktop/fretoil/toil/src/toil/wdl/wdl-stats.log", "a+") as f:
            f.write("Ending WDL Job @ " + str(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())))
            f.write("\n")
            f.write("Total runtime: %2.2f sec" % (end - start))
            f.write("\n\n")
            f.write("\n" + "-"*80 + "\n")

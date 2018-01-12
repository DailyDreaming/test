.. _commandRef:

.. _workflowOptions:

Toil Workflow Options and Command Line Interface
================================================

The ``toil`` CLI supports the following commands as arguments:

	``status`` - Reports runtime and resource usage for all jobs in a specified jobstore

	``stats`` - Inspects a job store to see which jobs have failed, run successfully, etc.

	``destroy-cluster`` - For autoscaling.  Terminates the specified cluster and associated resources.

	``launch-cluster`` - For autoscaling.  This is used to launch a toil leader instance with the specified provisioner.

	``rsync-cluster`` - For autoscaling.  Used to transfer files to a cluster launched with ``toil launch-cluster``.

	``kill`` - Kills any running jobs trees in a rogue toil.

	``clean`` - Delete the job store used by a previous Toil workflow invocation.

	``ssh-cluster`` - SSHs into the toil appliance container running on the leader of the cluster.

Status
------

To use the status command, a workflow must first be run using the ``--stats`` option.

An example of this would be running the following::

    toil discoverfiles.py file:my-jobstore --stats

Where ``discoverfiles.py`` is the following:

.. code-block:: python

    import subprocess
    from toil.common import Toil
    from toil.job import Job

    class discoverFiles(Job):
        """Views files at a specified path using ls."""
        def __init__(self, path, *args, **kwargs):
            self.path = path
            super(discoverFiles, self).__init__(*args, **kwargs)

        def run(self, fileStore):
            subprocess.check_call(["ls", self.path])

    def main():
        options = Job.Runner.getDefaultArgumentParser().parse_args()

        job1 = discoverFiles(path="/", displayName='sysFiles')
        job2 = discoverFiles(path="/home/lifeisaboutfishtacos", displayName='userFiles')
        job3 = discoverFiles(path="/home/andbeeftacos")

        job1.addChild(job2)
        job2.addChild(job3)

        with Toil(options) as toil:
            if not toil.options.restart:
                toil.start(job1)
            else:
                toil.restart()

    if __name__ == '__main__':
        main()

Notice the ``displayName`` key, which can rename a job, giving it an alias when it is finally displayed in stats.
Running this workflow file should record three job names then: ``sysFiles`` (job1), ``userFiles`` (job2), and ``discoverFiles`` (job3).
To see the runtime and resources used for each job when it was run, type::

    toil stats file:my-jobstore

This should output the following:

.. code-block:: python

    Batch System: singleMachine
    Default Cores: 1  Default Memory: 2097152K
    Max Cores: 9.22337e+18
    Total Clock: 0.56  Total Runtime: 1.01
    Worker
        Count |                                    Time* |                                    Clock |                                     Wait |                                   Memory
            n |      min    med*     ave     max   total |      min     med     ave     max   total |      min     med     ave     max   total |      min     med     ave     max   total
            1 |     0.14    0.14    0.14    0.14    0.14 |     0.13    0.13    0.13    0.13    0.13 |     0.01    0.01    0.01    0.01    0.01 |      76K     76K     76K     76K     76K
    Job
     Worker Jobs  |     min    med    ave    max
                  |       3      3      3      3
        Count |                                    Time* |                                    Clock |                                     Wait |                                   Memory
            n |      min    med*     ave     max   total |      min     med     ave     max   total |      min     med     ave     max   total |      min     med     ave     max   total
            3 |     0.01    0.06    0.05    0.07    0.14 |     0.00    0.06    0.04    0.07    0.12 |     0.00    0.01    0.00    0.01    0.01 |      76K     76K     76K     76K    229K
     sysFiles
        Count |                                    Time* |                                    Clock |                                     Wait |                                   Memory
            n |      min    med*     ave     max   total |      min     med     ave     max   total |      min     med     ave     max   total |      min     med     ave     max   total
            1 |     0.01    0.01    0.01    0.01    0.01 |     0.00    0.00    0.00    0.00    0.00 |     0.01    0.01    0.01    0.01    0.01 |      76K     76K     76K     76K     76K
     userFiles
        Count |                                    Time* |                                    Clock |                                     Wait |                                   Memory
            n |      min    med*     ave     max   total |      min     med     ave     max   total |      min     med     ave     max   total |      min     med     ave     max   total
            1 |     0.06    0.06    0.06    0.06    0.06 |     0.06    0.06    0.06    0.06    0.06 |     0.01    0.01    0.01    0.01    0.01 |      76K     76K     76K     76K     76K
     discoverFiles
        Count |                                    Time* |                                    Clock |                                     Wait |                                   Memory
            n |      min    med*     ave     max   total |      min     med     ave     max   total |      min     med     ave     max   total |      min     med     ave     max   total
            1 |     0.07    0.07    0.07    0.07    0.07 |     0.07    0.07    0.07    0.07    0.07 |     0.00    0.00    0.00    0.00    0.00 |      76K     76K     76K     76K     76K


Toil also provides several command line options when running a toil script (see :ref:`running`),
or using Toil to run a CWL script. Many of these are described below.
For most Toil scripts, executing::

    $ python MY_TOIL_SCRIPT.py --help

will show this list of options.

It is also possible to set and manipulate the options described when invoking a
Toil workflow from within Python using :func:`toil.job.Job.Runner.getDefaultOptions`, e.g.

.. code-block:: python

    options = Job.Runner.getDefaultOptions("./toilWorkflow") # Get the options object
    options.logLevel = "INFO" # Set the log level to the info level.
    options.clean = "ALWAYS" # Always delete the jobStore after a run

    with Toil(options) as toil:
        toil.start(Job())  # Run the script


.. _loggingRef:

Logging
-------
Toil hides stdout and stderr by default except in case of job failure.
For more robust logging options (default is INFO), use ``--logDebug`` or more generally, use
``--logLevel=``, which may be set to either ``OFF`` (or ``CRITICAL``), ``ERROR``, ``WARN`` (or ``WARNING``),
``INFO`` or ``DEBUG``. Logs can be directed to a file with ``--logFile=``.

If large logfiles are a problem, ``--maxLogFileSize`` (in bytes) can be set as well as ``--rotatingLogging``, which
prevents logfiles from getting too large.

Stats
-----
The ``--stats`` argument records statistics about the Toil workflow in the job store. After a Toil run has finished,
the command ``toil stats <jobStore>`` can be used to return statistics about cpu, memory, job duration, and more.
The job store will never be deleted with ``--stats``, as it overrides ``--clean``.

Restart
-------
In the event of failure, Toil can resume the pipeline by adding the argument ``--restart`` and rerunning the
python script. Toil pipelines can even be edited and resumed which is useful for development or troubleshooting.

Clean
-----
If a Toil pipeline didn't finish successfully, or is using a variation of ``--clean``, the job store will exist
until it is deleted. ``toil clean <jobStore>`` ensures that all artifacts associated with a job store are removed.
This is particularly useful for deleting AWS job stores, which reserves an SDB domain as well as an S3 bucket.

The deletion of the job store can be modified by the ``--clean`` argument, and may be set to ``always``, ``onError``,
``never``, or ``onSuccess`` (default).

Temporary directories where jobs are running can also be saved from deletion using the ``--cleanWorkDir``, which has
the same options as ``--clean``.  This option should only be run when debugging, as intermediate jobs will fill up
disk space.


Batch system
------------

Toil supports several different batch systems using the ``--batchSystem`` argument.
More information in the :ref:`batchsysteminterface`.


Default cores, disk, and memory
-------------------------------

Toil uses resource requirements to intelligently schedule jobs. The defaults for cores (1), disk (2G), and memory (2G),
can all be changed using ``--defaultCores``, ``--defaultDisk``, and ``--defaultMemory``. Standard suffixes
like K, Ki, M, Mi, G or Gi are supported.


Job store
---------

Running toil scripts has one required positional argument: the job store.  The default job store is just a path
to where the user would like the job store to be created. To use the :ref:`quick start <quickstart>` example,
if you're on a node that has a large **/scratch** volume, you can specify the jobstore be created there by
executing: ``python HelloWorld.py /scratch/my-job-store``, or more explicitly,
``python HelloWorld.py file:/scratch/my-job-store``. Toil uses the colon as way to explicitly name what type of
job store the user would like. The other job store types are AWS (``aws:region-here:job-store-name``),
Azure (``azure:account-name-here:job-store-name``), and the experimental Google
job store (``google:projectID-here:job-store-name``). Different types of job store options can be
looked up in :ref:`jobStoreInterface`.

Miscellaneous
-------------
Here are some additional useful arguments that don't fit into another category.

* ``--workDir`` sets the location where temporary directories are created for running jobs.
* ``--retryCount`` sets the number of times to retry a job in case of failure. Useful for non-systemic failures like HTTP requests.
* ``--sseKey`` accepts a path to a 32-byte key that is used for server-side encryption when using the AWS job store.
* ``--cseKey`` accepts a path to a 256-bit key to be used for client-side encryption on Azure job store.
* ``--setEnv <NAME=VALUE>`` sets an environment variable early on in the worker

For implementation-specific flags for schedulers like timelimits, queues, accounts, etc.. An environment variable can be
defined before launching the Job, i.e:

.. code-block:: console

    export TOIL_SLURM_ARGS="-t 1:00:00 -q fatq"

Running Workflows with Services
-------------------------------

Toil supports jobs, or clusters of jobs, that run as *services* (see :ref:`serviceDev`) to other
*accessor* jobs. Example services include server databases or Apache Spark
Clusters. As service jobs exist to provide services to accessor jobs their
runtime is dependent on the concurrent running of their accessor jobs. The dependencies
between services and their accessor jobs can create potential deadlock scenarios,
where the running of the workflow hangs because only service jobs are being
run and their accessor jobs can not be scheduled because of too limited resources
to run both simultaneously. To cope with this situation Toil attempts to
schedule services and accessors intelligently, however to avoid a deadlock
with workflows running service jobs it is advisable to use the following parameters:

* ``--maxServiceJobs`` The maximum number of service jobs that can be run concurrently, excluding service jobs running on preemptable nodes.
* ``--maxPreemptableServiceJobs`` The maximum number of service jobs that can run concurrently on preemptable nodes.

Specifying these parameters so that at a maximum cluster size there will be
sufficient resources to run accessors in addition to services will ensure that
such a deadlock can not occur.

If too low a limit is specified then a deadlock can occur in which toil can
not schedule sufficient service jobs concurrently to complete the workflow.
Toil will detect this situation if it occurs and throw a
:class:`toil.DeadlockException` exception. Increasing the cluster size
and these limits will resolve the issue.

.. _clusterRef:


**Workflow was run with a fresh AWS EC2 (Ubuntu 16.04 Server) instance of type t2.2xlarge with one node, mounted with a 200 Gb EFS volume (EC2 wizard in firefox).**

Update the instance::

    sudo apt-get update
    sudo apt-get -y upgrade
    sudo apt-get -y dist-upgrade

Install docker::

    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt-get update
    apt-cache policy docker-ce
    sudo apt-get install -y docker-ce

Modify docker so that sudo is not needed for root::

    sudo usermod -aG docker ${USER}
    sudo su - ${USER}

Install pip, a virtualenv, the dev version of toil, and the requisite pip installs (cwltool, schema-salad, avro, synapse, and html5lib)::

    sudo apt install -y python-pip
    sudo pip install --upgrade pip
    sudo pip install virtualenv
    git clone https://github.com/BD2KGenomics/toil.git
    cd toil
    virtualenv --python /usr/bin/python2 dev
    source /home/ubuntu/toil/dev/bin/activate
    make prepare
    make develop
    pip install cwl-runner schema-salad==2.6.20170630075932 avro==1.8.1 cwltool==1.0.20170822192924 ruamel.yaml==0.14.12 --no-cache-dir
    pip install synapseclient --no-cache-dir
    pip install html5lib cwltest
    cd ..

I created a copy of my Synapse credentials in .synapseConfig::

    nano .synapseConfig

Download data from Synapse::

    synapse get -r syn9725771

I used the synapse get command to download the synapse-get and synapse-submit CWL tools as well as the JSON parameters to download data for the bcbio_NA12878-chr20 workflow, and then modify the get file::

    synapse get -r syn9689286
    synapse get -r syn9689284

Run the main bcbio workflow::

    cd NA12878-platinum-chr20-workflow
    toil-cwl-runner NA12878-platinum-chr20-workflowmain-NA12878-platinum-chr20.cwl NA12878-platinum-chr20-workflow/main-NA12878-platinum-chr20-samples.json

# A Custom Docker Image for Running the UCSC Genome Browser.
#
# This downloads the UCSC Genome Browser setup bash script and installs it within the docker image.
# It will then be accessible via 127.0.0.1:80 or 127.0.0.1:8000 if those ports are
# connected ("docker run -p 80:80" or "docker run -p 8000:8000").
#
# To build this image, run:
#
#   docker login
#   docker build . -t {docker_username}/{tag_key}:{tag_value}
#   docker push {docker_username}/{tag_key}:{tag_value}
#
# For example:
#
#   docker login
#   docker build . -t dailydreaming/genome_browser:latest 2>&1 | tee docker-build.log
#   docker push dailydreaming/genome_browser:latest
#
# Then, to run the Genome Browser (running locally on Ubuntu 18.04):
#
# docker run -p 80:80 dailydreaming/browser:latest
#
# Go to 127.0.0.1:8000 in a web browser and you should see the Genome Browser.
#
# Notes:
#
#  - To make this compatible with Terra we build on their suggested base image, "terra-jupyter-base":
#        https://github.com/DataBiosphere/terra-docker/blob/master/terra-jupyter-base/Dockerfile
#
#  - Terra only currently has support for: docker.io or gcr.io, so upload there (docker.io is free)
FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive
ENV APACHEDIR=/usr/local/apache
ENV MACHTYPE=x86_64

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y libssl-dev python3-dev python-dev git zip unzip wget build-essential apt-transport-https curl cmake rsync libpcap-dev libpng-dev ghostscript gmt r-base uuid-dev

ADD browserSetup.sh /tmp/browserSetup_raw.sh
RUN python3 -c 'f = open("/tmp/browserSetup_raw.sh"); new_content = f.read().replace("if $MYSQLADMIN -u root password $MYSQLROOTPWD;", "if /etc/init.d/mysql start && $MYSQLADMIN -u root password $MYSQLROOTPWD;"); f2 = open("/tmp/browserSetup.sh", "w"); f2.write(new_content); f.close(); f2.close()'
RUN bash /tmp/browserSetup.sh -b install; exit 0
RUN apt-get install -y apache2 mariadb-server python-mysqldb libmariadbclient-dev

RUN cd $APACHEDIR && git clone git://genome-source.soe.ucsc.edu/kent.git
RUN cd $APACHEDIR/kent && git checkout beta
ADD makefile ${APACHEDIR}/kent/src/makefile
ADD makefile.hubCheck ${APACHEDIR}/kent/src/hg/utils/hubCheck/makefile
ADD customFactory.c ${APACHEDIR}/kent/src/hg/lib/customFactory.c

ADD srcCompile.sh /tmp/srcCompile.sh
RUN bash /tmp/srcCompile.sh

EXPOSE 3306 33060 8000 8001 80 443 3333 873

ENTRYPOINT ["sh", "-c", "/etc/init.d/mysql start; apachectl -D FOREGROUND"]

#!/usr/bin/env bash

export SSLDIR=/usr/local/ssl/include
export MYSQLINC=/usr/include/mysql
export APACHEDIR=/usr/local/apache
export HTDOCDIR=$APACHEDIR/htdocs
export CGIBINDIR=$APACHEDIR/cgi-bin
export TRASHDIR=$APACHEDIR/trash
export MYSQLDIR=/var/lib/mysql
export CGI_BIN=$APACHEDIR/cgi-bin
export SAMTABIXDIR=$APACHEDIR/kent/samtabix
export USE_SAMTABIX=1
export SCRIPTS=$APACHEDIR/util
export BINDIR=$APACHEDIR/util
export PATH=$BINDIR:$PATH
mkdir -p $APACHEDIR/util

curl --remote-name https://www.openssl.org/source/openssl-1.0.2a.tar.gz
tar -xzvf openssl-1.0.2a.tar.gz
cd openssl-1.0.2a
./config --prefix=/usr/local/ssl --openssldir=/usr/local/ssl shared zlib
# make -j2 aborted with an error
make
make install
cd ..
rm openssl-1.0.2a.tar.gz

# get samtools patched for UCSC and compile it
cd $APACHEDIR/kent
if [ ! -d samtabix ]; then
 git clone http://genome-source.soe.ucsc.edu/samtabix.git
fi
cd samtabix
git pull
make

# compile the genome browser CGIs
cd $APACHEDIR/kent/src
make clean
make libs
# create jkweb.a
cd $APACHEDIR/kent/src/lib
make
# create stringify utility required by some makefiles
cd $APACHEDIR/kent/src/utils/stringify
make
# create pslCDnaFilter utility program
cd $APACHEDIR/kent/src/hg/pslCDnaFilter
make

cd $APACHEDIR/kent/src/hg
make compile
make install DESTDIR=

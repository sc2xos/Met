#!/bin/bash

SERVER=ftp.ptree.jaxa.jp
USER=ss.cpx.1103.yzm_gmail.com
PASS=SP+wari8

DLDIR=/home/soga/data/satelite/data
cd $DLDIR

TARGETDATE=$(date -d "$TARGETDATE" "+%Y%m%d")
yyyy=$(date -d "$TARGETDATE" "+%Y")
mm=$(date -d "$TARGETDATE" "+%m")
dd=$(date -d "$TARGETDATE" "+%d")

DIR=/jma/hsd/${yyyy}${mm}/${dd}/00
echo "########## Download from " $DIR " ##########"
#起動観測域
ftp -n <<-END
open $SERVER
user $USER $PASS
passive
cd $DIR
binary
prompt
mget PI_H08_${TARGETDATE}_0000*.png
cd ../06
mget PI_H08_${TARGETDATE}_0600*.png
cd ../12
mget PI_H08_${TARGETDATE}_1200*.png
cd ../18
mget PI_H08_${TARGETDATE}_1800*.png

END

for type in PLLTG PLLJP PGPFD
do
    mkdir -p ${type}/${TARGETDATE}
    mv PI_H08_${TARGETDATE}*${type}.png  ${DLDIR}/${type}/${TARGETDATE}/
done

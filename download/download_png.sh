#!/bin/bash

SERVER=ftp.ptree.jaxa.jp
USER=ss.cpx.1103.yzm_gmail.com
PASS=SP+wari8

DLDIR=/home/soga/data/satelite/data
cd $DLDIR

STARTDATE=20210801
ENDDATE=20210830
TEMPDATE=$STARTDATE
while [ 1 ] ; do

    yyyy=$(date -d "$TEMPDATE" "+%Y")
    mm=$(date -d "$TEMPDATE" "+%m")
    dd=$(date -d "$TEMPDATE" "+%d")
    
    DIR=/jma/hsd/${yyyy}${mm}/${dd}/00
    echo "########## Download " $DIR "Data ##########"
    #起動観測域
    ftp -n <<-END
    open $SERVER
    user $USER $PASS
    passive
    cd $DIR
    binary
    prompt
    mget PI_H08_${TEMPDATE}_0000*.png
    cd ../06
    mget PI_H08_${TEMPDATE}_0600*.png
    cd ../12
    mget PI_H08_${TEMPDATE}_1200*.png
    cd ../18
    mget PI_H08_${TEMPDATE}_1800*.png

END
    #データの移動
    #機動観測域
    mkdir -p PLLTG/$TEMPDATE
    mv PI_H08_${TEMPDATE}*PLLTG.png  $DLDIR/PLLTG/$TEMPDATE
    #ll -lR $DLDIR/PLLTG/$TEMPDATE
    #日本域
    mkdir -p PLLJP/$TEMPDATE
    mv PI_H08_${TEMPDATE}*PLLJP.png  $DLDIR/PLLJP/$TEMPDATE/
    #ll -lR $DLDIR/PLLJP/$TEMPDATE
    #全域
    mkdir -p PGPFD/$TEMPDATE
    mv PI_H08_${TEMPDATE}*PGPFD.png  $DLDIR/PGPFD/$TEMPDATE/
    #ll -lR $DLDIR/PGPFD/$TEMPDATE
    
    if [ $TEMPDATE = $ENDDATE ] ; then
        break
    fi
    
    TEMPDATE=`date -d "$TEMPDATE 1days" "+%Y%m%d"`
done

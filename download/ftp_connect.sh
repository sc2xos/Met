#!/bin/sh

#Address: ftp.ptree.jaxa.jp
#UID: ss.cpx.1103.yzm_gmail.com
#PW: SP+wari8

SERVER=ftp.ptree.jaxa.jp
USER=ss.cpx.1103.yzm_gmail.com
PASS=SP+wari8
FILE=

ftp -n <<END
open $SERVER
user $USER $PASS
passive
cd pub
prompt
mget *.txt
END

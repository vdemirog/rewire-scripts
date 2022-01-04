#!/bin/bash

while true;
do
        result=$(nc -l -p 8000)
        echo $result
        firstcmd=`echo "${result}" | head -1`
        secondcmd=`echo "${result}" | head -2 | tail -1`
        ./ndnconf.sh $firstcmd
        ./ndnconf.sh $secondcmd

done
exit 0


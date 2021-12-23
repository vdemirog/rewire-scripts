#!/bin/bash

DB_SENSORS="hum temp sound light movement hall"

while true;
do
    for k in $DB_SENSORS 
    do 
	    for i in $(seq 0 10);
	    do
            echo ndn:/example/$k$i | nc -q 1 10.0.3.18 7998
	        result=$(nc -l -p 7999)
            echo $result
            if [ "$result" == "cts" ] then  
                ./ndnconf.sh ndnpeek ndn:/example/$k$i                
                #ndnpeek -f -w 1000 -v ndn:/example/$k$i &
            fi
            sleep 2	
	    done
    done
done

exit 0

#while true;
#do
#    ndnpeek -f -w 1000 -v /content1
#done
#exit 0


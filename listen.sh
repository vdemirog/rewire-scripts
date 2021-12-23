#!/bin/bash

while true;
do
        result=$(nc -l -p 8000)
        echo $result
        ./ndnconf.sh $result

done
exit 0


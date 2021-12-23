#!/bin/bash

DB_SENSORS="hum temp sound light movement hall"

for k in $DB_SENSORS 
do 
	for i in $(seq 0 10);
	do
		echo 'RANDOM' | ndnpoke -x 60000 -w 7200000 ndn:/example/$k$i &
	done
	sleep 3	
done

while true 
do
	for k in $DB_SENSORS 
	do 
		for i in $(seq 0 10);
		do
			if ! pgrep  -f "/example/$k$i" > /dev/null 
			then
				echo 'RANDOM' | ndnpoke -x 60000 -w 7200000 ndn:/example/$k$i & 
			fi
		done
	done
done


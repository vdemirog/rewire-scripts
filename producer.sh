#!/bin/bash

# 150 content objects
content="1 2 3 4 5 6 7 8 9 10 11 12 38413 14 15 16 17 18 13 20 21 22 23 24 25 26 27 19 29 30 31 32 33 544 35 36 37 39 40 41 42 43 44 45 46 47 48 49 52 53 54 55 59 61 63 64 67 1092 69 70 71 72 74 76 77 78 85 86 88 4185 90 89 604 261720 95 102 103 111 114 123 126 130 134 142 143 659 148 147 2197 1175 149 155 156 158 159 160 171 173 174 687 179 181 183 15034 188 194 200 215 218 221 3818 235 749 243 757 18167 270 289 2342 2348 816 20785 316 318 319 320 2881 43333 1372 8039 1388 367 385 31618 388 906 2450 408 416 936 4796851 1472 1481 972 465 467 5605 4072 3563 2037"

for k in $content
do
	while /bin/true; do
		echo $RANDOM | ndnpoke -x 10000 -w 7200000 ndn:/content$k
    		#sleep 0.1
	done &
	sleep 0.1
done

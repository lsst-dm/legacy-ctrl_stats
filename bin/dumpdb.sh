#!/bin/sh
host=$1
port=$2
scratch=$3
nodes=S2012Pipe.diamond.dag.nodes.log
for i in `/bin/ls $scratch`
do
    file=$scratch/$i/$nodes
    if [ -f $file ]
    then
            python dbDump2.py $1 $2 $i $file
            ret=$?
            if [ $ret != 0 ]
            then
                exit
            fi
    fi
done

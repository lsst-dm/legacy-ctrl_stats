#!/bin/sh
host=$1
port=$2
dbname=$3
scratch=$4
nodes=S2012Pipe.diamond.dag.nodes.log
for i in `/bin/ls $scratch`
do
    file=$scratch/$i/$nodes
    if [ -f $file ]
    then
            python dbDump.py $1 $2 $3 $file
            ret=$?
            if [ $ret != 0 ]
            then
                exit
            fi
    fi
done

#!/bin/sh
scratch=$1
nodes=S2012Pipe.diamond.dag.nodes.log
for i in `/bin/ls $scratch`
do
    file=$scratch/$i/$nodes
    if [ -f $file ]
    then
            python dbDump.py $file
            ret=$?
            if [ $ret != 0 ]
            then
                exit
            fi
    fi
done

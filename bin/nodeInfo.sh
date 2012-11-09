#!/bin/sh
scratch=$1
nodes=S2012Pipe.diamond.dag.nodes.log
for i in `/bin/ls $scratch`
do
    file=$scratch/$i/$nodes
    if [ -f $file ]
    then
            echo "====="
            echo $file
            echo "====="
            python nodeInfo.py $file $2
            ret=$? 
            if [ $ret != 0 ]
            then
                exit
            fi
    fi
done

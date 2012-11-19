#!/bin/sh
host=$1
port=$2
scratch=$3
nodes=S2012Pipe.diamond.dag.nodes.log
prejob=worker-pre.log
postjob=worker-post.log
for i in `/bin/ls $scratch`
do
    nodesfile=$scratch/$i/$nodes
    prefile=$scratch/$i/logs/$prejob
    postfile=$scratch/$i/$postjob
    if [ -f $file ]
    then
            python condorLogIngest.py -q -H $1 -p $2 -d $i -f $prefile $nodesfile $postfile
    fi
done

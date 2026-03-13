#!/bin/bash

###### USERS INPUT ############################################################

#### END OF USER INPUT #######################################################

if [ -d "processor0" ]
then
    export NP="$(find processor* -maxdepth 0 -type d -print| wc -l)"

    #for i in processor*;do rm -rf $i/0/*; for j in $i/[1-9]*; do rm -rf $j/uniform; mv $j/* $i/0/.; done; done
    #rm -rf processor*/[1-9]*
    # Run simpleFoam in parallel
    echo -e "Run processPoroPerm in parallel on $NP processors"
    srun processPoroPerm -parallel  > processPoroPermFlow.out
else
    #for j in [1-9]*; do rm -rf $j/uniform; mv $j/* 0/.; done
    #rm -rf [1-9]*
    echo -e "Run processPoroPerm"
    processPoroPerm > processPoroPermFlow.out
fi 





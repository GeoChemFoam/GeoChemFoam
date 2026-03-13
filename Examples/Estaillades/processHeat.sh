#!/bin/bash

###### USERS INPUT ############################################################


#### END OF USER INPUT #######################################################


if [ -d "processor0" ]
then
    export NP="$(find processor* -maxdepth 0 -type d -print| wc -l)"

    echo -e "processHeatTransfer in parallel on $NP processors"
    mpiexec -np $NP processHeatTransfer -parallel > processHeatTransferH.out
else
    echo -e "processHeatTransfer"
    processHeatTransfer > processHeatTransferH.out
fi




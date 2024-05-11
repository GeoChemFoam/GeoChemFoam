#!/bin/bash

###### USERS INPUT ############################################################

#### END OF USER INPUT

# Run processDispersion in parallel
if [ -d "processor0" ]
then
    export NP="$(find processor* -maxdepth 0 -type d -print| wc -l)"

    #rm -rf processor*
    echo -e "processDisp in parallel"
    mpirun -np $NP processDispersion -parallel  > processDispD.out
else
    echo -e "processDisp"
    processDispersion > processDispD.out
fi

#!/bin/bash

###### USERS INPUT ############################################################

## Define the total number of iterations of the simulation
TotalTime=0.4
WriteTimestep=0.04
runTimestep=2e-4

#### END OF USER INPUT #######################################################

cp system/controlDict1 system/controlDict
sed -i "s/TotalTime/$TotalTime/g" system/controlDict
sed -i "s/WriteTimestep/$WriteTimestep/g" system/controlDict
sed -i "s/runTimestep/$runTimestep/g" system/controlDict


cp system/fvSolution1 system/fvSolution

if [ -d "processor0" ]
then
    export NP="$(find processor* -maxdepth 0 -type d -print| wc -l)"

    echo -e "Run heatTransportFoam in parallel on $NP processors"
    mpirun -np $NP heatTransportFoam -parallel  > heatTransportFoamH.out 
else
    echo -e "Run heatTransportSimpleFoam"
    heatTransportFoam > heatTransportFoamH.out 
fi




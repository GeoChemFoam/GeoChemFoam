#!/bin/bash

###### USERS INPUT ############################################################

## Define the total number of iterations of the simulation
TotalTime=20000

#### END OF USER INPUT #######################################################

cp constant/fvOptionsRun1 constant/fvOptions
sed -i "s/TotalTime/$TotalTime/g" constant/fvOptions

cp system/controlDict1 system/controlDict
sed -i "s/TotalTime/$TotalTime/g" system/controlDict
sed -i "s/WriteTimestep/$TotalTime/g" system/controlDict
sed -i "s/runTimestep/1/g" system/controlDict

cp system/fvSolution1 system/fvSolution

if [ -d "processor0" ]
then
    export NP="$(find processor* -maxdepth 0 -type d -print| wc -l)"

    # Run simpleFoam in parallel
    echo -e "Run simpleDBSFoam in parallel on $NP processors"
    mpiexec -np $NP simpleDBSFoam -parallel  > simpleDBSFoamFlow.out
else
    echo -e "Run simpleDBSFoam"
    simpleDBSFoam > simpleDBSFoamFlow.out
fi 

echo -e "Note: Please check the last line of simpleDBSFoamFlow.out to confirm the flow field has converged. If it has not, change TotalTime and/or the p tolerance  in system/fvSolution and re-run the script" 

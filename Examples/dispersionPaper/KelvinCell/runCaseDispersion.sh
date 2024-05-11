#!/bin/bash

###### USERS INPUT ############################################################
## Define the total number of iterations of the simulation
TotalTime=10000
WriteTime=10000
RunTimeStep=1

#### END OF USER INPUT

cp system/fvSolution2 system/fvSolution
cp system/controlDict2 system/controlDict
sed -i "s/TotalTime/$TotalTime/g" system/controlDict
sed -i "s/WriteTime/$WriteTime/g" system/controlDict
sed -i "s/RunTimeStep/$RunTimeStep/g" system/controlDict

# Run dispersionFoam in parallel
if [ -d "processor0" ]
then
    export NP="$(find processor* -maxdepth 0 -type d -print| wc -l)"

    # Run dispersionFoam in parallel
    echo -e "Run dispersionFoam in parallel"
    mpirun -np $NP dispersionFoam -parallel  > dispersionFoamD.out
else
    echo -e "Run dispersionFoam"
    dispersionFoam -parallel
fi

#!/bin/bash

###### USERS INPUT ############################################################
## Define the total number of iterations of the simulation
TotalTime=66.1362
WriteTime=2000
RunTimeStep=0.00661362

#### END OF USER INPUT

cp system/fvSolution2 system/fvSolution
cp system/controlDict2 system/controlDict
sed -i "s/TotalTime/$TotalTime/g" system/controlDict
sed -i "s/WriteTime/$WriteTime/g" system/controlDict
sed -i "s/RunTimeStep/$RunTimeStep/g" system/controlDict

# Run scalarTransportDBSFoam in parallel
if [ -d "processor0" ]
then
    export NP="$(find processor* -maxdepth 0 -type d -print| wc -l)"

    # Run dispersionFoam in parallel
    echo -e "Run scalarTransportDBSFoam in parallel"
    mpirun -np $NP scalarTransportDBSFoam -parallel  > dispersionFoamD.out
else
    echo -e "Run scalarTransportDBSFoam"
   scalarTransportDBSFoam -parallel
fi

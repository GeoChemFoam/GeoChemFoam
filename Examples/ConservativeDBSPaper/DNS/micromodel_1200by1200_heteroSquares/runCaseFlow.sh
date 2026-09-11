#/bin/bash

###### USERS INPUT ############################################################

## Define the total number of iterations of the simulation
TotalTime=20000
WriteTimestep=1000

#### END OF USER INPUT #######################################################

cp system/controlDict1 system/controlDict
sed -i "s/TotalTime/$TotalTime/g" system/controlDict
sed -i "s/WriteTimestep/$WriteTimestep/g" system/controlDict
sed -i "s/runTimestep/1/g" system/controlDict

cp system/fvSolution1 system/fvSolution

if [ -d "processor0" ]
then
    export NP="$(find processor* -maxdepth 0 -type d -print| wc -l)"
    #Run simpleFoam in parallel
    echo -e "Run simpleGCFoam in parallel on $NP processors"
    mpirun -np $NP simpleGCFoam -parallel  > simpleGCFoam.out

    reconstructPar -withZero > reconstructPar.out

    rm -rf processor*

else
    echo -e "Run simpleGCFoam"
    simpleGCFoam > simpleGCFoam.out
fi 

echo -e "Note: Please check the last line of simpleGCFoam.out to confirm the flow field has converged. If it has not, change TotalTime and/or the p tolerance  in system/fvSolution and re-run the script" 

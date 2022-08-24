#!/bin/bash

# Load user environment variables
source $HOME/.bashrc

#export $GCFOAM_DIR/lib

cd ../temp

echo "map fields to new mesh"
mapFields ../micromodel -case ../temp -sourceTime latestTime 
mv 0/pointMotionU* 0/pointMotionU

cp system/controlDict0 system/controlDict
cp system/fvSolution0 system/fvSolution

echo "decompose parallel"
decomposePar 

export NP="$(find processor* -maxdepth 0 -type d -print| wc -l)"

echo "run reactiveTransportALEFoam for 1e-6 second"
mpiexec -np $NP reactiveTransportALEFoam -parallel 

echo "reconstructPar"
reconstructPar 
rm -rf processor*

cp 1e-06/C 0/.
cp 1e-06/U 0/.
cp 1e-06/p 0/.
cp 1e-06/phi 0/.
cp 1e-06/pointMotionU 0/.
cp 1e-06/cellMotionU 0/.

rm -rf 1e-06

echo -e "Fields have been initialised."

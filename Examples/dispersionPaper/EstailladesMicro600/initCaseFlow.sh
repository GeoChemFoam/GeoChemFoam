#!/bin/bash

###### USERS INPUT ############################################################

## Define your pressure drop at the inlet (Pa/m)
PGRAD=5.5958e4

#fluid properties
Visc=1e-6

#### END OF USER INPUT #######################################################

echo -e "set flow and transport properties"
cp constant/transportProperties1 constant/transportProperties
sed -i "s/Visc/$Visc/g" constant/transportProperties

mkdir -p 0

cp 0_orig/U 0/.
cp 0_orig/p 0/.

cp constant/fvOptionsRun constant/fvOptionsRun1
sed -i "s/PGRAD/$PGRAD/g" constant/fvOptionsRun1

if [ -d "processor0" ]
then
    # Decompose
    echo -e "DecomposePar"
    decomposePar -fields > decomposeParFlow.out

    rm -rf 0
fi 

echo "Case initialised"

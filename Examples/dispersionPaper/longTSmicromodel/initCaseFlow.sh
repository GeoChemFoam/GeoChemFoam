#!/bin/bash

###### USERS INPUT ############################################################

#Define flow rate
PGRAD=87.1155

#fluid properties
Visc=1e-6

#Kozeny-Carman constant
#permeability of foam is 1/kf*eps^3/(1-eps)^2=4e-12
kf=6.000e10

#### END OF USER INPUT #######################################################

echo -e "set flow and transport properties"
cp constant/transportProperties1 constant/transportProperties
sed -i "s/Visc/$Visc/g" constant/transportProperties
sed -i "s/k_f/$kf/g" constant/transportProperties

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

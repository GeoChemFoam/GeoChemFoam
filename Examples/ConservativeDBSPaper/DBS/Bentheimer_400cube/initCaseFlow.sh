#!/bin/bash

###### USERS INPUT ############################################################

#fluid properties
Visc=1e-6

#Kozeny-Carman constant
kf=8e12

#Pressure Gradient
momentum_Source=0

#### END OF USER INPUT #######################################################

echo -e "set flow and transport properties"
cp constant/transportProperties1 constant/transportProperties
sed -i "s/Visc/$Visc/g" constant/transportProperties
sed -i "s/k_f/$kf/g" constant/transportProperties
#sed -i "s/momentum_Source/$momentum_Source/g" constant/transportProperties

mkdir -p 0
cp 0_orig/U 0/.
cp 0_orig/p 0/.

#echo -e "set field"
#setFields > setFields.out


if [ -d "processor0" ]
then
    # Decompose
    echo -e "DecomposePar"
    decomposePar -fields > decomposeParFlow.out

    rm -rf 0
fi 

echo -e "Case initialised"





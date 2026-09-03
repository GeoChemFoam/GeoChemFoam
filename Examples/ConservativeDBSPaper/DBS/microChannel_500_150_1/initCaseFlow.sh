#!/bin/bash

###### USERS INPUT ############################################################

#Define pressure drop
PDROP=0.01

#fluid properties
Visc=1e-6

#Kozeny-Carman constant
kf=7e12

#### END OF USER INPUT #######################################################

echo -e "set flow and transport properties"
cp constant/transportProperties1 constant/transportProperties
sed -i "s/Visc/$Visc/g" constant/transportProperties
sed -i "s/k_f/$kf/g" constant/transportProperties

cp system/fvSolution1 system/fvSolution

cp 0_org/eps.org ./0/eps
cp 0_org/U 0/.
cp 0_org/p 0/.
sed -i "s/PDROP/$PDROP/g" 0/p

echo -e "Case initialised"





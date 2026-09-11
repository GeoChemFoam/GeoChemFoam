#!/bin/bash

###### USERS INPUT ############################################################

#Define pressure drop
PDROP=0.0001

#fluid properties
Visc=1e-6

#Kozeny-Carman constant
kf=1.8e8

#### END OF USER INPUT #######################################################

echo -e "set flow and transport properties"
cp constant/transportProperties1 constant/transportProperties
sed -i "s/Visc/$Visc/g" constant/transportProperties
sed -i "s/k_f/$kf/g" constant/transportProperties

cp system/fvSolution1 system/fvSolution

mkdir 0
cp 0_orig/eps.orig ./0/eps
cp 0_orig/U 0/.
cp 0_orig/p 0/.
sed -i "s/PDROP/$PDROP/g" 0/p

echo -e "Case initialised"





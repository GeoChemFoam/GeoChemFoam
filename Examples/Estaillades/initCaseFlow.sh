#!/bin/bash

###### USERS INPUT ############################################################

#Define flow rate
PDROP=0.001

#fluid properties
Visc=1e-6

#Kozeny-Carman constant
kf=5e12

#### END OF USER INPUT #######################################################

echo -e "set flow and transport properties"
cp constant/transportProperties1 constant/transportProperties
sed -i "s/Visc/$Visc/g" constant/transportProperties
sed -i "s/k_f/$kf/g" constant/transportProperties

NPX="$(cat system/NPX)"
NPY="$(cat system/NPY)"
NPZ="$(cat system/NPZ)"



echo -e "create eps"
python system/createU.py --NPX $NPX --NPY $NPY --NPZ $NPZ 
python system/createP.py --NPX $NPX --NPY $NPY --NPZ $NPZ --PDROP $PDROP

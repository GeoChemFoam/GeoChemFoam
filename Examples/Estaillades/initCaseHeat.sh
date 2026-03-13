#!/bin/bash

###### USERS INPUT ############################################################

#fluid properties
kappa_f=0.04 
kappa_s=3.3

rho_f=300
rho_s=2600

gamma_f=3000
gamma_s=700

#### END OF USER INPUT #######################################################

echo -e "set flow and transport properties"
cp constant/transportProperties2 constant/transportProperties
sed -i "s/kappa_s/$kappa_s/g" constant/transportProperties
sed -i "s/kappa_f/$kappa_f/g" constant/transportProperties
sed -i "s/rho_f/$rho_f/g" constant/transportProperties
sed -i "s/rho_s/$rho_s/g" constant/transportProperties
sed -i "s/gamma_f/$gamma_f/g" constant/transportProperties
sed -i "s/gamma_s/$gamma_s/g" constant/transportProperties

NPX="$(cat system/NPX)"
NPY="$(cat system/NPY)"
NPZ="$(cat system/NPZ)"

echo -e "create T"
python system/createT.py --NPX $NPX --NPY $NPY --NPZ $NPZ




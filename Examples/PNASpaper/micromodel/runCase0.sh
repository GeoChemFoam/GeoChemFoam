#!/bin/bash

###### USERS INPUT ############################################################

#Define flow rate
flowRate=6.7124e-12

#fluid properties
Visc=1e-6
Diff=1e-9

#Reaction constants
kreac=8.1632e-6
scoeff=1
rhos=2700
Mws=100
cinlet=0.01

# Number of processors
NP=24


#### END OF USER INPUT #######################################################

MPIRUN=mpirun

set -e

cp constant/transportProperties0 constant/transportProperties
sed -i "s/Visc/$Visc/g" constant/transportProperties

cp constant/thermoPhysicalProperties0 constant/thermoPhysicalProperties
sed -i "s/Diff/$Diff/g" constant/thermoPhysicalProperties


rm -rf 0_org
cp -r 0_gold 0_org
sed -i "s/flow_rate/$flowRate/g" 0_org/U
sed -i "s/k_reac/$kreac/g" 0_org/C
sed -i "s/s_coeff/$scoeff/g" 0_org/C
sed -i "s/c_inlet/$cinlet/g" 0_org/C
sed -i "s/k_reac/$kreac/g" 0_org/pointMotionU
sed -i "s/Mw_s/$Mws/g" 0_org/pointMotionU
sed -i "s/rho_s/$rhos/g" 0_org/pointMotionU

cp -r 0_org 0


cp system/controlDict0 system/controlDict
cp system/fvSolution0 system/fvSolution

echo "decompose parallel"
cp system/decomposeParDict1 system/decomposeParDict
sed -i "s/NP/$NP/g" system/decomposeParDict

decomposePar > decomposePar0.out

echo "run reactiveTransportALEFoam for 1e-6 second"
mpiexec -np $NP reactiveTransportALEFoam -parallel > reactiveTransportALEFoam0.out

echo "reconstructPar"
reconstructPar > reconstructPar0.out
rm -rf processor*

cp 1e-06/C 0/.
cp 1e-06/U 0/.
cp 1e-06/p 0/.
cp 1e-06/phi 0/.
cp 1e-06/pointMotionU 0/.
cp 1e-06/cellMotionU 0/.

rm -rf 1e-06 

echo -e "Fields have been initialised."

#!/bin/bash

###### USERS INPUT ############################################################

## diffusion
Diff=1e-8

##porosity of micropores
eps0=0.445167

##tortuosity iof micropores
tau=2.636

##micro pore size
Lpore=3.69828e-07

## Dipsersivity constant
## Pe<1
## Dx=Diff*tinv*(1+beta1*Pe^alpha1)
## Dy=Diff*tinv*(1+beta2*Pe^gamma1)
## Pe>1
## Dx=Diff*tinv*(1+beta1*Pe^alpha2)
## Dy=Diff*tinv*(1+beta2*Pe^gamma2)
beta1=70
alpha1=1.35
alpha2=1.35
beta2=4.6
gamma1=1.0
gamma2=0.68
#### END OF USER INPUT

rm -f constant/fvOptions

cp constant/transportProperties2 constant/transportProperties
sed -i "s/Diff/$Diff/g" constant/transportProperties

mkdir -p 0
cp 0_orig/B 0/.

if [ -d "processor0" ]
then
    echo -e "reconstructPar"
    reconstructPar -withZero > reconstructParD.out
    echo "Calculate micro dispersivity"
    python system/createDeff.py --Diff $Diff --eps0 $eps0 --tau $tau --Lpore $Lpore --beta1 $beta1 --alpha1 $alpha1 --alpha2 $alpha2 --beta2 $beta2 --gamma1 $gamma1 --gamma2 $gamma2 

    # Decompose
    echo -e "DecomposePar"
    decomposePar -fields > decomposeParD.out

    rm -rf 0
else
    echo "Calculate micro dispersivity"
    python system/createDeff.py --Diff $Diff --eps0 $eps0 --tau $tau --Lpore $Lpore --beta1 $beta1 --alpha1 $alpha1 --alpha2 $alpha2 --beta2 $beta2 --gamma1 $gamma1 --gamma2 $gamma2
fi

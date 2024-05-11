#!/bin/bash

###### USERS INPUT ############################################################

## diffusion
Diff=1e-7

##porosity of micropores
eps0=0.4295

##matrix pore size
Lpore=1.0625e-5

## Dipsersivity constant
## Pe<1
## 0.1<Pe<1
## Dx=Diff*tinv*(1+beta1*Pe^alpha1)
## Dy=Diff*tinv*(1+beta2*Pe^gamma1)
## 1<Pe<10
## Dx=Diff*tinv*(1+beta1*Pe^alpha2)
## Dy=Diff*tinv*(1+beta2*Pe^gamma2)
## Pe>100
## Dx=Diff*tinv*(1+eta1*Pe^alpha3)
## Dy=Diff*tinv*(1+eta2*Pe^gamma3)

beta1=0.228
alpha1=1.187
alpha2=1.187
beta2=1.6290
gamma1=1.663
gamma2=0.546
eta1=0.880
alpha3=1.599
eta2=2.667
gamma3=0.332

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
    python system/createDeff.py --Diff $Diff --eps0 $eps0 --tau $tau --Lpore $Lpore --beta1 $beta1 --alpha1 $alpha1 --alpha2 $alpha2 --beta2 $beta2 --gamma1 $gamma1 --gamma2 $gamma2 --eta1 $eta1 --alpha3 $alpha3 --eta2 $eta2 --gamma3 $gamma3 

    # Decompose
    echo -e "DecomposePar"
    decomposePar -fields > decomposeParD.out

    rm -rf 0
else
    echo "Calculate micro dispersivity"
    python system/createDeff.py --Diff $Diff --eps0 $eps0 --tau $tau --Lpore $Lpore --beta1 $beta1 --alpha1 $alpha1 --alpha2 $alpha2 --beta2 $beta2 --gamma1 $gamma1 --gamma2 $gamma2 --eta1 $eta1 --alpha3 $alpha3 --eta2 $eta2 --gamma3 $gamma3 
fi

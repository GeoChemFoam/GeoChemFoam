#!/bin/bash

###### USERS INPUT ############################################################

## diffusion
Diff=1e-6


##porosity of micropores
micro_por=('1' '0.338' '0.338' '0.338' '0.338' '0.338' '0.338' '0.338' '0.338' '0.338' '0.338' '0.338' '0.338' '0.0001')

##tortuosity iof micropores
micro_tau=('1' '2.22' '2.22' '2.22' '2.22' '2.22' '2.22' '2.22' '2.22' '2.22' '2.22' '2.22' '2.22' '1')

##micro pore size
micro_Lpore=('0' '1.88e-7' '1.88e-7' '1.88e-7' '1.88e-7' '1.88e-7' '1.88e-7' '1.88e-7' '1.88e-7' '1.88e-7' '1.88e-7' '1.88e-7' '1.88e-7' '0')

## Dipsersivity constant
## Pe<1
## Dx=Diff*tinv*(1+betax*Pe^alpha1x)
## Dy=Diff*tinv*(1+betay*Pe^alpha1y)
## Dz=Diff*tinv*(1+betaz*Pe^alpha2z)
## Pe>1
## Dx=Diff*tinv*(1+betax*Pe^alpha2x)
## Dy=Diff*tinv*(1+betay*Pe^alpha2y)
## Dy=Diff*tinv*(1+betaz*Pe^alpha2z)

micro_betax=('0' '2.56' '2.56' '2.56' '2.56' '2.56' '2.56' '2.56' '2.56' '2.56' '2.56' '2.56' '2.56' '1')
micro_alpha1x=('1' '0.94' '0.94' '0.94' '0.94' '0.94' '0.94' '0.94' '0.94' '0.94' '0.94' '0.94' '0.94' '1')
micro_alpha2x=('1' '0.56' '0.56' '0.56' '0.56' '0.56' '0.56' '0.56' '0.56' '0.56' '0.56' '0.56' '0.56' '1')
micro_betay=('0' '100' '100' '100' '100' '100' '100' '100' '100' '100' '100' '100' '100' '0')
micro_alpha1y=('1' '1.54' '1.54' '1.54' '1.54' '1.54' '1.54' '1.54' '1.54' '1.54' '1.54' '1.54' '1.54' '1')
micro_alpha2y=('1' '1.54' '1.54' '1.54' '1.54' '1.54' '1.54' '1.54' '1.54' '1.54' '1.54' '1.54' '1.54' '1')
micro_betaz=('0' '2.56' '2.56' '2.56' '2.56' '2.56' '2.56' '2.56' '2.56' '2.56' '2.56' '2.56' '2.56' '1')
micro_alpha1z=('1' '0.94' '0.94' '0.94' '0.94' '0.94' '0.94' '0.94' '0.94' '0.94' '0.94' '0.94' '0.94' '1')
micro_alpha2z=('1' '0.56' '0.56' '0.56' '0.56' '0.56' '0.56' '0.56' '0.56' '0.56' '0.56' '0.56' '0.56' '1')
#### END OF USER INPUT

rm -f constant/fvOptions

cp constant/transportProperties2 constant/transportProperties
sed -i "s/Diff/$Diff/g" constant/transportProperties

mkdir -p 0
cp 0_orig/B 0/.

if [ -d "processor0" ]
then
    reconstructPar -withZero -fields '(eps U)' > reconstructParD.out
    python system/createDeff.py --Diff $Diff --micro_por ${micro_por[@]} --micro_tau ${micro_tau[@]} --micro_Lpore ${micro_Lpore[@]} --micro_betax ${micro_betax[@]} --micro_alpha1x ${micro_alpha1x[@]} --micro_alpha2x ${micro_alpha2x[@]}  --micro_betay ${micro_betay[@]} --micro_alpha1y ${micro_alpha1y[@]} --micro_alpha2y ${micro_alpha2y[@]} --micro_betaz ${micro_betaz[@]}  --micro_alpha1z ${micro_alpha1z[@]} --micro_alpha2z ${micro_alpha2z[@]} 
    # Decompose
    echo -e "DecomposePar"
    decomposePar -fields > decomposeParD.out
fi

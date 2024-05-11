#!/bin/bash

###### USERS INPUT ############################################################

## Define the total number of iterations of the simulation
TotalTime=10000
WriteTime=500
RunTimeStep=1

##microporous phases
micro_por=('1' '0.338' '0.338' '0.338' '0.338' '0.338' '0.338' '0.338' '0.338' '0.338' '0.338' '0.338' '0.338' '0.0001')
micro_tort=('1' '2.22' '2.22' '2.22' '2.22' '2.22' '2.22' '2.22' '2.22' '2.22' '2.22' '2.22' '2.22' '1')
micro_alpha1y=('1' '1.54' '1.54' '1.54' '1.54' '1.54' '1.54' '1.54' '1.54' '1.54' '1.54' '1.54' '1.54' '1')
micro_alpha2y=('1' '1.54' '1.54' '1.54' '1.54' '1.54' '1.54' '1.54' '1.54' '1.54' '1.54' '1.54' '1.54' '1')
micro_alpha1x=('1' '0.94' '0.94' '0.94' '0.94' '0.94' '0.94' '0.94' '0.94' '0.94' '0.94' '0.94' '0.94' '1')
micro_alpha2x=('1' '0.56' '0.56' '0.56' '0.56' '0.56' '0.56' '0.56' '0.56' '0.56' '0.56' '0.56' '0.56' '1')
micro_alpha1z=('1' '0.94' '0.94' '0.94' '0.94' '0.94' '0.94' '0.94' '0.94' '0.94' '0.94' '0.94' '0.94' '1')
micro_alpha2z=('1' '0.56' '0.56' '0.56' '0.56' '0.56' '0.56' '0.56' '0.56' '0.56' '0.56' '0.56' '0.56' '1')
micro_betay=('0' '100' '100' '100' '100' '100' '100' '100' '100' '100' '100' '100' '100' '0')
micro_betax=('0' '2.56' '2.56' '2.56' '2.56' '2.56' '2.56' '2.56' '2.56' '2.56' '2.56' '2.56' '2.56' '1')
micro_betaz=('0' '2.56' '2.56' '2.56' '2.56' '2.56' '2.56' '2.56' '2.56' '2.56' '2.56' '2.56' '2.56' '1')
micro_Lpore=('0' '1.88e-7' '1.88e-7' '1.88e-7' '1.88e-7' '1.88e-7' '1.88e-7' '1.88e-7' '1.88e-7' '1.88e-7' '1.88e-7' '1.88e-7' '1.88e-7' '0')


#### END OF USER INPUT

rm -f constant/fvOptions
cp system/fvSolution2 system/fvSolution
cp system/controlDict2 system/controlDict
sed -i "s/TotalTime/$TotalTime/g" system/controlDict
sed -i "s/WriteTime/$WriteTime/g" system/controlDict
sed -i "s/RunTimeStep/$RunTimeStep/g" system/controlDict

#reconstructPar -withZero -fields '(eps U)' > reconstructParDAll.out

#cp -r 0 0_save
#cp -r 0_save 0

Diff=1e-6

cp constant/transportProperties2 constant/transportProperties
sed -i "s/Diff/$Diff/g" constant/transportProperties

python system/createDeff.py --micro_por ${micro_por[@]} --micro_tort ${micro_tort[@]} --micro_alpha1x ${micro_alpha1x[@]} --micro_alpha2x ${micro_alpha2x[@]} --micro_alpha1y ${micro_alpha1y[@]} --micro_alpha2y ${micro_alpha2y[@]} --micro_alpha1z ${micro_alpha1z[@]} --micro_alpha2z ${micro_alpha2z[@]} --micro_betax ${micro_betax[@]} --micro_betay ${micro_betay[@]} --micro_betaz ${micro_betaz[@]} --micro_Lpore ${micro_Lpore[@]} --Diff $Diff  

mv 0/D 0/D0

#Diff=1e-7

#cp constant/transportProperties2 constant/transportProperties
#sed -i "s/Diff/$Diff/g" constant/transportProperties

#python system/createDeff.py --micro_por ${micro_por[@]} --micro_tort ${micro_tort[@]} --micro_alpha1x ${micro_alpha1x[@]} --micro_alpha2x ${micro_alpha2x[@]} --micro_alpha1y ${micro_alpha1y[@]} --micro_alpha2y ${micro_alpha2y[@]} --micro_alpha1z ${micro_alpha1z[@]} --micro_alpha2z ${micro_alpha2z[@]} --micro_betax ${micro_betax[@]} --micro_betay ${micro_betay[@]} --micro_betaz ${micro_betaz[@]} --micro_Lpore ${micro_Lpore[@]} --Diff $Diff

#mv 0/D 0/D01

#Diff=1e-8

#cp constant/transportProperties2 constant/transportProperties
#sed -i "s/Diff/$Diff/g" constant/transportProperties

#python system/createDeff.py --micro_por ${micro_por[@]} --micro_tort ${micro_tort[@]} --micro_alpha1x ${micro_alpha1x[@]} --micro_alpha2x ${micro_alpha2x[@]} --micro_alpha1y ${micro_alpha1y[@]} --micro_alpha2y ${micro_alpha2y[@]} --micro_alpha1z ${micro_alpha1z[@]} --micro_alpha2z ${micro_alpha2z[@]} --micro_betax ${micro_betax[@]} --micro_betay ${micro_betay[@]} --micro_betaz ${micro_betaz[@]} --micro_Lpore ${micro_Lpore[@]} --Diff $Diff

#mv 0/D 0/D1

#Diff=1e-9

#cp constant/transportProperties2 constant/transportProperties
#sed -i "s/Diff/$Diff/g" constant/transportProperties

#python system/createDeff.py --micro_por ${micro_por[@]} --micro_tort ${micro_tort[@]} --micro_alpha1x ${micro_alpha1x[@]} --micro_alpha2x ${micro_alpha2x[@]} --micro_alpha1y ${micro_alpha1y[@]} --micro_alpha2y ${micro_alpha2y[@]} --micro_alpha1z ${micro_alpha1z[@]} --micro_alpha2z ${micro_alpha2z[@]} --micro_betax ${micro_betax[@]} --micro_betay ${micro_betay[@]} --micro_betaz ${micro_betaz[@]} --micro_Lpore ${micro_Lpore[@]} --Diff $Diff

#mv 0/D 0/D10

#Diff=1e-10

#cp constant/transportProperties2 constant/transportProperties
#sed -i "s/Diff/$Diff/g" constant/transportProperties

#python system/createDeff.py --micro_por ${micro_por[@]} --micro_tort ${micro_tort[@]} --micro_alpha1x ${micro_alpha1x[@]} --micro_alpha2x ${micro_alpha2x[@]} --micro_alpha1y ${micro_alpha1y[@]} --micro_alpha2y ${micro_alpha2y[@]} --micro_alpha1z ${micro_alpha1z[@]} --micro_alpha2z ${micro_alpha2z[@]} --micro_betax ${micro_betax[@]} --micro_betay ${micro_betay[@]} --micro_betaz ${micro_betaz[@]} --micro_Lpore ${micro_Lpore[@]} --Diff $Diff

#mv 0/D 0/D100

#cp 0_orig/B 0/.

rm 0/eps
rm 0/U

decomposePar -fields > decomposeParDAll.out


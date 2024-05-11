#!/bin/bash

###### USERS INPUT ############################################################

## diffusion
Diff=1e-8

#### END OF USER INPUT

rm -f constant/fvOptions

cp constant/transportProperties2 constant/transportProperties
sed -i "s/Diff/$Diff/g" constant/transportProperties

mkdir -p 0
cp 0_orig/B 0/.

if [ -d "processor0" ]
then
    # Decompose
    echo -e "DecomposePar"
    decomposePar -fields > decomposeParD.out

    rm -rf 0
fi

#!/bin/bash

###### USERS INPUT ############################################################

#Smoothing parameters: smooth surface when image has artifical roughness created ny segmentation to avoid error when using adaptive mesh
nSmooth=1
cSmooth=0.5

#### END OF USER INPUT #######################################################

cp system/fvSolution1 system/fvSolution
sed -i "s/nSmooth/$nSmooth/g" system/fvSolution
sed -i "s/cSmooth/$cSmooth/g" system/fvSolution

if [ -d "processor0" ]
then
    export NP="$(find processor* -maxdepth 0 -type d -print| wc -l)"

    echo -e "smoothSolidSurface in parallel on $NP processors"
    srun smoothSolidSurface -parallel  > smoothSolidSurface.out
    rm -rf processor*/0/Kinv
    rm -rf processor*/0/nuFact
else
    echo -e "smoothSolidSurface"
    smoothSolidSurface > smoothSolidSurface.out
    rm -rf 0/Kinv
    rm -rf 0/nuFact
fi





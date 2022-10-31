#!/bin/bash

# Load user environment variables
source $HOME/.bashrc

#export $GCFOAM_DIR/lib

MPIRUN=mpirun

cd ../temp

echo -e "remove bad internal faces"
./removeInternalFaces.sh

echo -e "create stl of solidwalls"
surfaceMeshTriangulate -patches '(solidwalls)' constant/triSurface/Image_meshed.stl 
cp constant/triSurface/Image_meshed.stl ../micromodel/constant/triSurface/Image_meshed.stl

source $OF4X_DIR/OpenFOAM-4.x/etc/bashrc 

rm -rf 0 0.* [1-9]*

rm -rf constant/polyMesh
rm -rf processor*
rm -f *.csv
rm -f constant/triSurface/pore_ind*

cp system/controlDictInit system/controlDict


# Create background mesh
echo -e "Create background mesh"
blockMesh 

# Decompose background mesh
echo -e "Decompose background mesh"
decomposePar 

export NP="$(find processor* -maxdepth 0 -type d -print| wc -l)"

# Remove fields on this stage
rm -rf ./processor*/0/*

# Run snappyHexMesh in parallel
echo -e "Run snappyHexMesh in parallel"
$MPIRUN -np $NP snappyHexMesh -overwrite -parallel  

# reconstruct mesh to fields decomposition
echo -e "reconstruct parallel mesh"
reconstructParMesh -constant 


rm -rf *.out processor*

cp -r 0_org 0

cp -r constant/polyMesh 0/.


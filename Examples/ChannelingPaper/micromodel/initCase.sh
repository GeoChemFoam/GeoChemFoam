#!/bin/bash

###### USERS INPUT ############################################################

#Define image name
Image_name="HM12_6_12"

# Define image dimensions
x_dim=12000
y_dim=12000
z_dim=1

# define resolution (m)
res=0.0000025

# depth of 2D model
depth=0.00006

# define value of the pores and solid in the image 
pores_value=1
solid_value=0

# Pad width
padWidth=24

# step size for raw2stl generation
stepSize=2

# Define cropping parameters
x_min=0
x_max=12000
y_min=0
y_max=12000
z_min=0
z_max=24

# number of cells of initial mesh
# n*(nlevel+1) should be equal to image dimension when not binning 
n_x=1004
n_y=1004
#In 2D images, z has to be the empty direction
n_z=1

# flow direction 0 or 1, 2 is empty
direction=1

# Number of processors
NP=24

#### END OF USER INPUT #######################################################

source $OF4X_DIR/OpenFOAM-4.x/etc/bashrc 

MPIRUN=mpirun 

echo -e "make stl"
cd constant/triSurface
python raw2stl.py --x_min=$x_min --x_max=$x_max --y_min=$y_min --y_max=$y_max --z_min=$z_min --z_max=$z_max --pores_value=$pores_value --solid_value=$solid_value  --image_name=$Image_name --x_dim=$x_dim --y_dim=$y_dim --z_dim=$z_dim --padWidth=$padWidth --stepSize=$stepSize
cd ../..
# ./runSmooth.sh

#export pore_index_0="$(cat constant/triSurface/pore_indx)"
#export pore_index_1="$(cat constant/triSurface/pore_indy)"
#export pore_index_2="$(cat constant/triSurface/pore_indz)"
pore_index_0=$(expr -$padWidth*$res*0.5 | bc)
pore_index_1=$(expr -$padWidth*$res*0.5 | bc)
pore_index_2=0

surfaceTransformPoints -translate '(-2 -2 -1)' constant/triSurface/Image_meshed.stl constant/triSurface/Image_meshed.stl > surfaceTransformPoints1.out
surfaceTransformPoints -scale "($res $res $depth)" constant/triSurface/Image_meshed.stl constant/triSurface/Image_meshed.stl > surfaceTransformPoints2.out

# Create background mesh
echo -e "Create background mesh"
cp system/blockMeshDict2D$direction system/blockMeshDict

x_1=$(expr -$padWidth*$res | bc)
y_1=$(expr -$padWidth*$res | bc)
z_1=$(expr -$depth*0.5 | bc)

x_2=$(expr $x_max*$res-$x_min*$res+$padWidth*$res | bc)
y_2=$(expr $y_max*$res-$y_min*$res+$padWidth*$res | bc)
z_2=$(expr $depth*0.5 | bc)


sed -i "s/x_min/$x_1/g" system/blockMeshDict
sed -i "s/y_min/$y_1/g" system/blockMeshDict
sed -i "s/z_min/$z_1/g" system/blockMeshDict

sed -i "s/x_max/$x_2/g" system/blockMeshDict
sed -i "s/y_max/$y_2/g" system/blockMeshDict
sed -i "s/z_max/$z_2/g" system/blockMeshDict

sed -i "s/nx/$n_x/g" system/blockMeshDict
sed -i "s/ny/$n_y/g" system/blockMeshDict
sed -i "s/nz/$n_z/g" system/blockMeshDict

cp system/controlDictInit system/controlDict

blockMesh  > blockMesh.out

cp system/decomposeParDict1 system/decomposeParDict
sed -i "s/NP/$NP/g" system/decomposeParDict


# Decompose background mesh
echo -e "Decompose background mesh"
decomposePar > decomposeBlockMesh.out
rm -rf processor*/0/*

# Run snappyHexMesh in parallel
echo -e "Run snappyHexMesh in parallel"
cp system/snappyHexMeshDict1 system/snappyHexMeshDict

sed -i "s/poreIndex0/$pore_index_0/g" system/snappyHexMeshDict
sed -i "s/poreIndex1/$pore_index_1/g" system/snappyHexMeshDict
sed -i "s/poreIndex2/$pore_index_2/g" system/snappyHexMeshDict


cp system/postProcessDict1 system/postProcessDict
sed -i "s/x_1/$x_1/g" system/postProcessDict
sed -i "s/y_1/$y_1/g" system/postProcessDict
sed -i "s/z_1/$z_1/g" system/postProcessDict

sed -i "s/x_2/$x_2/g" system/postProcessDict
sed -i "s/y_2/$y_2/g" system/postProcessDict
sed -i "s/z_2/$z_2/g" system/postProcessDict

sed -i "s/flowdir/$direction/g" system/postProcessDict


$MPIRUN -np $NP snappyHexMesh -overwrite -parallel  > snappyHexMesh.out

echo -e "reconstruct parallel mesh"
reconstructParMesh -constant > reconstructParMesh.out

#echo -e "transformPoints" 
#vector="($res $res $res)"
#transformPoints -scale "$vector" > transformPoints.out

rm -rf processor*

echo -e "Image Initialised. It is advised to check in paraview to confirm mesh of porespace is reasonable before running flow" 

#!/bin/bash

###### USERS INPUT ############################################################

#Define image name
Image_name="micromodel_1200by1200_heteroSquares"

# Image directory relative to the case directory
dir="../../raw_images"

#Choose image format
format='raw'

#Choose if the image is compressed or not
compressed='yes'

# Define image dimensions
x_dim=1200
y_dim=1200
z_dim=1

#Values of solid, pore, and minimum porosity value for the solid phase (note: if the image contains solid voxels, this CANNOT be 0)
pores_value=0
solid_value=1
eps_min=0.0001

# tort=1/(eps)^index
tortIndex=1

# Define cropping parameters
x_min=0
x_max=1200
y_min=60
y_max=1140
z_min=0
z_max=1

#padding for inlet/outlet
padWidth=0

# define resolution (m)
res=0.000001


# number of cells of the initial mesh
n_x=1200
n_y=1080
n_z=1

#Mesh refinement level
nlevel=0
refineStokes=0

# flow direction 0 or 1, 2 is empty
direction=0

# Number of processors
NP=8

#### END OF USER INPUT #######################################################

if [ $format != 'raw' ]
then
        echo "ERROR: only raw format is implemented for this solver"
        exit
fi

#Insert dimensions in postProcessDict
x_1=0
y_1=0
z_1=0

xSize=$(echo "$x_max - $x_min" | bc)
ySize=$(echo "$y_max - $y_min" | bc)
zSize=$(echo "$z_max - $z_min" | bc)

x_2=$(expr $xSize*$res | bc)
y_2=$(expr $ySize*$res | bc)
z_2=$(expr $zSize*$res | bc)


cp system/postProcessDict1 system/postProcessDict
sed -i "s/x_1/$x_1/g" system/postProcessDict
sed -i "s/y_1/$y_1/g" system/postProcessDict
sed -i "s/z_1/$z_1/g" system/postProcessDict

sed -i "s/x_2/$x_2/g" system/postProcessDict
sed -i "s/y_2/$y_2/g" system/postProcessDict
sed -i "s/z_2/$z_2/g" system/postProcessDict

sed -i "s/flowdir/$direction/g" system/postProcessDict

mkdir constant/polyMesh
cp system/blockMeshDict$direction system/blockMeshDict

#Dummy fluid properties
cp system/fvSolution1 system/fvSolution
sed -i "s/nSmooth/1/g" system/fvSolution
sed -i "s/cSmooth/0.5/g" system/fvSolution

cp constant/transportProperties1 constant/transportProperties

sed -i "s/k_f/0/g" constant/transportProperties

cp -r 0_orig 0

sed -i "s/flow_rate/1e-30/g" 0/U


filename=$Image_name\.$format

if [ $compressed == 'yes' ]
then
        filename=$Image_name\.$format\.tar.gz
fi

mkdir constant/triSurface
cp $dir\/$filename constant/triSurface/.
cd constant/triSurface
if [ $compressed == 'yes' ]
then
        tar -xf $filename
fi
cd ../..

python system/createblockmesh.py --xDim $x_dim --yDim $y_dim --zDim $z_dim --xMin $x_min --xMax $x_max --yMin $y_min --yMax $y_max --zMin $z_min --zMax $z_max --nX $n_x --nY $n_y --nZ $n_z --nLevel $nlevel --refineStokes $refineStokes --res $res --Image_name $Image_name --padWidth $padWidth --pores_value $pores_value --solid_value $solid_value --eps_min $eps_min --tortIndex $tortIndex --direction $direction

cp system/topoSetDict1 system/topoSetDict

topoSet -dict system/topoSetDict > topoSet.out

subsetMesh fluidRegion -overwrite > subsetMesh.out

sed -i '/oldInternalFaces/,/}/s/type *empty;/type wall;/' constant/polyMesh/boundary

sed -i '/oldInternalFaces/,/}/s/inGroups.*;//' constant/polyMesh/boundary

# Set BCs for oldWalls
for field in p eps tinv; do
    sed -i '/oldInternalFaces/,/}/s/type.*/    type zeroGradient;/' 0/$field
done

sed -i '/oldInternalFaces/,/}/s/type.*/    type noSlip;/' 0/U

if [ $NP -gt 1 ]
then
    cp system/decomposeParDict1 system/decomposeParDict
    sed -i "s/NP/$NP/g" system/decomposeParDict
    echo -e "decomposePar"
    decomposePar > decomposePar.out

    rm -rf 0
fi

rm -rf constant/triSurface

echo -e "Mesh created. It is advised to check in paraview to confirm mesh and 0/eps are reasonable before running flow"






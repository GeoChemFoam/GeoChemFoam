#!/bin/bash

###### USERS INPUT ############################################################

#Define image name
Image_name="Kelvin1-200x200x200"

#Image directory location ($PWD if current directory)
dir="../images"

#Choose image format
format='raw'

#Choose if the image is compressed or not
compressed='yes'

# Define image dimensions
x_dim=200
y_dim=200
z_dim=200

#Values of solid, pore, and minimum porosity value for the solid phase (note: if the image contains solid voxels, this CANNOT be 0)
pores_value=1
solid_value=2
eps_min=0.445167

# Define cropping parameters
x_min=0
x_max=100
y_min=0
y_max=100
z_min=0
z_max=100

#padding for inlet/outlet
padWidth=0

# define resolution (m)
res=0.00001

# number of cells of initial mesh
n_x=50
n_y=50
n_z=50

#Mesh refinement level
nlevel=1
refineStokes=0

#Choose the direction of flow, 0 is x, 1 is y, 2 is z
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

cp system/fvSolution1 system/fvSolution
sed -i "s/nSmooth/1/g" system/fvSolution
sed -i "s/cSmooth/0.5/g" system/fvSolution
cp system/blockMeshDict0 system/blockMeshDict
cp constant/fvOptions$direction constant/fvOptionsRun

cp system/controlDict0 system/controlDict

rm -rf 0
mkdir 0

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

python system/createblockmesh.py --xDim $x_dim --yDim $y_dim --zDim $z_dim --xMin $x_min --xMax $x_max --yMin $y_min --yMax $y_max --zMin $z_min --zMax $z_max --nX $n_x --nY $n_y --nZ $n_z --nLevel $nlevel --refineStokes $refineStokes --res $res --Image_name $Image_name --padWidth $padWidth --pores_value $pores_value --solid_value $solid_value --eps_min $eps_min --direction $direction

if [ $NP -gt 1 ]
then
    cp system/decomposeParDict1 system/decomposeParDict
    sed -i "s/NP/$NP/g" system/decomposeParDict
    echo -e "decomposePar"
    decomposePar -constant > decomposePar.out

    rm -rf 0
fi

rm -rf constant/triSurface

echo -e "Mesh created. It is advised to check in paraview to confirm mesh and 0/eps are reasonable before running flow"

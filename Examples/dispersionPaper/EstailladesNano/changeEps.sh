#!/bin/bash

###### USERS INPUT ############################################################

#Define image name
Image_name="EstailladesNanoCyclic_0p420_600x600x600_0p032um"

#Image directory location ($PWD if current directory)
dir="."

#Choose image format
format='raw'

#Choose if the image is compressed or not
compressed='no'

# Define image dimensions
x_dim=600
y_dim=600
z_dim=600

#Values of solid, pore, and minimum porosity value for the solid phase (note: if the image contains solid voxels, this CANNOT be 0)
pores_value=0
solid_value=255
eps_min=0.0001

# Define cropping parameters
x_min=0
x_max=600
y_min=0
y_max=600
z_min=0
z_max=600

#padding for inlet/outlet
padWidth=0

# define resolution (m)
res=0.000000032

# number of cells of initial mesh
n_x=600
n_y=600
n_z=600

#Mesh refinement level
nlevel=0
refineStokes=0

# flow direction 0 or 1, 2 is empty
direction=1

#### END OF USER INPUT #######################################################

if [ $format != 'raw' ]
then
        echo "ERROR: only raw format is implemented for this solver"
        exit
fi

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


python system/createEps.py --xDim $x_dim --yDim $y_dim --zDim $z_dim --xMin $x_min --xMax $x_max --yMin $y_min --yMax $y_max --zMin $z_min --zMax $z_max --nX $n_x --nY $n_y --nZ $n_z --nLevel $nlevel --refineStokes $refineStokes --res $res --Image_name $Image_name --padWidth $padWidth --pores_value $pores_value --solid_value $solid_value --eps_min $eps_min --direction $direction

if [ -d "processor0" ]
then
    rm -rf processor*/0/*
    echo -e "decomposePar"
    decomposePar -fields > decomposePar.out
    rm -rf 0
fi

rm -rf constant/triSurface

echo -e "Eps created. It is advised to check in paraview to confirm mesh and 0/eps are reasonable before running flow"






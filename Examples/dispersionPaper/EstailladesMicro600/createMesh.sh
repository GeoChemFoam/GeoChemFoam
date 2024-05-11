#!/bin/bash

###### USERS INPUT ############################################################

#Name of your image (image must be in raw format 8 bit)
Image_name="EstailladesCyclic_14p_600x600x600_3p97um"

#Image directory location ($PWD if current directory)
dir="../images"

#Choose image format
format='raw'

#Choose if the image is compressed or not
compressed='yes'

# Define image dimensions
x_dim=600
y_dim=600
z_dim=600

#Values of solid, pore, and minimum porosity value for the solid phase (note: if the image contains solid voxels, this CANNOT be 0)
pores_value=1
solid_value=14

#define the labels of the phases
phases=(1 2 3 4 5 6 7 8 9 10 11 12 13 14)

#define the porosity of each phase, note that the porosity of the solid phase CANNOT be 0, default to 0.0001
#micro_por=('1' '0.57' '0.52' '0.47' '0.42' '0.36' '0.27' '0.22' '0.18' '0.15' '0.12' '0.09' '0.07' '0.0001')
micro_por=('1' '0.518' '0.518' '0.518' '0.518' '0.279' '0.279' '0.279' '0.279' '0.096' '0.096' '0.096' '0.096' '0.0001')

#define the permeability of each label (note: solid phase should be < 1e-20, pore should be > 1e6)
micro_k=('1e13' '5.3e-15' '5.3e-15' '5.3e-15' '5.3e-15' '8.1e-16' '8.1e-16' '8.1e-16' '8.1e-16' '3.4e-17' '3.4e-17' '3.4e-17' '3.4e-17' '1e-20')

# Define cropping parameters
x_min=200
x_max=400
y_min=200
y_max=400
z_min=200
z_max=400

#padding for inlet/outlet (minimum 2)
padWidth=0

# define resolution (m)
res=0.00000397

# number of cells of initial mesh
n_x=200
n_y=200
n_z=200

#Mesh refinement level
nlevel=0
#0=no refinment in pores, 1=refinemnet in pores
refineStokes=0

#Choose the direction of flow, 0 is x, 1 is y, 2 is z
direction=1

##Number of processors
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

python system/createblockmesh.py --xDim $x_dim --yDim $y_dim --zDim $z_dim --xMin $x_min --xMax $x_max --yMin $y_min --yMax $y_max --zMin $z_min --zMax $z_max --nX $n_x --nY $n_y --nZ $n_z --nLevel $nlevel --refineStokes $refineStokes --res $res --Image_name $Image_name --padWidth $padWidth --pores_value $pores_value --solid_value $solid_value --direction $direction --micro_por ${micro_por[@]} --micro_k ${micro_k[@]} --phases ${phases[@]}

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

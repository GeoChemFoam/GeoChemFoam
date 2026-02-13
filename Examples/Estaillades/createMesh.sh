#!/bin/bash

###### USERS INPUT ############################################################

#Define image name
Image_name="Estaillades-Z1-14p_500x1000x1000_3p9676um"

#Image directory location ($PWD if current directory)
dir="/ADD_DIRECTORY_WHERE_THE_IMAGE_IS."

#Choose image format
format='raw'

#Choose if the image is compressed or not
compressed='no'

# Define image dimensions
x_dim=500
y_dim=1000
z_dim=1000

#Values of solid, pore, and minimum porosity value for the solid phase (note: if the image contains solid voxels, this CANNOT be 0)
pores_value=0
solid_value=13

#define the labels of the phases
phases=(0 1 2 3 4 5 6 7 8 9 10 11 12 13)

#define the porosity of each phase, note that the porosity of the solid phase CANNOT be 0, default to 0.0001
#micro_por=('1' '0.0001' '0.0001' '0.0001' '0.0001' '0.0001' '0.0001' '0.0001' '0.0001' '0.0001' '0.0001' '0.0001' '0.0001' '0.0001' '0.0001')
micro_por=('1' '0.57' '0.52' '0.47' '0.42' '0.36' '0.27' '0.22' '0.18' '0.15' '0.12' '0.09' '0.07' '0.0001')
#define the permeability of each label (note: solid phase should be < 1e-20, pore should be > 1e6)
#micro_k=('7.5e11' '2e-26' '2e-26' '2e-26' '2e-26' '2e-26' '2e-26' '2e-26' '2e-26' '2e-26' '2e-26' '2e-26' '2e-26' '2e-26' '2e-26')
micro_k=('7.5e11' '7.47e-15' '6.91e-15' '4.79e-15' '3.24e-15' '2.12e-15' '8.06e-16' '4.59e-16' '2.44e-16' '1.17e-16' '4.95e-17' '1.73e-17' '4.76e-18' '2e-26')


#Definen
# Define cropping parameters
x_min=0
x_max=500
y_min=0
y_max=1000
z_min=0
z_max=1000


#padding for inlet/outlet
#This adds voxels in the image directly
padWidth=0

# define resolution (m)
res=0.0000039676

# number of cells of initial mesh
## They need to be a factor of the number of voxels in the padded image
n_x=500
n_y=1000
n_z=1000

# flow direction 0 or 1, 2 is empty
direction=0

# Number of processors
##They need to be a factor of the number of voxel in the padded image
NPX=4
NPY=4
NPZ=4

#### END OF USER INPUT #######################################################

# error check the mesh is evenly distributed over the grid of processors 
padded_n_x=$n_x
padded_n_y=$n_y
padded_n_z=$n_z
# Check if process grid is a factor of padded cropped voxel grid
if [[ $direction == 0 ]]; then
  padded_n_x=$((n_x + 2*padWidth))
fi
if [[ $(($padded_n_x % $NPX)) != 0 ]]; then
  echo "ERROR: NPX=$NPX must be a factor of the padded_n_x=$padded_n_x voxels"
  exit -1
fi
if [[ $direction == 1 ]]; then
   padded_n_y=$((n_y + 2*padWidth))
fi
if [[ $(($padded_n_y % $NPY)) != 0 ]]; then
  echo "ERROR:  NPY=$NPY must be a factor of the padded_n_y=$padded_n_y voxels"
  exit -1
fi
if [[ $direction == 2 ]]; then
  padded_n_z=$((n_z + 2*padWidth))
fi
if [[ $(($padded_n_z % $NPZ)) != 0 ]]; then
  echo "ERROR: NPZ=$NPZ must be a factor of the padded_n_z=$padded_n_z voxels"
  exit -1
fi


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

#Dummy fluid properties
cp system/fvSolution1 system/fvSolution
sed -i "s/nSmooth/1/g" system/fvSolution
sed -i "s/cSmooth/0.5/g" system/fvSolution

cp constant/transportProperties1 constant/transportProperties

sed -i "s/k_f/0/g" constant/transportProperties

mkdir -p 0

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

NP=$(echo "$NPX*$NPY*$NPZ" | bc)
if [ $NP -ge 2 ]
then 
    for ((k = 0 ; k < $NPZ ; k++ )); do
        for ((j = 0 ; j < $NPY ; j++ )); do
            for ((i = 0 ; i < $NPX ; i++ )); do 
                iproc=$(echo "$k*$NPX*$NPY+$j*$NPX+$i" | bc)
                mkdir processor$iproc
                mkdir processor$iproc/constant
                mkdir processor$iproc/constant/polyMesh
                mkdir processor$iproc/0
            done;
        done;
    done;
fi

echo $NPX >> system/NPX
echo $NPY >> system/NPY
echo $NPZ >> system/NPZ

# if PLATFORM is ARCHER2 then use srun, otherwise use serial version
if [[ "${PLATFORM}" == "ARCHER2" ]]; then

   # error check that number of process files matches number of MPI tasks in parallel job
   if [[ ${NP} != ${SLURM_NTASKS} ]]
   then
       echo "ERROR: Number of MPI tasks does not equal number of processor files"
       exit
   fi

   # prepend spindle to srun command to pre-load python modules, otherwise comment-out sprindle line to simply use srun
   spindle --slurm --python-prefix=/opt/cray/pe/python/${CRAY_PYTHON_LEVEL} \
   srun --distribution=block:block --hint=nomultithread python createMesh.py --xDim $x_dim --yDim $y_dim --zDim $z_dim --xMin $x_min --xMax $x_max --yMin $y_min --yMax $y_max --zMin $z_min --zMax $z_max --nX $n_x --nY $n_y --nZ $n_z --res $res --Image_name $Image_name --padWidth $padWidth --pores_value $pores_value --solid_value $solid_value --direction $direction --micro_por ${micro_por[@]} --micro_k ${micro_k[@]} --phases ${phases[@]}  --NPX $NPX --NPY $NPY --NPZ $NPZ


else
    mpirun python createMesh.py --xDim $x_dim --yDim $y_dim --zDim $z_dim --xMin $x_min --xMax $x_max --yMin $y_min --yMax $y_max --zMin $z_min --zMax $z_max --nX $n_x --nY $n_y --nZ $n_z --res $res --Image_name $Image_name --padWidth $padWidth --pores_value $pores_value --solid_value $solid_value --direction $direction --micro_por ${micro_por[@]} --micro_k ${micro_k[@]} --phases ${phases[@]}  --NPX $NPX --NPY $NPY --NPZ $NPZ


fi

#rm -rf constant/triSurface

echo -e "Mesh created. It is advised to check in paraview to confirm mesh and 0/eps are reasonable before running flow"






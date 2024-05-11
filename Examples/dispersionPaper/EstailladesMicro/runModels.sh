#!/bin/bash

#SBATCH --nodes=16
#SBATCH --tasks-per-node=128
#SBATCH --cpus-per-task=1
#SBATCH --distribution=block:block
#SBATCH --hint=nomultithread
#SBATCH --time=24:00:00

# Replace [budget code] below with your project code (e.g. t01)
#SBATCH --account=n03-hw
#SBATCH --partition=standard
#SBATCH --qos=standard

export PYTHONUSERBASE=/work/n03/shared/gcfoam/.local

export PATH=$PYTHONUSERBASE/bin:$PATH
export PYTHONPATH=$PYTHONUSERBASE/lib/python3.8/site-packages:$PYTHONPATH

module load cray-python
module load PrgEnv-gnu
module load openfoam/com/v2212

source /work/n03/shared/gcfoam/works/GeoChemFoam-v-dev/etc/bashrc
#./binMesh.sh
#./createMesh.sh
#./changeEps.sh
#./initCaseFlow.sh
decomposePar -fields > decomposeParFlow.out
#./runCaseFlow.sh
#srun processPoroPerm -parallel
#./processFlow.sh
#./initCaseDispersionAll.sh
#./initCaseDispersion.sh

# Pe=0.01
cp constant/transportProperties0.01 constant/transportProperties
rm -f processor*/0/D
for i in processor*;do cp $i/0/D0 $i/0/D; done
./runCaseDispersion.sh
./processDispersion.sh
cp disp.csv Pe0/.
rm -rf processor*/[1-9]*

# Pe=0.1
#cp constant/transportProperties0.1 constant/transportProperties
#rm processor*/0/D
#for i in processor*;do cp $i/0/D01 $i/0/D; done
#./runCaseDispersion.sh
#./processDispersion.sh
#cp disp.csv Pe0.1/.
#rm -rf processor*/[1-9]*

# Pe=1
#cp constant/transportPropertiesD1 constant/transportProperties
#rm processor*/0/D
#for i in processor*;do cp $i/0/D1 $i/0/D; done
#./runCaseDispersion.sh
#./processDispersion.sh
#cp disp.csv Pe1/.
#rm -rf processor*/[1-9]*

# Pe=10
#cp constant/transportProperties10 constant/transportProperties
#rm processor*/0/D
#for i in processor*;do cp $i/0/D10 $i/0/D; done
#./runCaseDispersion.sh
#./processDispersion.sh
#cp disp.csv Pe10/.
#rm -rf processor*/[1-9]*

# Pe=100
#cp constant/transportProperties100 constant/transportProperties
#rm processor*/0/D
#for i in processor*;do cp $i/0/D100 $i/0/D; done
#./runCaseDispersion.sh
#./processDispersion.sh
#cp disp.csv Pe100/.
#rm -rf processor*/[1-9]*


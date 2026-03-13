#!/bin/bash

#SBATCH --nodes=48
#SBATCH --tasks-per-node=125
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

module load other-software
module load openfoam/v2212_64
source /work/n03/shared/gcfoam/works/GeoChemFoam-v-dev/etc/bashrc

#./deleteAll.sh
./initCaseFlow.sh
./runCaseFlow.sh
./processFlow.sh
#./initCaseHeat
#./processHeat
#


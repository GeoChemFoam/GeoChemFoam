#!/bin/bash
#SBATCH --job-name=createMeshpar
#SBATCH --nodes=56
#SBATCH --ntasks-per-node=125
#SBATCH --cpus-per-task=1
#SBATCH --time=03:00:00
# Replace account code with your account code (e.g. t01)
#SBATCH --account=n03-hw
#SBATCH --partition=standard
#SBATCH --qos=standard

# Configure GCF
module load other-software
module load openfoam/v2212_64
source /work/n03/shared/gcfoam/works/GeoChemFoam-v-dev/etc/bashrc

# Enable your PVE
module load cray-python

# include when pre-loading python modules
module load load-epcc-module
module load spindle/0.13

# Set the number of threads to 1 to avoid auto-threading
export OMP_NUM_THREADS=1
# Propagate the cpus-per-task setting from script to srun commands
export SRUN_CPUS_PER_TASK=${SLURM_CPUS_PER_TASK}

export PLATFORM=ARCHER2

./createMesh.sh



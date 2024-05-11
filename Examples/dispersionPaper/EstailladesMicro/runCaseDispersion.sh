#!/bin/bash

###### USERS INPUT ############################################################

#### END OF USER INPUT

# Run simpleFoam in parallel
echo -e "Run dispersionFoam in parallel"
srun dispersionFoam -parallel  > dispersionFoamD.out

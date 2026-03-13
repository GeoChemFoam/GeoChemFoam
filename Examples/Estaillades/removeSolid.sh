#!/bin/bash

###### USERS INPUT ############################################################

#### END OF USER INPUT #######################################################

#srun topoSet -parallel > toposet.out
#srun subsetMesh pores -patch solidwalls0 -overwrite -parallel > subsetMesh.out
#srun checkMesh -parallel > checkMesh.out

srun subsetMesh region0 -overwrite -parallel > subsetMesh2.out

srun checkMesh -parallel > checkMesh2.out

srun createPatch -overwrite -parallel > createPatch.out


for i in processor*;do awk '1;/boundaryField/{c=2}c&&!--c{print "    wall_solid\n    {\n        type zeroGradient;\n    }\n"}' $i/0/eps > $i/0/eps0;  mv $i/0/eps0 $i/0/eps; done


#!/bin/bash

###### USERS INPUT ############################################################

## Define the total time of the simulation and how often to output fields
## Define initial and maximum time-step
TotalTime=20000
WriteTimestep=10000
initTimestep=5
maxTimestep=50

## Number of processor
NP=24

#### END OF USER INPUT #######################################################

set -e

cp system/fvSolutionRun system/fvSolution

rm -rf polyMesh_old
cp -r constant/polyMesh polyMesh_old

rm -rf ../temp
cp -r ../micromodel ../temp

cp system/decomposeParDict1 system/decomposeParDict
sed -i "s/NP/$NP/g" system/decomposeParDict

python << END
import os


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


a=0;
s=str(a)
removeOld = 0

os.system('echo "Time= 0 s ###############################################################################" ')
for n in range(0,$TotalTime+1,$WriteTimestep):
  os.system('cp system/controlDictRun system/controlDict')
  os.system('sed -i "s/var/'+str(n)+'/g" system/controlDict') 
  os.system('sed -i "s/WriteTimestep/$WriteTimestep/g" system/controlDict') 
  os.system('sed -i "s/initTimestep/$initTimestep/g" system/controlDict') 
  os.system('sed -i "s/maxTimestep/$maxTimestep/g" system/controlDict') 
  while a<n:
    os.system('echo "decompose parallel mesh"')
    os.system('decomposePar > decomposeParRT.out')
    os.system('echo "run reactiveTransportALEFoam"')
    os.system('mpiexec -np $NP reactiveTransportALEFoam -parallel > reactiveTransportALEFoamRT.out')
    os.system('echo "reconstruct parallel mesh"')
    os.system('reconstructPar -latestTime > reconstructParRT.out' )
    os.system('rm -rf processor*')
    if removeOld == 1:
        os.system('rm -rf '+s)
    for directories in os.listdir(os.getcwd()): 
      if (is_number(directories)):
        if (float(directories)>a):
          a=float(directories)
          s=directories
    os.system('rm polyMesh_old/points')
    os.system('cp '+s+'/polyMesh/points polyMesh_old/.')
    os.system('cp polyMesh_old/* '+s+'/polyMesh/.')
    if a<n:
      os.system('cp -r '+s+' ../temp/.')
      os.system('echo "Remesh"')
      os.system( './remesh.sh > remesh.out') 
      os.system('echo "calculate fields"')
      os.system('./calculateFields.sh > calculateFields.out')
      os.system('cd ../micromodel')
      os.system('rm -rf '+s)
      os.system('mv ../temp/0 ./'+s)
      os.system('cp '+s+'/polyMesh/* polyMesh_old/.')
      os.system('echo " "')
      removeOld=1
    else:
      removeOld=0
    os.system('echo "Time='+str(s)+r' seconds ###############################################################################"')
END

processPoroPerm

rm -rf ../temp
rm -rf polyMesh_old

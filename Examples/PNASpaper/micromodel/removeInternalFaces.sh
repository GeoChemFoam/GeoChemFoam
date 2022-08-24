#!/bin/bash




# ###### DO NOT MAKE CHANGES FROM HERE ###################################



set -e


python << END
import os
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
a=0;
s=str(0)
for directories in os.listdir(os.getcwd()): 
  if (is_number(directories)):
    if (float(directories)>a):
      a=float(directories)
      s=directories
os.system('rm -rf '+s+'/polyMesh/sets/*')
os.system('cp system/faceSetDict1 system/faceSetDict')
os.system('faceSet')
os.system('cp '+s+'/polyMesh/sets/solidwalls '+s+'/polyMesh/sets/collapsingFaces')
os.system('cp system/faceSetDict2 system/faceSetDict')
os.system('faceSet')
os.system('cp system/faceSetDict3 system/faceSetDict')
os.system('faceSet')
os.system('createPatch -overwrite')
END



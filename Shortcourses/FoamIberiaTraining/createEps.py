import os
import sys
import numpy as np


Image_name=sys.argv[1] 
xDim = int(sys.argv[2])
yDim = int(sys.argv[3])
zDim = int(sys.argv[4])
xMin = int(sys.argv[5])
xMax = int(sys.argv[6])
yMin = int(sys.argv[7])
yMax = int(sys.argv[8])
zMin = int(sys.argv[9])
zMax = int(sys.argv[10])
nX   = int(sys.argv[11])
nY   = int(sys.argv[12])
nZ   = int(sys.argv[13])
pores_value = float(sys.argv[14])
solid_value = float(sys.argv[15])

# open image
f = open(Image_name+'.raw', 'rb')
img = np.fromfile(f, dtype=np.uint8)
img = np.reshape(img,(zDim,yDim,xDim))
my_array = img[zMin:zMax,yMin:yMax,xMin:xMax]


#number of cells
p=int((xMax-xMin)/nX)
q=int((yMax-yMin)/nY)
r=int((zMax-zMin)/nZ)

ncells = nX*nY*nZ

eps=np.zeros((nX,nY,nZ),dtype=float)
for i in range (0,nX):
    for ii in range (0,p):
        for j in range (0,nY):
            for jj in range (0,q):
                for k in range (0,nY):
                    for kk in range (0,r):
                        eps[i,j,k]+=//*FILL VALUE OF EPS HERE*//

data = [
'/*--------------------------------*- C++ -*----------------------------------*\\\\n',
'| =========                 |                                                 |\n',
'| \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |\n',
'|  \\\\    /   O peration     | Version:  2212                                  |\n',
'|   \\\\  /    A nd           | Website:  www.openfoam.com                      |\n',
'|    \\\\/     M anipulation  |                                                 |\n',
'\\*---------------------------------------------------------------------------*/\n',
"FoamFile\n",
"{\n",
"    version     2.0;\n",
"    format      ascii;\n",
"    arch        \"LSB;label=32;scalar=64\";\n",
"    class       volScalarField;\n",
"    location    \"0\";\n",
"    object      eps;\n",
"}\n",
"// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n",
"\n",
"dimensions      [0 0 0 0 0 0 0];\n",
"\n",
"internalField   nonuniform List<scalar> \n",
f"{ncells}\n",
"(\n"
]

for k in range (0,nZ):
    for j in range (0, nY):
        for i in range (0, nX):
            data.append(str(eps[i,j,k])+'\n')
data.extend([
")\n",
";\n",
"\n",
"boundaryField\n",
"{\n"
"    inlet\n"
"    {\n",
"        type            zeroGradient;\n",
"    }\n"
"    outlet\n"
"    {\n",
"        type            zeroGradient;\n",
"    }\n"
"    walls\n"
"    {\n",
"        type            zeroGradient;\n",
"    }\n"
"}\n",
"\n",
"\n",
"// ************************************************************************* //"
])


with open('0/eps', 'w') as f:
  f.writelines(data)
  f.close()





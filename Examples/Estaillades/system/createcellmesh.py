import numpy as np
import array
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--xDim', type=int, help='xDim')
parser.add_argument('--yDim', type=int, help='yDim')
parser.add_argument('--zDim', type=int, help='zDim')
parser.add_argument('--xMin', type=int, help='xMin')
parser.add_argument('--xMax', type=int, help='xMax')
parser.add_argument('--yMin', type=int, help='yMin')
parser.add_argument('--yMax', type=int, help='yMax')
parser.add_argument('--zMin', type=int, help='zMin')
parser.add_argument('--zMax', type=int, help='zMax')
parser.add_argument('--nX', type=int, help='nX')
parser.add_argument('--nY', type=int, help='nY')
parser.add_argument('--nZ', type=int, help='nZ')
parser.add_argument('--padWidth', type=int, help='pad Width')
parser.add_argument('--direction', type=int, help='flow in x y or z?')
parser.add_argument('--NPX', type=int, help='NPX')
parser.add_argument('--NPY', type=int, help='NPY')
parser.add_argument('--NPZ', type=int, help='NPZ')


opt = parser.parse_args()

xDim=opt.xDim
yDim=opt.yDim
zDim=opt.zDim

xMin=opt.xMin
xMax=opt.xMax
yMin=opt.yMin
yMax=opt.yMax
zMin=opt.zMin
zMax=opt.zMax

nX=opt.nX
nY=opt.nY
nZ=opt.nZ
padWidth=opt.padWidth
direction=opt.direction

NPX=opt.NPX
NPY=opt.NPY
NPZ=opt.NPZ

if direction==0:
    #bounding box
    xmin=-padWidth
    xmax=xMax-xMin+padWidth
    ymin=0
    ymax=yMax-yMin
    zmin=0
    zmax=zMax-zMin
    
elif direction==1:
    #bounding box
    xmin=0
    xmax=xMax-xMin
    ymin=-padWidth
    ymax=yMax-yMin+padWidth
    zmin=0
    zmax=zMax-zMin
    
else:
    #bounding box
    xmin=0
    xmax=xMax-xMin
    ymin=0
    ymax=yMax-yMin
    zmin=-padWidth
    zmax=zMax-zMin+padWidth

#number of cells
p=int((xMax-xMin)/nX)
q=int((yMax-yMin)/nY)
r=int((zMax-zMin)/nZ)

nx1=int((xmax-xmin)/p)
ny1=int((ymax-ymin)/q)
nz1=int((zmax-zmin)/r)
        
if (NPX*NPY*NPZ>1):
    for ipz in range(0,NPZ):
        for ipy in range(0,NPY):
            for ipx in range(0,NPX):
                iproc=ipz*NPX*NPY+ipy*NPX+ipx
                
                nzp=int(np.rint(nz1/NPZ))
                nyp=int(np.rint(ny1/NPY))
                nxp=int(np.rint(nx1/NPX))
                ncells = nxp*nyp*nzp  
                                                     
                ###################################################################
                ###### cellProcAddressing #########################################
                ###################################################################              
                f=open('processor'+str(iproc)+'/constant/polyMesh/cellProcAddressing','a')
                f.seek(0) #get to the first position
                
                ##So that the files are exactly the same than with blockMesh - remove later
                f.write('/*--------------------------------*- C++ -*----------------------------------*\\'+'\n')
                f.write('| =========                 |                                                 |'+'\n')
                f.write('| \\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |'+'\n')
                f.write('|  \\\    /   O peration     | Version:  2212                                  |'+'\n')
                f.write('|   \\\  /    A nd           | Website:  www.openfoam.com                      |'+'\n')
                f.write('|    \\\/     M anipulation  |                                                 |'+'\n')
                f.write('\*---------------------------------------------------------------------------*/'+'\n')
                ######
                
                f.write("FoamFile"+'\n')
                f.write("{"+'\n')
                f.write("    version     2.0;"+'\n')
                f.write("    format      ascii;"+'\n')
                f.write("    arch        \"LSB;label=32;scalar=64\";"+'\n')
                f.write("    class       labelList;"+'\n')
                f.write("    location    \"constant/polyMesh\";"+'\n')
                f.write("    object      cellProcAddressing;"+'\n')
                f.write("}"+'\n')
                
                ##So that the files are exactly the same than with blockMesh - remove later                
                f.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //"+'\n')
                f.write('\n')
                f.write('\n')
                #####                
                f.write(str(ncells)+'\n')
                f.write("("+'\n')
 
                for k in range (0,nzp):
                    for j in range (0,nyp):
                        for i in range (0,nxp):
                            f.write(str((ipz*nzp+k)*ny1*nx1+(ipy*nyp+j)*nx1+ipx*nxp+i)+'\n')
                f.write(")"+'\n')
                
                ##So that the files are exactly the same than with blockMesh - remove later                
                f.write('\n')                
                f.write('\n')
                f.write("// ************************************************************************* //")
                ######
                f.close()

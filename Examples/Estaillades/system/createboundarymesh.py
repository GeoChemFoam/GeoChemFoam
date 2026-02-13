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

                nIfaces=nxp*nyp*(nzp-1)+nxp*(nyp-1)*nzp+(nxp-1)*nyp*nzp                                                        
                ###################################################################
                ###### boundary   #################################################
                ###################################################################
                f=open('processor'+str(iproc)+'/constant/polyMesh/boundary','a')
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
                f.write("    class       polyBoundaryMesh;"+'\n')
                f.write("    location    \"constant/polyMesh\";"+'\n')
                f.write("    object      boundary;"+'\n')
                f.write("}"+'\n')

                ##So that the files are exactly the same than with blockMesh - remove later                
                f.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //"+'\n')
                f.write('\n')
                #####

                nbound=6
                if (ipx>0):
                    nbound=nbound+1
                if (ipx<NPX-1):
                    nbound=nbound+1
                if (ipy>0):
                    nbound=nbound+1
                if (ipy<NPY-1):
                    nbound=nbound+1
                if (ipz>0):
                    nbound=nbound+1
                if (ipz<NPZ-1):
                    nbound=nbound+1                                                                                                
                f.write(str(nbound)+'\n')
                f.write("("+'\n')
 
                startFace=nIfaces
                
                ###left 
                if (ipx==0):
                    nbfaces=nyp*nzp
                else:
                    nbfaces=0
                if (direction==0):
                    f.write("    inlet"+'\n')
                else:
                    f.write("    wall_left"+'\n') 
                f.write("    {"+'\n')
                f.write("        type            patch;"+'\n')
                f.write("        nFaces          "+str(nbfaces)+";"+'\n')
                f.write("        startFace       "+str(startFace)+";"+'\n')
                f.write("    }"+'\n')
                startFace=startFace+nbfaces
                if (ipx==NPX-1):
                    nbfaces=nyp*nzp
                else:
                    nbfaces=0
                if (direction==0):
                    f.write("    outlet"+'\n')
                else:
                    f.write("    wall_right"+'\n')
                f.write("    {"+'\n')
                f.write("        type            patch;"+'\n')
                f.write("        nFaces          "+str(nbfaces)+";"+'\n')
                f.write("        startFace       "+str(startFace)+";"+'\n')
                f.write("    }"+'\n')
                startFace=startFace+nbfaces
                if (ipy==0):
                    nbfaces=nxp*nzp
                else:
                    nbfaces=0
                if (direction==1):
                    f.write("    inlet"+'\n')
                else:
                    f.write("    wall_bottom"+'\n')
                f.write("    {"+'\n')
                f.write("        type            patch;"+'\n')
                f.write("        nFaces          "+str(nbfaces)+";"+'\n')
                f.write("        startFace       "+str(startFace)+";"+'\n')
                f.write("    }"+'\n')
                startFace=startFace+nbfaces
                if (ipy==NPY-1):
                    nbfaces=nxp*nzp
                else:
                    nbfaces=0
                if (direction==1):
                    f.write("    outlet"+'\n')
                else:
                    f.write("    wall_top"+'\n')
                f.write("    {"+'\n')
                f.write("        type            patch;"+'\n')
                f.write("        nFaces          "+str(nbfaces)+";"+'\n')
                f.write("        startFace       "+str(startFace)+";"+'\n')
                f.write("    }"+'\n')
                startFace=startFace+nbfaces
                if (ipz==0):
                    nbfaces=nxp*nyp
                else:
                    nbfaces=0
                if (direction==2):
                    f.write("    inlet"+'\n')
                else:
                    f.write("    wall_front"+'\n')
                f.write("    {"+'\n')
                f.write("        type            patch;"+'\n')
                f.write("        nFaces          "+str(nbfaces)+";"+'\n')
                f.write("        startFace       "+str(startFace)+";"+'\n')
                f.write("    }"+'\n')
                startFace=startFace+nbfaces
                if (ipz==NPZ-1):
                    nbfaces=nxp*nyp
                else:
                    nbfaces=0
                if (direction==2):
                    f.write("    outlet"+'\n')
                else:
                    f.write("    wall_back"+'\n')
                f.write("    {"+'\n')
                f.write("        type            patch;"+'\n')
                f.write("        nFaces          "+str(nbfaces)+";"+'\n')
                f.write("        startFace       "+str(startFace)+";"+'\n')
                f.write("    }"+'\n')
                startFace=startFace+nbfaces
                ##proc k to k-1
                if (ipz>0):
                    f.write("    procBoundary"+str(iproc)+"to"+str(iproc-NPX*NPY)+'\n')
                    f.write("    {"+'\n')
                    f.write("        type            processor;"+'\n')                    
                    f.write("        inGroups        1(processor);"+'\n')
                    f.write("        nFaces          "+str(nxp*nyp)+";"+'\n')
                    f.write("        startFace       "+str(startFace)+";"+'\n')
                    f.write("        matchTolerance  0.0001;"+'\n')
                    f.write("        transform       unknown;"+'\n')
                    f.write("        myProcNo        "+str(iproc)+";"+'\n')
                    f.write("        neighbProcNo    "+str(iproc-NPX*NPY)+";"+'\n');                    
                    f.write("    }"+'\n')
                    startFace=startFace+nxp*nyp
                ##proc j to j-1
                if (ipy>0):
                    f.write("    procBoundary"+str(iproc)+"to"+str(iproc-NPX)+'\n')
                    f.write("    {"+'\n')
                    f.write("        type            processor;"+'\n')                    
                    f.write("        inGroups        1(processor);"+'\n')
                    f.write("        nFaces          "+str(nxp*nzp)+";"+'\n')
                    f.write("        startFace       "+str(startFace)+";"+'\n')
                    f.write("        matchTolerance  0.0001;"+'\n')
                    f.write("        transform       unknown;"+'\n')
                    f.write("        myProcNo        "+str(iproc)+";"+'\n')
                    f.write("        neighbProcNo    "+str(iproc-NPX)+";"+'\n');                    
                    f.write("    }"+'\n')
                    startFace=startFace+nxp*nzp                                  
                ##proc i to i-1
                if (ipx>0):
                    f.write("    procBoundary"+str(iproc)+"to"+str(iproc-1)+'\n')
                    f.write("    {"+'\n')
                    f.write("        type            processor;"+'\n')                    
                    f.write("        inGroups        1(processor);"+'\n')
                    f.write("        nFaces          "+str(nyp*nzp)+";"+'\n')
                    f.write("        startFace       "+str(startFace)+";"+'\n')
                    f.write("        matchTolerance  0.0001;"+'\n')
                    f.write("        transform       unknown;"+'\n')
                    f.write("        myProcNo        "+str(iproc)+";"+'\n')
                    f.write("        neighbProcNo    "+str(iproc-1)+";"+'\n');                    
                    f.write("    }"+'\n')
                    startFace=startFace+nyp*nzp  
                ##proc i to i+1
                if (ipx<NPX-1):
                    f.write("    procBoundary"+str(iproc)+"to"+str(iproc+1)+'\n')
                    f.write("    {"+'\n')
                    f.write("        type            processor;"+'\n')                    
                    f.write("        inGroups        1(processor);"+'\n')
                    f.write("        nFaces          "+str(nyp*nzp)+";"+'\n')
                    f.write("        startFace       "+str(startFace)+";"+'\n')
                    f.write("        matchTolerance  0.0001;"+'\n')
                    f.write("        transform       unknown;"+'\n')
                    f.write("        myProcNo        "+str(iproc)+";"+'\n')
                    f.write("        neighbProcNo    "+str(iproc+1)+";"+'\n');                    
                    f.write("    }"+'\n')
                    startFace=startFace+nyp*nzp
                ##proc j to j+1
                if (ipy<NPY-1):
                    f.write("    procBoundary"+str(iproc)+"to"+str(iproc+NPX)+'\n')
                    f.write("    {"+'\n')
                    f.write("        type            processor;"+'\n')                    
                    f.write("        inGroups        1(processor);"+'\n')
                    f.write("        nFaces          "+str(nxp*nzp)+";"+'\n')
                    f.write("        startFace       "+str(startFace)+";"+'\n')
                    f.write("        matchTolerance  0.0001;"+'\n')
                    f.write("        transform       unknown;"+'\n')
                    f.write("        myProcNo        "+str(iproc)+";"+'\n')
                    f.write("        neighbProcNo    "+str(iproc+NPX)+";"+'\n');                    
                    f.write("    }"+'\n')
                    startFace=startFace+nxp*nzp
                ##proc k to k+1
                if (ipz<NPZ-1):
                    f.write("    procBoundary"+str(iproc)+"to"+str(iproc+NPX*NPY)+'\n')
                    f.write("    {"+'\n')
                    f.write("        type            processor;"+'\n')                    
                    f.write("        inGroups        1(processor);"+'\n')
                    f.write("        nFaces          "+str(nxp*nyp)+";"+'\n')
                    f.write("        startFace       "+str(startFace)+";"+'\n')
                    f.write("        matchTolerance  0.0001;"+'\n')
                    f.write("        transform       unknown;"+'\n')
                    f.write("        myProcNo        "+str(iproc)+";"+'\n')
                    f.write("        neighbProcNo    "+str(iproc+NPX*NPY)+";"+'\n');                    
                    f.write("    }"+'\n')
                f.write(")"+'\n')
                ##So that the files are exactly the same than with blockMesh - remove later                
                f.write('\n')                
                f.write("// ************************************************************************* //")
    
                ###################################################################
                ###### boundaryProcAddressing #####################################
                ###################################################################
                f=open('processor'+str(iproc)+'/constant/polyMesh/boundaryProcAddressing','a')
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
                f.write("    object      boundaryProcAddressing;"+'\n')
                f.write("}"+'\n')

                ##So that the files are exactly the same than with blockMesh - remove later                
                f.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //"+'\n')
                f.write('\n')
                #####
                
                if (nbound<11):                                                                              
                    f.write(str(nbound)+"(0 1 2 3 4 5")
                    if (ipz>0):
                        f.write(" -1")
                    if (ipy>0):
                        f.write(" -1")
                    if (ipx>0):
                        f.write(" -1")
                    if (ipx<NPX-1):
                        f.write(" -1")
                    if (ipy<NPY-1):
                        f.write(" -1")
                    if (ipz<NPZ-1):
                        f.write(" -1")
                    f.write(")"+'\n')
                else:
                    f.write('\n')
                    f.write(str(nbound)+'\n')
                    f.write("("+'\n')
                    f.write("0"+'\n')
                    f.write("1"+'\n')
                    f.write("2"+'\n')
                    f.write("3"+'\n')
                    f.write("4"+'\n')
                    f.write("5"+'\n')
                    if (ipz>0):
                        f.write("-1"+'\n')
                    if (ipy>0):
                        f.write("-1"+'\n')
                    if (ipx>0):
                        f.write("-1"+'\n')
                    if (ipx<NPX-1):
                        f.write("-1"+'\n')
                    if (ipy<NPY-1):
                        f.write("-1"+'\n')
                    if (ipz<NPZ-1):
                        f.write("-1"+'\n')               
                    f.write(")"+'\n')
                    f.write('\n')
                ##So that the files are exactly the same than with blockMesh - remove later                
                f.write('\n')                
                f.write("// ************************************************************************* //")               
                ######
                f.close()

else:
    nIfaces=nx1*ny1*(nz1-1)+nx1*(ny1-1)*nz1+(nx1-1)*ny1*nz1
    
    
    ###################################################################
    ###### boundary   #################################################
    ###################################################################
    f=open('constant/polyMesh/boundary','a')
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
    f.write("    class       polyBoundaryMesh;"+'\n')
    f.write("    location    \"constant/polyMesh\";"+'\n')
    f.write("    object      boundary;"+'\n')
    f.write("}"+'\n')

    ##So that the files are exactly the same than with blockMesh - remove later                
    f.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //"+'\n')
    f.write('\n')
    #####


    f.write("6"+'\n')
    f.write("("+'\n')
    if (direction==0):
        f.write("    inlet"+'\n')
    else:
        f.write("    wall_left"+'\n') 
    f.write("    {"+'\n')
    f.write("        type            patch;"+'\n')
    f.write("        nFaces          "+str(ny1*nz1)+";"+'\n')
    f.write("        startFace       "+str(nIfaces)+";"+'\n')
    f.write("    }"+'\n')
    if (direction==0):
        f.write("    outlet"+'\n')
    else:
        f.write("    wall_right"+'\n')
    f.write("    {"+'\n')
    f.write("        type            patch;"+'\n')
    f.write("        nFaces          "+str(ny1*nz1)+";"+'\n')
    f.write("        startFace       "+str(nIfaces+ny1*nz1)+";"+'\n')
    f.write("    }"+'\n')
    if (direction==1):
        f.write("    inlet"+'\n')
    else:
        f.write("    wall_bottom"+'\n')
    f.write("    {"+'\n')
    f.write("        type            patch;"+'\n')
    f.write("        nFaces          "+str(nx1*nz1)+";"+'\n')
    f.write("        startFace       "+str(nIfaces+2*ny1*nz1)+";"+'\n')
    f.write("    }"+'\n')
    if (direction==1):
        f.write("    outlet"+'\n')
    else:
        f.write("    wall_top"+'\n')
    f.write("    {"+'\n')
    f.write("        type            patch;"+'\n')
    f.write("        nFaces          "+str(nx1*nz1)+";"+'\n')
    f.write("        startFace       "+str(nIfaces+2*ny1*nz1+nx1*nz1)+";"+'\n')
    f.write("    }"+'\n')
    if (direction==2):
        f.write("    inlet"+'\n')
    else:
        f.write("    wall_front"+'\n')
    f.write("    {"+'\n')
    f.write("        type            patch;"+'\n')
    f.write("        nFaces          "+str(nx1*ny1)+";"+'\n')
    f.write("        startFace       "+str(nIfaces+2*ny1*nz1+2*nx1*nz1)+";"+'\n')
    f.write("    }"+'\n')
    if (direction==2):
        f.write("    outlet"+'\n')
    else:
        f.write("    wall_back"+'\n')
    f.write("    {"+'\n')
    f.write("        type            patch;"+'\n')
    f.write("        nFaces          "+str(nx1*ny1)+";"+'\n')
    f.write("        startFace       "+str(nIfaces+2*ny1*nz1+2*nx1*nz1+nx1*ny1)+";"+'\n')
    f.write("    }"+'\n')
    f.write(")"+'\n')
                    
    ##So that the files are exactly the same than with blockMesh - remove later                
    f.write('\n')                
    f.write("// ************************************************************************* //")
    
    ######
    f.close()

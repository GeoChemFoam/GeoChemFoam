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
parser.add_argument('--rank', type=int, help='rank')

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

rank=opt.rank

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
              if(rank==iproc):

                nzp=int(np.rint(nz1/NPZ))
                nyp=int(np.rint(ny1/NPY))
                nxp=int(np.rint(nx1/NPX))
                ncells = nxp*nyp*nzp  
                npoints=(nxp+1)*(nyp+1)*(nzp+1)                                                     
                ###################################################################
                ###### faces  #####################################################
                ###################################################################

                nfaces=(nxp+1)*nyp*nzp+nxp*(nyp+1)*nzp+nxp*nyp*(nzp+1)
                nIfaces=nxp*nyp*(nzp-1)+nxp*(nyp-1)*nzp+(nxp-1)*nyp*nzp
                f=open('processor'+str(iproc)+'/constant/polyMesh/faces','a')
                f.seek(0) #get to the first position

                ##So that the files are exactly the same than with blockMesh - remove later
                f.write('/*--------------------------------*- C++ -*----------------------------------*\\'+'\n')
                f.write('| =========                 |                                                 |'+'\n')
                f.write('| \\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |'+'\n')
                f.write('|  \\\    /   O peration     | Version:  2212                                  |'+'\n')
                f.write('|   \\\  /    A nd           | Website:  www.openfoam.com                      |'+'\n')
                f.write('|    \\\/     M anipulation  |                                                 |'+'\n')
                f.write('\*---------------------------------------------------------------------------*/'+'\n')
                ####
                
                f.write("FoamFile"+'\n')
                f.write("{"+'\n')
                f.write("    version     2.0;"+'\n')
                f.write("    format      ascii;"+'\n')
                f.write("    arch        \"LSB;label=32;scalar=64\";"+'\n')
                f.write("    class       faceList;"+'\n')
                f.write("    location    \"constant/polyMesh\";"+'\n')
                f.write("    object      faces;"+'\n')
                f.write("}"+'\n')

                ##So that the files are exactly the same than with blockMesh - remove later
                f.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //"+'\n')
                f.write('\n')
                f.write('\n')
                #####

                f.write(str(nfaces)+'\n')
                f.write("("+'\n')

                ##internal faces
                for k in range(0,nzp):
                    for j in range(0,nyp):
                        for i in range (0,nxp):
                            if (i<nxp-1):
                                ## i->i+1 face
                                x1=k*(nxp+1)*(nyp+1)+j*(nxp+1)+i+1
                                x2=k*(nxp+1)*(nyp+1)+(j+1)*(nxp+1)+i+1
                                x3=(k+1)*(nxp+1)*(nyp+1)+(j+1)*(nxp+1)+i+1
                                x4=(k+1)*(nxp+1)*(nyp+1)+j*(nxp+1)+i+1
                                f.write("4("+str(x1)+" "+str(x2)+" "+str(x3)+" "+str(x4)+")"+'\n')
                            if (j<nyp-1):
                                ## j->j+1 face
                                x1=k*(nxp+1)*(nyp+1)+(j+1)*(nxp+1)+i
                                x2=(k+1)*(nxp+1)*(nyp+1)+(j+1)*(nxp+1)+i
                                x3=(k+1)*(nxp+1)*(nyp+1)+(j+1)*(nxp+1)+i+1
                                x4=k*(nxp+1)*(nyp+1)+(j+1)*(nxp+1)+i+1
                                f.write("4("+str(x1)+" "+str(x2)+" "+str(x3)+" "+str(x4)+")"+'\n')
                            if (k<nzp-1):
                                x1=(k+1)*(nxp+1)*(nyp+1)+j*(nxp+1)+i
                                x2=(k+1)*(nxp+1)*(nyp+1)+j*(nxp+1)+i+1
                                x3=(k+1)*(nxp+1)*(nyp+1)+(j+1)*(nxp+1)+i+1
                                x4=(k+1)*(nxp+1)*(nyp+1)+(j+1)*(nxp+1)+i
                                f.write("4("+str(x1)+" "+str(x2)+" "+str(x3)+" "+str(x4)+")"+'\n')
                if (ipx==0):
                    ##Left boundary
                    for k in range(0,nzp):
                        for j in range(0,nyp):
                            ##left face of (jth,kth) column
                            x1=k*(nxp+1)*(nyp+1)+j*(nxp+1)
                            x2=(k+1)*(nxp+1)*(nyp+1)+j*(nxp+1)
                            x3=(k+1)*(nxp+1)*(nyp+1)+(j+1)*(nxp+1)
                            x4=k*(nxp+1)*(nyp+1)+(j+1)*(nxp+1)
                            f.write("4("+str(x1)+" "+str(x2)+" "+str(x3)+" "+str(x4)+")"+'\n')
                            
                if (ipx==NPX-1):
                    ##right boundary
                    for k in range(0,nzp):
                        for j in range(0,nyp):
                            ##left face of (jth,kth) column
                            x1=k*(nxp+1)*(nyp+1)+j*(nxp+1)+nxp
                            x2=k*(nxp+1)*(nyp+1)+(j+1)*(nxp+1)+nxp
                            x3=(k+1)*(nxp+1)*(nyp+1)+(j+1)*(nxp+1)+nxp
                            x4=(k+1)*(nxp+1)*(nyp+1)+j*(nxp+1)+nxp
                            f.write("4("+str(x1)+" "+str(x2)+" "+str(x3)+" "+str(x4)+")"+'\n')
                if (ipy==0):
                    ##bottom boundary
                    for i in range(0,nxp):
                        for k in range(0,nzp):
                            ##bottom face of (ith,kth) column
                            x1=k*(nxp+1)*(nyp+1)+i
                            x2=k*(nxp+1)*(nyp+1)+i+1
                            x3=(k+1)*(nxp+1)*(nyp+1)+i+1
                            x4=(k+1)*(nxp+1)*(nyp+1)+i
                            f.write("4("+str(x1)+" "+str(x2)+" "+str(x3)+" "+str(x4)+")"+'\n')
                if (ipy==NPY-1):
                    ##top boundary
                    for i in range(0,nxp):
                        for k in range(0,nzp):
                            ##bottom face of (ith,kth) column
                            x1=k*(nxp+1)*(nyp+1)+nyp*(nxp+1)+i
                            x2=(k+1)*(nxp+1)*(nyp+1)+nyp*(nxp+1)+i
                            x3=(k+1)*(nxp+1)*(nyp+1)+nyp*(nxp+1)+i+1
                            x4=k*(nxp+1)*(nyp+1)+nyp*(nxp+1)+i+1
                            f.write("4("+str(x1)+" "+str(x2)+" "+str(x3)+" "+str(x4)+")"+'\n')
                            
                if (ipz==0):
                    ##front boundary
                    for i in range(0,nxp):
                        for j in range(0,nyp):
                            ##bottom face of (ith,kth) column
                            x1=j*(nxp+1)+i
                            x2=(j+1)*(nxp+1)+i
                            x3=(j+1)*(nxp+1)+i+1
                            x4=j*(nxp+1)+i+1
                            f.write("4("+str(x1)+" "+str(x2)+" "+str(x3)+" "+str(x4)+")"+'\n')
                
                if (ipz==NPZ-1):        
                    ##back boundary
                    for i in range(0,nxp):
                        for j in range(0,nyp):
                        ##bottom face of (ith,kth) column
                            x1=nzp*(nxp+1)*(nyp+1)+j*(nxp+1)+i
                            x2=nzp*(nxp+1)*(nyp+1)+j*(nxp+1)+i+1
                            x3=nzp*(nxp+1)*(nyp+1)+(j+1)*(nxp+1)+i+1
                            x4=nzp*(nxp+1)*(nyp+1)+(j+1)*(nxp+1)+i
                            f.write("4("+str(x1)+" "+str(x2)+" "+str(x3)+" "+str(x4)+")"+'\n')

                if (ipz>0):
                    ##proc in front
                    for j in range(0,nyp):
                        for i in range(0,nxp):
                            ##bottom face of (ith,kth) column
                            x1=j*(nxp+1)+i
                            x2=(j+1)*(nxp+1)+i
                            x3=(j+1)*(nxp+1)+i+1
                            x4=j*(nxp+1)+i+1
                            f.write("4("+str(x1)+" "+str(x2)+" "+str(x3)+" "+str(x4)+")"+'\n')
                            
                if (ipy>0):
                    ##proc in bottom
                    for k in range(0,nzp):
                        for i in range(0,nxp):
                            ##bottom face of (ith,kth) column
                            x1=k*(nxp+1)*(nyp+1)+i
                            x2=k*(nxp+1)*(nyp+1)+i+1
                            x3=(k+1)*(nxp+1)*(nyp+1)+i+1
                            x4=(k+1)*(nxp+1)*(nyp+1)+i
                            f.write("4("+str(x1)+" "+str(x2)+" "+str(x3)+" "+str(x4)+")"+'\n')

                if (ipx>0):
                    ##proc on the left
                    for k in range(0,nzp):
                        for j in range(0,nyp):
                            ##left face of (jth,kth) column
                            x1=k*(nxp+1)*(nyp+1)+j*(nxp+1)
                            x2=(k+1)*(nxp+1)*(nyp+1)+j*(nxp+1)
                            x3=(k+1)*(nxp+1)*(nyp+1)+(j+1)*(nxp+1)
                            x4=k*(nxp+1)*(nyp+1)+(j+1)*(nxp+1)
                            f.write("4("+str(x1)+" "+str(x2)+" "+str(x3)+" "+str(x4)+")"+'\n')
                if (ipx<NPX-1):
                    ##proc on the right
                    for k in range(0,nzp):
                        for j in range(0,nyp):
                            ##left face of (jth,kth) column
                            x1=k*(nxp+1)*(nyp+1)+j*(nxp+1)+nxp
                            x2=k*(nxp+1)*(nyp+1)+(j+1)*(nxp+1)+nxp
                            x3=(k+1)*(nxp+1)*(nyp+1)+(j+1)*(nxp+1)+nxp
                            x4=(k+1)*(nxp+1)*(nyp+1)+j*(nxp+1)+nxp
                            f.write("4("+str(x1)+" "+str(x2)+" "+str(x3)+" "+str(x4)+")"+'\n')

                if (ipy<NPY-1):
                    ##proc on top
                    for k in range(0,nzp):
                        for i in range(0,nxp):
                            ##bottom face of (ith,kth) column
                            x1=k*(nxp+1)*(nyp+1)+nyp*(nxp+1)+i
                            x2=(k+1)*(nxp+1)*(nyp+1)+nyp*(nxp+1)+i
                            x3=(k+1)*(nxp+1)*(nyp+1)+nyp*(nxp+1)+i+1
                            x4=k*(nxp+1)*(nyp+1)+nyp*(nxp+1)+i+1
                            f.write("4("+str(x1)+" "+str(x2)+" "+str(x3)+" "+str(x4)+")"+'\n')
                            
                if (ipz<NPZ-1):        
                    ##proc on back
                    for j in range(0,nyp):
                        for i in range(0,nxp):
                            ##bottom face of (ith,kth) column
                            x1=nzp*(nxp+1)*(nyp+1)+j*(nxp+1)+i
                            x2=nzp*(nxp+1)*(nyp+1)+j*(nxp+1)+i+1
                            x3=nzp*(nxp+1)*(nyp+1)+(j+1)*(nxp+1)+i+1
                            x4=nzp*(nxp+1)*(nyp+1)+(j+1)*(nxp+1)+i
                            f.write("4("+str(x1)+" "+str(x2)+" "+str(x3)+" "+str(x4)+")"+'\n')

                            
                f.write(")"+'\n')

                ##So that the files are exactly the same than with blockMesh - remove later                
                f.write('\n')                
                f.write('\n')
                f.write("// ************************************************************************* //")
                ######

                f.close()
                
                ###################################################################
                ###### faceProcAddressing  ######################################
                ###################################################################
                
                f=open('processor'+str(iproc)+'/constant/polyMesh/faceProcAddressing','a')
                f.seek(0) #get to the first position

                ##So that the files are exactly the same than with blockMesh - remove later
                f.write('/*--------------------------------*- C++ -*----------------------------------*\\'+'\n')
                f.write('| =========                 |                                                 |'+'\n')
                f.write('| \\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |'+'\n')
                f.write('|  \\\    /   O peration     | Version:  2212                                  |'+'\n')
                f.write('|   \\\  /    A nd           | Website:  www.openfoam.com                      |'+'\n')
                f.write('|    \\\/     M anipulation  |                                                 |'+'\n')
                f.write('\*---------------------------------------------------------------------------*/'+'\n')
                ####
                
                f.write("FoamFile"+'\n')
                f.write("{"+'\n')
                f.write("    version     2.0;"+'\n')
                f.write("    format      ascii;"+'\n')
                f.write("    arch        \"LSB;label=32;scalar=64\";"+'\n')
                f.write("    class       labelList;"+'\n')
                f.write("    location    \"constant/polyMesh\";"+'\n')
                f.write("    object      faceProcAddressing;"+'\n')
                f.write("}"+'\n')

                ##So that the files are exactly the same than with blockMesh - remove later
                f.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //"+'\n')
                f.write('\n')
                f.write('\n')
                #####
                
                f.write(str(nfaces)+'\n')
                f.write("("+'\n')
                
                ##internal faces
                for k in range(0,nzp-1):
                    for j in range(0,nyp-1):
                        for i in range (0,nxp-1):
                            f.write(str((k+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(j+ipy*nyp)*((nx1-1)+2*nx1)+(i+ipx*nxp)*3+1)+'\n')
                            f.write(str((k+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(j+ipy*nyp)*((nx1-1)+2*nx1)+(i+ipx*nxp)*3+2)+'\n')
                            f.write(str((k+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(j+ipy*nyp)*((nx1-1)+2*nx1)+(i+ipx*nxp)*3+3)+'\n')
                        ##i=nxp
                        if (ipx==NPX-1):
                            ### right boundary is external in global mesh
                            f.write(str((k+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(j+ipy*nyp)*((nx1-1)+2*nx1)+(nxp-1+ipx*nxp)*3+1)+'\n')
                            f.write(str((k+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(j+ipy*nyp)*((nx1-1)+2*nx1)+(nxp-1+ipx*nxp)*3+2)+'\n')
                        else:
                            f.write(str((k+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(j+ipy*nyp)*((nx1-1)+2*nx1)+(nxp-1+ipx*nxp)*3+2)+'\n')
                            f.write(str((k+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(j+ipy*nyp)*((nx1-1)+2*nx1)+(nxp-1+ipx*nxp)*3+3)+'\n')
                    ##j=nyp
                    if (ipy==NPY-1):
                        ### top boundary is external in global mesh
                        for i in range (0,nxp-1):
                            f.write(str((k+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+(i+ipx*nxp)*2+1)+'\n')
                            f.write(str((k+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+(i+ipx*nxp)*2+2)+'\n')                     
                        ##i=nxp
                        if (ipx==NPX-1):
                            ### right boundary is external in global mesh
                            f.write(str((k+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+((nyp-1)+ipy*nyp)*((nx1-1)+2*nx1)+(nxp-1+ipx*nxp)*2+1)+'\n')
                        else:
                            f.write(str((k+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+((nyp-1)+ipy*nyp)*((nx1-1)+2*nx1)+(nxp-1+ipx*nxp)*2+2)+'\n')
                    else:
                        for i in range (0,nxp-1):
                            f.write(str((k+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+(i+ipx*nxp)*3+1)+'\n')
                            f.write(str((k+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+(i+ipx*nxp)*3+3)+'\n')                        
                        ##i=nxp
                        if (ipx==NPX-1):
                          ### right boundary is external in global mesh
                          f.write(str((k+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+((nyp-1)+ipy*nyp)*((nx1-1)+2*nx1)+((nxp-1)+ipx*nxp)*3+2)+'\n')
                        else:
                          f.write(str((k+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+((nyp-1)+ipy*nyp)*((nx1-1)+2*nx1)+((nxp-1)+ipx*nxp)*3+3)+'\n')
                ###k=nzp-1
                if (ipz==NPZ-1):
                    ###k=back boundary is external in global mesh
                    for j in range (0,nyp-1):
                        for i in range (0,nxp-1):
                            f.write(str(((nzp-1)+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(j+ipy*nyp)*((nx1-1)+nx1)+(i+ipx*nxp)*2+1)+'\n')
                            f.write(str(((nzp-1)+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(j+ipy*nyp)*((nx1-1)+nx1)+(i+ipx*nxp)*2+2)+'\n')
                        ### i=nxp-1
                        if (ipx==NPX-1):
                            ### right boundary is external in global mesh
                            f.write(str(((nzp-1)+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(j+ipy*nyp)*((nx1-1)+nx1)+((nxp-1)+ipx*nxp)*2+1)+'\n')
                        else:
                            f.write(str(((nzp-1)+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(j+ipy*nyp)*((nx1-1)+nx1)+((nxp-1)+ipx*nxp)*2+2)+'\n')
                    ### j=nyp-1
                    if (ipy==NPY-1):
                        for i in range (0,nxp-1):
                            f.write(str(((nzp-1)+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+((nyp-1)+ipy*nyp)*((nx1-1)+nx1)+(i+ipx*nxp)+1)+'\n')
                    else:
                        for i in range (0,nxp-1):
                            f.write(str(((nzp-1)+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+((nyp-1)+ipy*nyp)*((nx1-1)+nx1)+(i+ipx*nxp)*2+1)+'\n')
                else:
                    for j in range (0,nyp-1):
                        for i in range (0,nxp-1):
                            f.write(str(((nzp-1)+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(j+ipy*nyp)*((nx1-1)+2*nx1)+(i+ipx*nxp)*3+1)+'\n')
                            f.write(str(((nzp-1)+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(j+ipy*nyp)*((nx1-1)+2*nx1)+(i+ipx*nxp)*3+2)+'\n')
                        ### i=nxp-1
                        if (ipx==NPX-1):
                            ### right boundary is external in global mesh
                            f.write(str(((nzp-1)+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(j+ipy*nyp)*((nx1-1)+2*nx1)+((nxp-1)+ipx*nxp)*3+1)+'\n')
                        else:
                            f.write(str(((nzp-1)+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(j+ipy*nyp)*((nx1-1)+2*nx1)+((nxp-1)+ipx*nxp)*3+2)+'\n')
                    ### j=nyp-1
                    if (ipy==NPY-1):
                        for i in range (0,nxp-1):
                            f.write(str(((nzp-1)+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+((nyp-1)+ipy*nyp)*((nx1-1)+2*nx1)+(i+ipx*nxp)*2+1)+'\n')
                    else:
                        for i in range (0,nxp-1):
                            f.write(str(((nzp-1)+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+((nyp-1)+ipy*nyp)*((nx1-1)+2*nx1)+(i+ipx*nxp)*3+1)+'\n')
                            
                if (ipx==0):
                    ##Left boundary
                    for k in range(0,nzp):
                        for j in range(0,nyp):
                            f.write(str(nx1*ny1*(nz1-1)+nx1*(ny1-1)*nz1+(nx1-1)*ny1*nz1+(k+ipz*nzp)*ny1+j+ipy*nyp+1)+'\n')
                
                if (ipx==NPX-1):
                    ##right boundary
                    for k in range(0,nzp):
                        for j in range(0,nyp):
                            f.write(str(nx1*ny1*(nz1-1)+nx1*(ny1-1)*nz1+(nx1-1)*ny1*nz1+ny1*nz1+(k+ipz*nzp)*ny1+j+ipy*nyp+1)+'\n')
                if (ipy==0):
                    ##bottom boundary
                    for i in range(0,nxp):
                        for k in range(0,nzp):
                            f.write(str(nx1*ny1*(nz1-1)+nx1*(ny1-1)*nz1+(nx1-1)*ny1*nz1+2*ny1*nz1+(i+ipx*nxp)*nz1+k+ipz*nzp+1)+'\n')
                            
                if (ipy==NPY-1):
                    ##top boundary
                    for i in range(0,nxp):
                        for k in range(0,nzp):
                            f.write(str(nx1*ny1*(nz1-1)+nx1*(ny1-1)*nz1+(nx1-1)*ny1*nz1+2*ny1*nz1+nx1*nz1+(i+ipx*nxp)*nz1+(k+ipz*nzp)+1)+'\n')
                            
                if (ipz==0):
                    ##front boundary
                    for i in range(0,nxp):
                        for j in range(0,nyp):
                            f.write(str(nx1*ny1*(nz1-1)+nx1*(ny1-1)*nz1+(nx1-1)*ny1*nz1+2*ny1*nz1+2*nx1*nz1+(i+ipx*nxp)*ny1+j+ipy*nyp+1)+'\n')
                            
                if (ipz==NPZ-1):
                    ##back boundary
                    for i in range(0,nxp):
                        for j in range(0,nyp):
                            f.write(str(nx1*ny1*(nz1-1)+nx1*(ny1-1)*nz1+(nx1-1)*ny1*nz1+2*ny1*nz1+2*nx1*nz1+nx1*ny1+(i+ipx*nxp)*ny1+j+ipy*nyp+1)+'\n')
 
                if (ipz>0):
                    ##proc k to proc k-1
                    for j in range(0,nyp-1):
                        for i in range(0,nxp-1):
                            f.write(str(-((ipz*nzp-1)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(j+ipy*nyp)*((nx1-1)+2*nx1)+(i+ipx*nxp)*3+3))+'\n')
                        ##i=nxp-1
                        if (ipx==NPX-1):
                            ##right boundary is external in global mesh
                            f.write(str(-((ipz*nzp-1)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(j+ipy*nyp)*((nx1-1)+2*nx1)+(nxp-1+ipx*nxp)*3+2))+'\n')
                        else:
                            f.write(str(-((ipz*nzp-1)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(j+ipy*nyp)*((nx1-1)+2*nx1)+(nxp-1+ipx*nxp)*3+3))+'\n')
                    #j=nyp-1
                    if (ipy==NPY-1):
                        ##top boundary is external in global mesh
                        for i in range(0,nxp-1):
                            f.write(str(-((ipz*nzp-1)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+(i+ipx*nxp)*2+2))+'\n')
                        ##i=nxp=1
                        if (ipx==NPX-1):
                            ##right boundary is external in global mesh
                            f.write(str(-((ipz*nzp-1)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+(nxp-1+ipx*nxp)*2+1))+'\n')
                        else:
                            f.write(str(-((ipz*nzp-1)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+(nxp-1+ipx*nxp)*2+2))+'\n')
                    else:
                        for i in range(0,nxp-1):
                            f.write(str(-((ipz*nzp-1)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+(i+ipx*nxp)*3+3))+'\n')
                        ##i=nxp=1
                        if (ipx==NPX-1):
                            ##right boundary is external in global mesh
                            f.write(str(-((ipz*nzp-1)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+(nxp-1+ipx*nxp)*3+2))+'\n')
                        else:
                            f.write(str(-((ipz*nzp-1)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+(nxp-1+ipx*nxp)*3+3))+'\n')
                if (ipy>0):
                    ##proc j to proc j-1
                    for k in range(0,nzp-1):
                        for i in range(0,nxp-1):
                            f.write(str(-((k+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(ipy*nyp-1)*((nx1-1)+2*nx1)+(i+ipx*nxp)*3+2))+'\n')
                        ##i=nxp=1
                        if (ipx==NPX-1):
                            ##right boundary is external in global mesh
                            f.write(str(-((k+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(ipy*nyp-1)*((nx1-1)+2*nx1)+(nxp-1+ipx*nxp)*3+1))+'\n')
                        else:
                            f.write(str(-((k+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(ipy*nyp-1)*((nx1-1)+2*nx1)+(nxp-1+ipx*nxp)*3+2))+'\n')
                    #j=nyp-1                    
                    if (ipz==NPZ-1):
                        ##back boundary is external in global mesh                    
                        for i in range(0,nxp-1):
                            f.write(str(-((nzp-1+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(ipy*nyp-1)*((nx1-1)+nx1)+(i+ipx*nxp)*2+2))+'\n')
                        ##i=nxp=1                            
                        if (ipx==NPX-1):
                            ##right boundary is external in global mesh
                            f.write(str(-((nzp-1+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(ipy*nyp-1)*((nx1-1)+nx1)+(nxp-1+ipx*nxp)*2+1))+'\n')
                        else:
                            f.write(str(-((nzp-1+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(ipy*nyp-1)*((nx1-1)+nx1)+(nxp-1+ipx*nxp)*2+2))+'\n')
                    else:
                        for i in range(0,nxp-1):
                            f.write(str(-((nzp-1+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(ipy*nyp-1)*((nx1-1)+2*nx1)+(i+ipx*nxp)*3+2))+'\n')
                        ##i=nxp=1 
                        if (ipx==NPX-1):
                            ##right boundary is external in global mesh
                            f.write(str(-((nzp-1+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(ipy*nyp-1)*((nx1-1)+2*nx1)+(nxp-1+ipx*nxp)*3+1))+'\n')
                        else:
                            f.write(str(-((nzp-1+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(ipy*nyp-1)*((nx1-1)+2*nx1)+(nxp-1+ipx*nxp)*3+2))+'\n')         
                if (ipx>0):
                    ##proc i to i-1
                    for k in range(0,nzp-1):
                        for j in range(0,nyp-1):
                            f.write(str(-((k+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(j+ipy*nyp)*((nx1-1)+2*nx1)+(ipx*nxp-1)*3+1))+'\n')
                        #j=nyp-1
                        if (ipy==NPY-1):
                            ##top boundary is external in global mesh
                            f.write(str(-((k+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+(ipx*nxp-1)*2+1))+'\n')
                        else:
                            f.write(str(-((k+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+(ipx*nxp-1)*3+1))+'\n')
                    #k=nzp-1
                    if (ipz==NPZ-1):
                        #back boundary is external in global mesh
                        for j in range(0,nyp-1):
                            f.write(str(-((nzp-1+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(j+ipy*nyp)*((nx1-1)+nx1)+(ipx*nxp-1)*2+1))+'\n')
                        #j=nyp-1
                        if (ipy==NPY-1):
                            ##top boundary is external in global mesh
                            f.write(str(-((nzp-1+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+nx1)+(ipx*nxp-1)+1))+'\n')
                        else:
                            f.write(str(-((nzp-1+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+nx1)+(ipx*nxp-1)*2+1))+'\n')
                    else:
                        for j in range(0,nyp-1):
                            f.write(str(-((nzp-1+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(j+ipy*nyp)*((nx1-1)+2*nx1)+(ipx*nxp-1)*3+1))+'\n')
                        #j=nyp-1
                        if (ipy==NPY-1):
                            ##top boundary is external in global mesh
                            f.write(str(-((nzp-1+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+(ipx*nxp-1)*2+1))+'\n')
                        else:
                            f.write(str(-((nzp-1+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+(ipx*nxp-1)*3+1))+'\n')                 
                   
                if (ipx<NPX-1):
                    ##proc i to proc i+1
                    for k in range(0,nzp-1):
                        for j in range(0,nyp-1):
                            f.write(str((k+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(j+ipy*nyp)*((nx1-1)+2*nx1)+(nxp-1+ipx*nxp)*3+1)+'\n')
                        #j=nyp-1
                        if (ipy==NPY-1):
                            ##top boundary is external in global mesh
                            f.write(str((k+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+(nxp-1+ipx*nxp)*2+1)+'\n')
                        else:
                            f.write(str((k+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+(nxp-1+ipx*nxp)*3+1)+'\n')
                    #k=nzp-1
                    if (ipz==NPZ-1):
                        #back boundary is external in global mesh
                        for j in range(0,nyp-1):
                            f.write(str((nzp-1+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(j+ipy*nyp)*((nx1-1)+nx1)+(nxp-1+ipx*nxp)*2+1)+'\n')
                        #j=nyp-1
                        if (ipy==NPY-1):
                            ##top boundary is external in global mesh
                            f.write(str((nzp-1+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+nx1)+(nxp-1+ipx*nxp)+1)+'\n')
                        else:
                            f.write(str((nzp-1+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+nx1)+(nxp-1+ipx*nxp)*2+1)+'\n')
                    else:
                        for j in range(0,nyp-1):
                            f.write(str((nzp-1+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(j+ipy*nyp)*((nx1-1)+2*nx1)+(nxp-1+ipx*nxp)*3+1)+'\n')
                        #j=nyp-1
                        if (ipy==NPY-1):
                            ##top boundary is external in global mesh
                            f.write(str((nzp-1+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+(nxp-1+ipx*nxp)*2+1)+'\n')
                        else:
                            f.write(str((nzp-1+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+(nxp-1+ipx*nxp)*3+1)+'\n')
                    
                if (ipy<NPY-1):
                    ##proc j to proc j+1
                    for k in range(0,nzp-1):
                        for i in range (0,nxp-1):
                            f.write(str((k+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+(i+ipx*nxp)*3+2)+'\n')
                        ##i=nxp=1                            
                        if (ipx==NPX-1):
                            ##right boundary is external in global mesh
                            f.write(str((k+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+((nxp-1)+ipx*nxp)*3+1)+'\n')
                        else:
                            f.write(str((k+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+((nxp-1)+ipx*nxp)*3+2)+'\n')
                    #k=nzp-1
                    if (ipz==NPZ-1):
                        #back boundary is external in global mesh
                        for i in range (0,nxp-1):
                            f.write(str((nzp-1+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+nx1)+(i+ipx*nxp)*2+2)+'\n')
                        ##i=nxp=1                            
                        if (ipx==NPX-1):
                            ##right boundary is external in global mesh
                            f.write(str((nzp-1+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+nx1)+((nxp-1)+ipx*nxp)*2+1)+'\n')
                        else:
                            f.write(str((nzp-1+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+nx1)+((nxp-1)+ipx*nxp)*2+2)+'\n')
                    else:
                        for i in range (0,nxp-1):
                            f.write(str((nzp-1+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+(i+ipx*nxp)*3+2)+'\n')
                        ##i=nxp=1                            
                        if (ipx==NPX-1):
                            ##right boundary is external in global mesh
                            f.write(str((nzp-1+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+((nxp-1)+ipx*nxp)*3+1)+'\n')
                        else:
                            f.write(str((nzp-1+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+((nxp-1)+ipx*nxp)*3+2)+'\n')
                if (ipz<NPZ-1):
                    ##proc k to proc k+1
                    for j in range (0,nyp-1):
                        for i in range (0,nxp-1):
                            f.write(str(((nzp-1)+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(j+ipy*nyp)*((nx1-1)+2*nx1)+(i+ipx*nxp)*3+3)+'\n')
                        ##i=nxp=1                            
                        if (ipx==NPX-1):
                            ##right boundary is external in global mesh
                            f.write(str(((nzp-1)+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(j+ipy*nyp)*((nx1-1)+2*nx1)+((nxp-1)+ipx*nxp)*3+2)+'\n')
                        else:
                            f.write(str(((nzp-1)+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(j+ipy*nyp)*((nx1-1)+2*nx1)+((nxp-1)+ipx*nxp)*3+3)+'\n')
                    #j=nyp-1
                    if (ipy==NPY-1):
                        ##top boundary is external in global mesh
                        for i in range (0,nxp-1):
                            f.write(str(((nzp-1)+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+(i+ipx*nxp)*2+2)+'\n')
                        ##i=nxp=1                            
                        if (ipx==NPX-1):
                            ##right boundary is external in global mesh
                            f.write(str(((nzp-1)+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+((nxp-1)+ipx*nxp)*2+1)+'\n')
                        else:
                            f.write(str(((nzp-1)+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+((nxp-1)+ipx*nxp)*2+2)+'\n')
                    else:
                        for i in range (0,nxp-1):
                            f.write(str(((nzp-1)+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+(i+ipx*nxp)*3+3)+'\n')
                        ##i=nxp=1                            
                        if (ipx==NPX-1):
                            ##right boundary is external in global mesh
                            f.write(str(((nzp-1)+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+((nxp-1)+ipx*nxp)*3+2)+'\n')
                        else:
                            f.write(str(((nzp-1)+ipz*nzp)*(ny1*(nx1-1)+(ny1-1)*nx1+ny1*nx1)+(nyp-1+ipy*nyp)*((nx1-1)+2*nx1)+((nxp-1)+ipx*nxp)*3+3)+'\n')
                f.write(")"+'\n')
                
                ##So that the files are exactly the same than with blockMesh - remove later                
                f.write('\n')                
                f.write('\n')
                f.write("// ************************************************************************* //")
                ######
                
                f.close()           

                ###################################################################
                ###### owner  #####################################################
                ###################################################################                            
                f=open('processor'+str(iproc)+'/constant/polyMesh/owner','a')
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
                f.write("    note        \"nPoints:"+str(npoints)+"  nCells:"+str(ncells)+"  nFaces:"+str(nfaces)+"  nInternalFaces:"+str(nIfaces)+"\";"+'\n')
                f.write("    class       labelList;"+'\n')
                f.write("    location    \"constant/polyMesh\";"+'\n')
                f.write("    object      owner;"+'\n')
                f.write("}"+'\n')

                ##So that the files are exactly the same than with blockMesh - remove later                
                f.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //"+'\n')
                f.write('\n')
                f.write('\n')
                #####

                f.write(str(nfaces)+'\n')
                f.write("("+'\n')
                ##internal faces
                for k in range(0,nzp):
                    for j in range(0,nyp):
                        for i in range (0,nxp):
                            if (i<nxp-1):
                                ## i->i+1 face
                                f.write(str(k*nxp*nyp+j*nxp+i)+'\n')
                            if (j<nyp-1):
                                ## j->j+1 face
                                f.write(str(k*nxp*nyp+j*nxp+i)+'\n')
                            if (k<nzp-1):
                                ## k->k+1 face
                                f.write(str(k*nxp*nyp+j*nxp+i)+'\n')
                if (ipx==0):
                    ##Left boundary
                    for k in range(0,nzp):
                        for j in range(0,nyp):
                                f.write(str(k*nxp*nyp+j*nxp)+'\n')
                            
                if (ipx==NPX-1):
                    ##right boundary
                    for k in range(0,nzp):
                        for j in range(0,nyp):
                            f.write(str(k*nxp*nyp+j*nxp+nxp-1)+'\n')
                if (ipy==0):
                    ##bottom boundary
                    for i in range(0,nxp):
                        for k in range(0,nzp):
                            f.write(str(k*nxp*nyp+i)+'\n')
                if (ipy==NPY-1):
                    ##top boundary
                    for i in range(0,nxp):
                        for k in range(0,nzp):
                            f.write(str(k*nxp*nyp+(nyp-1)*nxp+i)+'\n')
                            
                if (ipz==0):
                    ##front boundary
                    for i in range(0,nxp):
                        for j in range(0,nyp):
                            f.write(str(j*nxp+i)+'\n')
                
                if (ipz==NPZ-1):        
                    ##back boundary
                    for i in range(0,nxp):
                        for j in range(0,nyp):
                            f.write(str((nzp-1)*nxp*nyp+j*nxp+i)+'\n')

                if (ipz>0):
                    ##proc in front
                    for j in range(0,nyp):
                        for i in range(0,nxp):
                            ##bottom face of (ith,kth) column
                            f.write(str(j*nxp+i)+'\n')
                            
                if (ipy>0):
                    ##proc in bottom
                    for k in range(0,nzp):
                        for i in range(0,nxp):
                            ##bottom face of (ith,kth) column
                            f.write(str(k*nxp*nyp+i)+'\n')

                if (ipx>0):
                    ##proc on the left
                    for k in range(0,nzp):
                        for j in range(0,nyp):
                            ##left face of (jth,kth) column
                            f.write(str(k*nxp*nyp+j*nxp)+'\n')
                            
                if (ipx<NPX-1):
                    ##proc on the right
                    for k in range(0,nzp):
                        for j in range(0,nyp):
                            ##left face of (jth,kth) column
                            f.write(str(k*nxp*nyp+j*nxp+nxp-1)+'\n')

                if (ipy<NPY-1):
                    ##proc on top
                    for k in range(0,nzp):
                        for i in range(0,nxp):
                            ##bottom face of (ith,kth) column
                            f.write(str(k*nxp*nyp+(nyp-1)*nxp+i)+'\n')
                            
                if (ipz<NPZ-1):        
                    ##proc on back
                    for j in range(0,nyp):
                        for i in range(0,nxp):
                            ##bottom face of (ith,kth) column
                            f.write(str((nzp-1)*nxp*nyp+j*nxp+i)+'\n')

                            
                f.write(")"+'\n')

                ##So that the files are exactly the same than with blockMesh - remove later                
                f.write('\n')                
                f.write('\n')
                f.write("// ************************************************************************* //")
                ######

                f.close()

                ###################################################################
                ###### neighbour  #################################################
                ################################################################### 
                f=open('processor'+str(iproc)+'/constant/polyMesh/neighbour','a')
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
                f.write("    note        \"nPoints:"+str(npoints)+"  nCells:"+str(ncells)+"  nFaces:"+str(nfaces)+"  nInternalFaces:"+str(nIfaces)+"\";"+'\n')
                f.write("    class       labelList;"+'\n')
                f.write("    location    \"constant/polyMesh\";"+'\n')
                f.write("    object      neighbour;"+'\n')
                f.write("}"+'\n')

                ##So that the files are exactly the same than with blockMesh - remove later                
                f.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //"+'\n')
                f.write('\n')
                f.write('\n')
                #####

                f.write(str(nIfaces)+'\n')
                f.write("("+'\n')
                ##internal faces
                for k in range(0,nzp):
                    for j in range(0,nyp):
                        for i in range (0,nxp):
                            if (i<nxp-1):
                                ## i->i+1 face
                                f.write(str(k*nxp*nyp+j*nxp+i+1)+'\n')
                            if (j<nyp-1):
                                ## j->j+1 face
                                f.write(str(k*nxp*nyp+(j+1)*nxp+i)+'\n')
                            if (k<nzp-1):
                                ## k->k+1 face
                                f.write(str((k+1)*nxp*nyp+j*nxp+i)+'\n')                                    
                f.write(")"+'\n')

                ##So that the files are exactly the same than with blockMesh - remove later                
                f.write('\n')                
                f.write('\n')
                f.write("// ************************************************************************* //")
                ######

                f.close()


else:
    ncells = nx1*ny1*nz1 
    npoints=(nx1+1)*(ny1+1)*(nz1+1)
    
    ###################################################################
    ###### faces  #####################################################
    ###################################################################

    nfaces=(nx1+1)*ny1*nz1+nx1*(ny1+1)*nz1+nx1*ny1*(nz1+1)
    nIfaces=nx1*ny1*(nz1-1)+nx1*(ny1-1)*nz1+(nx1-1)*ny1*nz1
    f=open('constant/polyMesh/faces','a')
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
    f.write("    class       faceList;"+'\n')
    f.write("    location    \"constant/polyMesh\";"+'\n')
    f.write("    object      faces;"+'\n')
    f.write("}"+'\n')

    ##So that the files are exactly the same than with blockMesh - remove later                
    f.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //"+'\n')
    f.write('\n')
    f.write('\n')
    #####

    f.write(str(nfaces)+'\n')
    f.write("("+'\n')

    ##internal faces
    for k in range(0,nz1):
        for j in range(0,ny1):
            for i in range (0,nx1):
                if (i<nx1-1):
                    ## i->i+1 face
                    x1=k*(nx1+1)*(ny1+1)+j*(nx1+1)+i+1
                    x2=k*(nx1+1)*(ny1+1)+(j+1)*(nx1+1)+i+1
                    x3=(k+1)*(nx1+1)*(ny1+1)+(j+1)*(nx1+1)+i+1
                    x4=(k+1)*(nx1+1)*(ny1+1)+j*(nx1+1)+i+1
                    f.write("4("+str(x1)+" "+str(x2)+" "+str(x3)+" "+str(x4)+")"+'\n')
                if (j<ny1-1):
                    ## j->j+1 face
                    x1=k*(nx1+1)*(ny1+1)+(j+1)*(nx1+1)+i
                    x2=(k+1)*(nx1+1)*(ny1+1)+(j+1)*(nx1+1)+i
                    x3=(k+1)*(nx1+1)*(ny1+1)+(j+1)*(nx1+1)+i+1
                    x4=k*(nx1+1)*(ny1+1)+(j+1)*(nx1+1)+i+1
                    f.write("4("+str(x1)+" "+str(x2)+" "+str(x3)+" "+str(x4)+")"+'\n')
                if (k<nz1-1):
                    x1=(k+1)*(nx1+1)*(ny1+1)+j*(nx1+1)+i
                    x2=(k+1)*(nx1+1)*(ny1+1)+j*(nx1+1)+i+1
                    x3=(k+1)*(nx1+1)*(ny1+1)+(j+1)*(nx1+1)+i+1
                    x4=(k+1)*(nx1+1)*(ny1+1)+(j+1)*(nx1+1)+i
                    f.write("4("+str(x1)+" "+str(x2)+" "+str(x3)+" "+str(x4)+")"+'\n')

    ##Left boundary
    for k in range(0,nz1):
        for j in range(0,ny1):
          ##left face of (jth,kth) column
          x1=k*(nx1+1)*(ny1+1)+j*(nx1+1)
          x2=(k+1)*(nx1+1)*(ny1+1)+j*(nx1+1)
          x3=(k+1)*(nx1+1)*(ny1+1)+(j+1)*(nx1+1)
          x4=k*(nx1+1)*(ny1+1)+(j+1)*(nx1+1)
          f.write("4("+str(x1)+" "+str(x2)+" "+str(x3)+" "+str(x4)+")"+'\n')

    ##right boundary
    for k in range(0,nz1):
        for j in range(0,ny1):
          ##left face of (jth,kth) column
          x1=k*(nx1+1)*(ny1+1)+j*(nx1+1)+nx1
          x2=k*(nx1+1)*(ny1+1)+(j+1)*(nx1+1)+nx1
          x3=(k+1)*(nx1+1)*(ny1+1)+(j+1)*(nx1+1)+nx1
          x4=(k+1)*(nx1+1)*(ny1+1)+j*(nx1+1)+nx1
          f.write("4("+str(x1)+" "+str(x2)+" "+str(x3)+" "+str(x4)+")"+'\n')

    ##bottom boundary
    for i in range(0,nx1):
        for k in range(0,nz1):
          ##bottom face of (ith,kth) column
          x1=k*(nx1+1)*(ny1+1)+i
          x2=k*(nx1+1)*(ny1+1)+i+1
          x3=(k+1)*(nx1+1)*(ny1+1)+i+1
          x4=(k+1)*(nx1+1)*(ny1+1)+i
          f.write("4("+str(x1)+" "+str(x2)+" "+str(x3)+" "+str(x4)+")"+'\n')

    ##top boundary
    for i in range(0,nx1):
        for k in range(0,nz1):
          ##bottom face of (ith,kth) column
          x1=k*(nx1+1)*(ny1+1)+ny1*(nx1+1)+i
          x2=(k+1)*(nx1+1)*(ny1+1)+ny1*(nx1+1)+i
          x3=(k+1)*(nx1+1)*(ny1+1)+ny1*(nx1+1)+i+1
          x4=k*(nx1+1)*(ny1+1)+ny1*(nx1+1)+i+1
          f.write("4("+str(x1)+" "+str(x2)+" "+str(x3)+" "+str(x4)+")"+'\n')

    ##front boundary
    for i in range(0,nx1):
        for j in range(0,ny1):
          ##bottom face of (ith,kth) column
          x1=j*(nx1+1)+i
          x2=(j+1)*(nx1+1)+i
          x3=(j+1)*(nx1+1)+i+1
          x4=j*(nx1+1)+i+1
          f.write("4("+str(x1)+" "+str(x2)+" "+str(x3)+" "+str(x4)+")"+'\n')
        
    ##back boundary
    for i in range(0,nx1):
        for j in range(0,ny1):
          ##bottom face of (ith,kth) column
          x1=nz1*(nx1+1)*(ny1+1)+j*(nx1+1)+i
          x2=nz1*(nx1+1)*(ny1+1)+j*(nx1+1)+i+1
          x3=nz1*(nx1+1)*(ny1+1)+(j+1)*(nx1+1)+i+1
          x4=nz1*(nx1+1)*(ny1+1)+(j+1)*(nx1+1)+i
          f.write("4("+str(x1)+" "+str(x2)+" "+str(x3)+" "+str(x4)+")"+'\n')
    f.write(")"+'\n')
                
    ##So that the files are exactly the same than with blockMesh - remove later                
    f.write('\n')                
    f.write('\n')
    f.write("// ************************************************************************* //")
    ######
    f.close()

    ###################################################################
    ###### owner  #####################################################
    ###################################################################

    f=open('constant/polyMesh/owner','a')
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
    f.write("    note        \"nPoints:"+str(npoints)+"  nCells:"+str(ncells)+"  nFaces:"+str(nfaces)+"  nInternalFaces:"+str(nIfaces)+"\";"+'\n')
    f.write("    class       labelList;"+'\n')
    f.write("    location    \"constant/polyMesh\";"+'\n')
    f.write("    object      owner;"+'\n')
    f.write("}"+'\n')

    ##So that the files are exactly the same than with blockMesh - remove later                
    f.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //"+'\n')
    f.write('\n')
    f.write('\n')
    #####

    f.write(str(nfaces)+'\n')
    f.write("("+'\n')
    ##internal faces
    for k in range(0,nz1):
        for j in range(0,ny1):
            for i in range (0,nx1):
                if (i<nx1-1):
                    ## i->i+1 face
                    f.write(str(k*nx1*ny1+j*nx1+i)+'\n')
                if (j<ny1-1):
                    ## j->j+1 face
                    f.write(str(k*nx1*ny1+j*nx1+i)+'\n')
                if (k<nz1-1):
                    ## k->k+1 face
                    f.write(str(k*nx1*ny1+j*nx1+i)+'\n')

    ##Left boundary
    for k in range(0,nz1):
        for j in range(0,ny1):
          f.write(str(k*nx1*ny1+j*nx1)+'\n')

    ##right boundary
    for k in range(0,nz1):
        for j in range(0,ny1):
          f.write(str(k*nx1*ny1+j*nx1+nx1-1)+'\n')

    ##bottom boundary
    for i in range(0,nx1):
        for k in range(0,nz1):
          f.write(str(k*nx1*ny1+i)+'\n')
      
    ##top boundary
    for i in range(0,nx1):
        for k in range(0,nz1):
          f.write(str(k*nx1*ny1+(ny1-1)*nx1+i)+'\n')
      
    ##front boundary
    for i in range(0,nx1):
        for j in range(0,ny1):
          f.write(str(j*nx1+i)+'\n')
        
    ##back boundary
    for i in range(0,nx1):
        for j in range(0,ny1):
          f.write(str((nz1-1)*nx1*ny1+j*nx1+i)+'\n')
    f.write(")"+'\n')
                
    ##So that the files are exactly the same than with blockMesh - remove later                
    f.write('\n')                
    f.write('\n')
    f.write("// ************************************************************************* //")
    ######
    f.close()

    ###################################################################
    ###### neighbour  #################################################
    ###################################################################
    f=open('constant/polyMesh/neighbour','a')
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
    f.write("    note        \"nPoints:"+str(npoints)+"  nCells:"+str(ncells)+"  nFaces:"+str(nfaces)+"  nInternalFaces:"+str(nIfaces)+"\";"+'\n')
    f.write("    class       labelList;"+'\n')
    f.write("    location    \"constant/polyMesh\";"+'\n')
    f.write("    object      neighbour;"+'\n')
    f.write("}"+'\n')

    ##So that the files are exactly the same than with blockMesh - remove later                
    f.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //"+'\n')
    f.write('\n')
    f.write('\n')
    #####

    f.write(str(nIfaces)+'\n')
    f.write("("+'\n')
    ##internal faces
    for k in range(0,nz1):
        for j in range(0,ny1):
            for i in range (0,nx1):
                if (i<nx1-1):
                    ## i->i+1 face
                    f.write(str(k*nx1*ny1+j*nx1+i+1)+'\n')
                if (j<ny1-1):
                    ## j->j+1 face
                    f.write(str(k*nx1*ny1+(j+1)*nx1+i)+'\n')
                if (k<nz1-1):
                    f.write(str((k+1)*nx1*ny1+j*nx1+i)+'\n')
    f.write(")"+'\n')
                
    ##So that the files are exactly the same than with blockMesh - remove later                
    f.write('\n')                
    f.write('\n')
    f.write("// ************************************************************************* //")
    ######
    f.close()
    


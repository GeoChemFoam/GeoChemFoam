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
parser.add_argument('--Image_name', help='name of image')
parser.add_argument('--padWidth', type=int, help='pad Width')
parser.add_argument('--pores_value', type=int, help='value of pores')
parser.add_argument('--solid_value', type=float, help='value of solid phase')
parser.add_argument('--direction', type=int, help='flow in x y or z?')
parser.add_argument('--micro_k', nargs='+')
parser.add_argument('--phases', nargs='+', type=int)
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

Image_name= opt.Image_name
padWidth=opt.padWidth
pores_value=opt.pores_value
solid_value=opt.solid_value
direction=opt.direction

micro_k=opt.micro_k
phases=opt.phases


NPX=opt.NPX
NPY=opt.NPY
NPZ=opt.NPZ

# open image
f = open('constant/triSurface/'+Image_name+'.raw', 'rb')
img = np.fromfile(f, dtype=np.uint8)
img = np.reshape(img,(zDim,yDim,xDim))
img_crop = img[zMin:zMax,yMin:yMax,xMin:xMax]
my_array = np.pad(img_crop,pad_width=padWidth,mode='constant',constant_values=pores_value)

if direction==0:

    #crop image to remove unecessary pad
    my_array = my_array[padWidth:padWidth+zMax-zMin,padWidth:padWidth+yMax-yMin,0:2*padWidth+xMax-xMin]

    #bounding box
    xmin=-padWidth
    xmax=xMax-xMin+padWidth
    ymin=0
    ymax=yMax-yMin
    zmin=0
    zmax=zMax-zMin
    
elif direction==1:

    #crop image to remove unecessary pad
    my_array = my_array[padWidth:padWidth+zMax-zMin,0:2*padWidth+yMax-yMin,padWidth:padWidth+xMax-xMin]
    
    #bounding box
    xmin=0
    xmax=xMax-xMin
    ymin=-padWidth
    ymax=yMax-yMin+padWidth
    zmin=0
    zmax=zMax-zMin
    
else:

    #crop image to remove unecessary pad
    my_array = my_array[0:2*padWidth+zMax-zMin,padWidth:padWidth+yMax-yMin,padWidth:padWidth+xMax-xMin]
    
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
                ncells=nxp*nyp*nzp
                ###################################################################
                ###### Kinv ########################################################
                ###################################################################
 
                ##get subarray for iproc
                my_array_p = my_array[ipz*nzp*r:(ipz+1)*nzp*r+nzp*r-1,ipy*nyp*q:(ipy+1)*nyp*q+nyp*q-1,ipx*nxp*p:(ipx+1)*nxp*p+nxp*p-1]                
                Kinv=np.zeros((nxp,nyp,nzp),dtype="float64")
                for i in range (0,nxp):
                    for ii in range (0,p):
                        for j in range (0,nyp):
                            for jj in range (0,q):
                                for k in range (0,nzp):
                                    for kk in range (0,r):
                                        a=my_array_p[k*r+kk,j*q+jj,i*p+ii]
                                        Kinv[i,j,k] +=  1/float(micro_k[np.squeeze(np.where(phases==a))])/p/q/r


                ##get subarray for proc i-1
                Kinv_bx0=np.zeros((nyp,nzp),dtype="float64")
                ##get subarray for proc i+1
                Kinv_bx1=np.zeros((nyp,nzp),dtype="float64")
                ##get subarray for proc j-1
                Kinv_by0=np.zeros((nxp,nzp),dtype="float64")
                ##get subarray for proc j+1
                Kinv_by1=np.zeros((nxp,nzp),dtype="float64")
                ##get subarray for proc k-1
                Kinv_bz0=np.zeros((nxp,nyp),dtype="float64")
                ##get subarray for proc k-1
                Kinv_bz1=np.zeros((nxp,nyp),dtype="float64")

                #proc k to k-1              
                if (ipz>0):
                   my_array_p_z0 = my_array[(ipz*nzp-1)*r:ipz*nzp*r,ipy*nyp*q:(ipy+1)*nyp*q,ipx*nxp*p:(ipx+1)*nxp*p] 
                   for i in range (0,nxp):
                       for ii in range (0,p):                       
                           for j in range (0,nyp):
                               for jj in range (0,q):
                                   for kk in range (0,r):
                                       a=my_array_p_z0[kk,j*q+jj,i*p+ii]
                                       Kinv_bz0[i,j] +=  1/float(micro_k[np.squeeze(np.where(phases==a))])/p/q/r

                #proc j to j-1              
                if (ipy>0):
                   my_array_p_y0 = my_array[ipz*nzp*r:(ipz+1)*nzp*r,(ipy*nyp-1)*q:ipy*nyp*q,ipx*nxp*p:(ipx+1)*nxp*p] 
                   for i in range (0,nxp):
                       for ii in range (0,p):                       
                           for jj in range (0,q):
                               for k in range (0,nzp):
                                   for kk in range (0,r):
                                       a=my_array_p_y0[k*r+kk,jj,i*p+ii]
                                       Kinv_by0[i,k] +=  1/float(micro_k[np.squeeze(np.where(phases==a))])/p/q/r

                #proc i to i-1              
                if (ipx>0):
                   my_array_p_x0 = my_array[ipz*nzp*r:(ipz+1)*nzp*r,ipy*nyp*q:(ipy+1)*nyp*q,(ipx*nxp-1)*p:ipx*nxp*p] 
                   for ii in range (0,p):
                       for j in range (0,nyp):
                           for jj in range (0,q):
                               for k in range (0,nzp):
                                   for kk in range (0,r):
                                       a=my_array_p_x0[k*r+kk,j*q+jj,ii]
                                       Kinv_bx0[j,k] +=  1/float(micro_k[np.squeeze(np.where(phases==a))])/p/q/r
                
                #proc i to i+1              
                if (ipx<NPX-1):
                   my_array_p_x1 = my_array[ipz*nzp*r:(ipz+1)*nzp*r,ipy*nyp*q:(ipy+1)*nyp*q,(ipx+1)*nxp*p:((ipx+1)*nxp+1)*p] 
                   for ii in range (0,p):
                       for j in range (0,nyp):
                           for jj in range (0,q):
                               for k in range (0,nzp):
                                   for kk in range (0,r):
                                       a=my_array_p_x1[k*r+kk,j*q+jj,ii]
                                       Kinv_bx1[j,k] +=  1/float(micro_k[np.squeeze(np.where(phases==a))])/p/q/r

                #proc j to j+1              
                if (ipy<NPY-1):
                   my_array_p_y1 = my_array[ipz*nzp*r:(ipz+1)*nzp*r,(ipy+1)*nyp*q:((ipy+1)*nyp+1)*q,ipx*nxp*p:(ipx+1)*nxp*p] 
                   for i in range (0,nxp):
                       for ii in range (0,p):                       
                           for jj in range (0,q):
                               for k in range (0,nzp):
                                   for kk in range (0,r):
                                       a=my_array_p_y1[k*r+kk,jj,i*p+ii]
                                       Kinv_by1[i,k] +=  1/float(micro_k[np.squeeze(np.where(phases==a))])/p/q/r

                #proc k to k+1              
                if (ipz<NPZ-1):
                   my_array_p_z1 = my_array[(ipz+1)*nzp*r:((ipz+1)+1)*nzp*r,ipy*nyp*q:(ipy+1)*nyp*q,ipx*nxp*p:(ipx+1)*nxp*p] 
                   for i in range (0,nxp):
                       for ii in range (0,p):                       
                           for j in range (0,nyp):
                               for jj in range (0,q):
                                   for kk in range (0,r):
                                       a=my_array_p_z1[kk,j*q+jj,i*p+ii]
                                       Kinv_bz1[i,j] +=  1/float(micro_k[np.squeeze(np.where(phases==a))])/p/q/r
                
                f=open('processor'+str(iproc)+'/0/Kinv','a')
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
                f.write("    class       volScalarField;"+'\n')
                f.write("    location    \"0\";"+'\n')
                f.write("    object      Kinv;"+'\n')
                f.write("}"+'\n')
                f.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //"+'\n')
                f.write(""+'\n')
                f.write("dimensions      [0 -2 0 0 0 0 0];"+'\n')
                f.write('\n')
                f.write("internalField   nonuniform List<scalar> "+'\n')
                f.write(str(ncells)+'\n')
                f.write("("+'\n')
                for k in range (0,nzp):
                    for j in range (0, nyp):
                        for i in range (0, nxp):
                            num_string = format(Kinv[i,j,k],".8f")
                            #for i in range(0,10):
                             #   if (num_string[-1]=='0') or (num_string[-1]=='.'):
                              #      num_string = num_string[:-1]
                            f.write(num_string+'\n')
                f.write(")"+'\n')
                f.write(";"+'\n')
                f.write(""+'\n')
                f.write("boundaryField"+'\n')
                f.write("{"+'\n')
                if  (direction==0):
                    f.write("    inlet"+'\n')
                else:
                    f.write("    wall_left"+'\n')
                f.write("    {"+'\n')
                f.write("        type            zeroGradient;"+'\n')
                f.write("    }"+'\n')
                if  (direction==0):
                    f.write("    outlet"+'\n')
                else:
                    f.write("    wall_right"+'\n')
                f.write("    {"+'\n')
                f.write("        type            zeroGradient;"+'\n')
                f.write("    }"+'\n')
                if (direction==1):
                    f.write("    inlet"+'\n')
                else:
                    f.write("    wall_bottom"+'\n')
                f.write("    {"+'\n')
                f.write("        type            zeroGradient;"+'\n')
                f.write("    }"+'\n')
                if (direction==1):
                    f.write("    outlet"+'\n')                
                else:
                    f.write("    wall_top"+'\n')
                f.write("    {"+'\n')
                f.write("        type            zeroGradient;"+'\n')
                f.write("    }"+'\n')
                if (direction==2):
                    f.write("    inlet"+'\n')
                else:
                    f.write("    wall_front"+'\n')
                f.write("    {"+'\n')
                f.write("        type            zeroGradient;"+'\n')
                f.write("    }"+'\n')
                if (direction==2):
                    f.write("    outlet"+'\n')                     
                else:
                    f.write("    wall_back"+'\n')
                f.write("    {"+'\n')
                f.write("        type            zeroGradient;"+'\n')
                f.write("    }"+'\n')                                    

                #f.write("    solidwalls"+'\n')
                #f.write("    {"+'\n')
                #f.write("        type            zeroGradient;"+'\n')
                #f.write("    }"+'\n')
                ##proc k to k-1                
                if (ipz>0):
                    f.write("    procBoundary"+str(iproc)+"to"+str(iproc-NPX*NPY)+'\n')
                    f.write("    {"+'\n')
                    f.write("        type            processor;"+'\n')                    
                    f.write("        value           nonuniform List<scalar> "+'\n')
                    f.write(str(nxp*nyp)+'\n')
                    f.write("("+'\n')
                    for j in range(0,nyp):
                        for i in range(0,nxp):
                            num_string = format(Kinv_bz0[i,j],".8f")
                            #for ii in range(0,10):
                             #   if (num_string[-1]=='0') or (num_string[-1]=='.'):
                              #      num_string = num_string[:-1]
                            f.write(num_string+'\n')                        
                    f.write(")"+'\n')               
                    f.write(";"+'\n')
                    f.write("    }"+'\n')
                    
                ##proc j to j-1                
                if (ipy>0):
                    f.write("    procBoundary"+str(iproc)+"to"+str(iproc-NPX)+'\n')
                    f.write("    {"+'\n')
                    f.write("        type            processor;"+'\n')                    
                    f.write("        value           nonuniform List<scalar> "+'\n')
                    f.write(str(nxp*nzp)+'\n')
                    f.write("("+'\n')
                    for k in range(0,nzp):
                        for i in range(0,nxp):
                            num_string = format(Kinv_by0[i,k],".8f")
                            #for ii in range(0,10):
                             #   if (num_string[-1]=='0') or (num_string[-1]=='.'):
                              #      num_string = num_string[:-1]
                            f.write(num_string+'\n')
                    f.write(")"+'\n')               
                    f.write(";"+'\n')
                    f.write("    }"+'\n')
                    
                ##proc i to i-1                
                if (ipx>0):
                    f.write("    procBoundary"+str(iproc)+"to"+str(iproc-1)+'\n')
                    f.write("    {"+'\n')
                    f.write("        type            processor;"+'\n')                    
                    f.write("        value           nonuniform List<scalar> "+'\n')
                    f.write(str(nyp*nzp)+'\n')
                    f.write("("+'\n')
                    for k in range(0,nzp):
                        for j in range(0,nyp):
                            num_string = format(Kinv_bx0[j,k],".8f")
                            #for ii in range(0,10):
                             #   if (num_string[-1]=='0') or (num_string[-1]=='.'):
                             #       num_string = num_string[:-1]
                            f.write(num_string+'\n')
                    f.write(")"+'\n')
                    f.write(";"+'\n')             
                    f.write("    }"+'\n')
                    
                ##proc i to i+1                
                if (ipx<NPX-1):
                    f.write("    procBoundary"+str(iproc)+"to"+str(iproc+1)+'\n')
                    f.write("    {"+'\n')
                    f.write("        type            processor;"+'\n')                    
                    f.write("        value           nonuniform List<scalar> "+'\n')
                    f.write(str(nyp*nzp)+'\n')
                    f.write("("+'\n')
                    for k in range(0,nzp):
                        for j in range(0,nyp):
                            num_string = format(Kinv_bx1[j,k],".8f")
                            #for ii in range(0,10):
                              #  if (num_string[-1]=='0') or (num_string[-1]=='.'):
                               #     num_string = num_string[:-1]
                            f.write(num_string+'\n')
                    f.write(")"+'\n')
                    f.write(";"+'\n')             
                    f.write("    }"+'\n')

                ##proc j to j+1                
                if (ipy<NPY-1):
                    f.write("    procBoundary"+str(iproc)+"to"+str(iproc+NPX)+'\n')
                    f.write("    {"+'\n')
                    f.write("        type            processor;"+'\n')                    
                    f.write("        value           nonuniform List<scalar> "+'\n')
                    f.write(str(nxp*nzp)+'\n')
                    f.write("("+'\n')
                    for k in range(0,nzp):
                        for i in range(0,nxp):
                            num_string = format(Kinv_by1[i,k],".8f")
                            #for ii in range(0,10):
                                #if (num_string[-1]=='0') or (num_string[-1]=='.'):
                                 #   num_string = num_string[:-1]
                            f.write(num_string+'\n')
                    f.write(")"+'\n')               
                    f.write(";"+'\n')
                    f.write("    }"+'\n')

                ##proc k to k+1                
                if (ipz<NPZ-1):
                    f.write("    procBoundary"+str(iproc)+"to"+str(iproc+NPX*NPY)+'\n')
                    f.write("    {"+'\n')
                    f.write("        type            processor;"+'\n')                    
                    f.write("        value           nonuniform List<scalar> "+'\n')
                    f.write(str(nxp*nyp)+'\n')
                    f.write("("+'\n')
                    for j in range(0,nyp):
                        for i in range(0,nxp):
                            num_string = format(Kinv_bz1[i,j],".8f")
                            #for ii in range(0,10):
                                #if (num_string[-1]=='0') or (num_string[-1]=='.'):
                                 #   num_string = num_string[:-1]
                            f.write(num_string+'\n')                        
                    f.write(")"+'\n')               
                    f.write(";"+'\n')
                    f.write("    }"+'\n')


                f.write("}"+'\n')
                ##So that the files are exactly the same than with blockMesh - remove later                
                f.write('\n')
                f.write('\n')                
                f.write("// ************************************************************************* //")

                f.close()              

else:
    ncells = nx1*ny1*nz1 

    ###################################################################
    ###### Kinv #####################################################
    ###################################################################
    Kinv=np.zeros((nx1,ny1,nz1),dtype=float)
    for i in range (0,nx1):
        for ii in range (0,p):
            for j in range (0,ny1):
                for jj in range (0,q):
                    for k in range (0,nz1):
                        for kk in range (0,r):
                            a=my_array[k*r+kk,j*q+jj,i*p+ii]
                            Kinv[i,j,k] +=  1/float(micro_k[np.squeeze(np.where(phases==a))])/p/q/r

    f=open('0/Kinv','a')
    f.seek(0) #get to the first position
    f.write("FoamFile"+'\n')
    f.write("{"+'\n')
    f.write("    version     2.0;"+'\n')
    f.write("    format      ascii;"+'\n')
    f.write("    class       volScalarField;"+'\n')
    f.write("    object      Kinv;"+'\n')
    f.write("}"+'\n')
    f.write(""+'\n')
    f.write("dimensions      [0 -2 0 0 0 0 0];"+'\n')
    f.write("internalField   nonuniform List<scalar>"+'\n')
    f.write(str(ncells)+'\n')
    f.write("("+'\n')
    for k in range (0,nz1):
        for j in range (0, ny1):
            for i in range (0, nx1):
                f.write(str(Kinv[i,j,k])+'\n')
    f.write(")"+'\n')
    f.write(";"+'\n')
    f.write(""+'\n')
    f.write("boundaryField"+'\n')
    f.write("{"+'\n')
    f.write("    inlet"+'\n')
    f.write("    {"+'\n')
    f.write("        type zeroGradient;"+'\n')
    f.write("    }"+'\n')
    f.write("    outlet"+'\n')
    f.write("    {"+'\n')
    f.write("        type zeroGradient;"+'\n')
    f.write("    }"+'\n')
    f.write("    \"wall_.*\""+'\n')
    f.write("    {"+'\n')
    f.write("        type zeroGradient;"+'\n')
    f.write("    }"+'\n')
    f.write("}"+'\n')
    f.close()


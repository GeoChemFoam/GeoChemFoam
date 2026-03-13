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
parser.add_argument('--micro_k', nargs='+', type=float)
parser.add_argument('--phases', nargs='+', type=int)
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

rank=opt.rank


# NPX, NPY and NPZ are the number of processors in the x, y, and z directions.
# xDim, yDim and zDim are the extents of the image file
# xMin, xMax, etc., are the lower/upper bounds of the cropped image xMin <= x < xMax
# nX, nY and nZ are are the number of cells of the initial mesh
# GJP I guess nX=xMax-xMin but then why define them separately in the calling routine

if direction==0:
   #bounding box
   xmin=-padWidth
   xmax=xMax-xMin+padWidth
   ymin=0
   ymax=yMax-yMin
   zmin=0
   zmax=zMax-zMin
   pad_in_z=0
elif direction==1:
   #bounding box
   xmin=0
   xmax=xMax-xMin
   ymin=-padWidth
   ymax=yMax-yMin+padWidth
   zmin=0
   zmax=zMax-zMin
   pad_in_z=0
else:
   direction=2
   #bounding box
   xmin=0
   xmax=xMax-xMin
   ymin=0
   ymax=yMax-yMin
   zmin=-padWidth
   zmax=zMax-zMin+padWidth
   direction=2
   pad_in_z=padWidth

#number of cells
p=int((xMax-xMin)/nX)
q=int((yMax-yMin)/nY)
r=int((zMax-zMin)/nZ)

nx1=int((xmax-xmin)/p)
ny1=int((ymax-ymin)/q)
nz1=int((zmax-zmin)/r)

nzp=int(np.rint(nz1/NPZ))
nyp=int(np.rint(ny1/NPY))
nxp=int(np.rint(nx1/NPX))
ncells=nxp*nyp*nzp

# if padding in z prepare a slice of pore_values
if direction ==2:
   my_local_pad_array = np.full((yDim*xDim), pores_value, dtype=np.uint8)

# initialise counter of local layers
local_layer=-1   

# open image
f = open('constant/triSurface/'+Image_name+'.raw', 'rb')
file_path = f.name
num_bytes = int(os.path.getsize(file_path) / float(zDim))

# run through every layer, included potential padding in z
for global_layer in range(0, zDim + 2*pad_in_z):

  # potentially adding padding in z to local my_array slice
  if global_layer < pad_in_z or global_layer >= zDim + pad_in_z:
     my_array = my_local_pad_array
     local_layer=local_layer+1
  else:
     # read layer from file into local my_array slice
     my_array = np.fromfile(f, dtype=np.uint8, count=num_bytes)
     # skip to next layer if this layer is cropped out in z
     if global_layer < zMin + pad_in_z or global_layer >= zMax + pad_in_z:
        continue
     local_layer=local_layer+1

  # convert 1D my_array to a 2D array
  my_array = np.reshape(my_array,(yDim,xDim))
  # crop that 2D array
  my_array = my_array[yMin:yMax,xMin:xMax]

  if direction==0:
    #add pad in direction 0
    my_array = np.pad(my_array,pad_width=((0,0),(padWidth,padWidth)),mode='constant',constant_values=pores_value)
  elif direction==1:
    #add pad in direction 1 
    my_array = np.pad(my_array,pad_width=((padWidth,padWidth),(0,0)),mode='constant',constant_values=pores_value)

  if (NPX*NPY*NPZ>1):
    for ipz in range(0,NPZ):
        for ipy in range(0,NPY):
            for ipx in range(0,NPX):
              iproc=ipz*NPX*NPY+ipy*NPX+ipx
              if(rank==iproc):

                ##get subarray for iproc

                # ipz is the z-coord of the proc
                # ipy is the y-coord of the proc
                # ipz is the z-coord of the proc
                # nzp is the number of cells in the z-dir for each proc
                # nyp is the number of cells in the z-dir for each proc
                # nxp is the nubmer of cells in the x-dir for each proc

                # np.concatenate cannot add layer onto pile if pile is empty, thus the first layer is a simply copy.

                if ipz*nzp*r <= local_layer < (ipz+1)*nzp*r:
                   my_array_3d = np.reshape(my_array[ipy*nyp*q:(ipy+1)*nyp*q, ipx*nxp*p:(ipx+1)*nxp*p], (1,nyp*q,nxp*p))
                   if local_layer == ipz*nzp*r:
                       my_array_p = my_array_3d
                   else:
                       my_array_p = np.concatenate((my_array_p, my_array_3d), axis=0)

                   #proc j to j-1              
                   if (ipy>0):
                      my_array_3d = np.reshape(my_array[(ipy*nyp-1)*q:ipy*nyp*q,ipx*nxp*p:(ipx+1)*nxp*p], (1,q,nxp*p))
                      if local_layer == ipz*nzp*r:
                          my_array_p_y0 = my_array_3d
                      else:
                          my_array_p_y0 = np.concatenate((my_array_p_y0, my_array_3d), axis=0)
                   #proc i to i-1              
                   if (ipx>0):
                      my_array_3d = np.reshape(my_array[ipy*nyp*q:(ipy+1)*nyp*q,(ipx*nxp-1)*p:ipx*nxp*p], (1,nyp*q,p))
                      if local_layer == ipz*nzp*r:
                          my_array_p_x0 = my_array_3d
                      else:
                          my_array_p_x0 = np.concatenate((my_array_p_x0, my_array_3d), axis=0)
                   #proc i to i+1              
                   if (ipx<NPX-1):
                      my_array_3d = np.reshape(my_array[ipy*nyp*q:(ipy+1)*nyp*q,(ipx+1)*nxp*p:((ipx+1)*nxp+1)*p], (1,nyp*q,p))
                      if local_layer == ipz*nzp*r:
                          my_array_p_x1 = my_array_3d
                      else:
                          my_array_p_x1 = np.concatenate((my_array_p_x1, my_array_3d), axis=0)
                   #proc j to j+1              
                   if (ipy<NPY-1):
                      my_array_3d = np.reshape(my_array[(ipy+1)*nyp*q:((ipy+1)*nyp+1)*q,ipx*nxp*p:(ipx+1)*nxp*p], (1,q,nxp*p))
                      if local_layer == ipz*nzp*r:
                          my_array_p_y1 = my_array_3d
                      else:
                          my_array_p_y1 = np.concatenate((my_array_p_y1, my_array_3d), axis=0)

                if (ipz*nzp-1)*r <= local_layer < ipz*nzp*r:
                   #proc k to k-1
                   if (ipz>0):
                      my_array_3d = np.reshape(my_array[ipy*nyp*q:(ipy+1)*nyp*q,ipx*nxp*p:(ipx+1)*nxp*p], (1,nyp,nxp))
                      if local_layer == (ipz*nzp-1)*r:
                          my_array_p_z0 = my_array_3d
                      else:
                          my_array_p_z0 = np.concatenate((my_array_p_z0, my_array_3d), axis=0)

                if (ipz+1)*nzp*r <= local_layer < ((ipz+1)*nzp+1)*r:
                   #proc k to k+1              
                   if (ipz<NPZ-1):
                      my_array_3d = np.reshape(my_array[ipy*nyp*q:(ipy+1)*nyp*q,ipx*nxp*p:(ipx+1)*nxp*p], (1,nyp,nxp))
                      if local_layer == (ipz+1)*nzp*r:
                          my_array_p_z1 = my_array_3d
                      else:
                          my_array_p_z1 = np.concatenate((my_array_p_z1, my_array_3d), axis=0)

if (NPX*NPY*NPZ>1):
    for ipz in range(0,NPZ):
        for ipy in range(0,NPY):
            for ipx in range(0,NPX):
              iproc=ipz*NPX*NPY+ipy*NPX+ipx
              if(rank==iproc):

                ###################################################################
                ###### Kinv ########################################################
                ###################################################################
 
                ##get subarray for iproc

                Kinv=np.zeros((nxp,nyp,nzp),dtype="float64")
                for i in range (0,nxp):
                    for ii in range (0,p):
                        for j in range (0,nyp):
                            for jj in range (0,q):
                                for k in range (0,nzp):
                                    for kk in range (0,r):
                                        a=my_array_p[k*r+kk,j*q+jj,i*p+ii]
                                        Kinv[i,j,k]+=1/float(micro_k[np.squeeze(np.where(phases==a))])/p/q/r

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
                   for i in range (0,nxp):
                       for ii in range (0,p):                       
                           for j in range (0,nyp):
                               for jj in range (0,q):
                                   for kk in range (0,r):
                                       a=my_array_p_z0[kk,j*q+jj,i*p+ii]
                                       Kinv_bz0[i,j]+=1/float(micro_k[np.squeeze(np.where(phases==a))])/p/q/r                     
                
                #proc j to j-1              
                if (ipy>0):
                   for i in range (0,nxp):
                       for ii in range (0,p):                       
                           for jj in range (0,q):
                               for k in range (0,nzp):
                                   for kk in range (0,r):
                                       a=my_array_p_y0[k*r+kk,jj,i*p+ii]
                                       Kinv_by0[i,k]+=1/float(micro_k[np.squeeze(np.where(phases==a))])/p/q/r

                #proc i to i-1              
                if (ipx>0):
                   for ii in range (0,p):
                       for j in range (0,nyp):
                           for jj in range (0,q):
                               for k in range (0,nzp):
                                   for kk in range (0,r):
                                       a=my_array_p_x0[k*r+kk,j*q+jj,ii]
                                       Kinv_bx0[j,k]+=1/float(micro_k[np.squeeze(np.where(phases==a))])/p/q/r
                
                #proc i to i+1              
                if (ipx<NPX-1):
                   for ii in range (0,p):
                       for j in range (0,nyp):
                           for jj in range (0,q):
                               for k in range (0,nzp):
                                   for kk in range (0,r):
                                       a=my_array_p_x1[k*r+kk,j*q+jj,ii]
                                       Kinv_bx1[j,k]+=1/float(micro_k[np.squeeze(np.where(phases==a))])/p/q/r                 

                #proc j to j+1              
                if (ipy<NPY-1):
                   for i in range (0,nxp):
                       for ii in range (0,p):                       
                           for jj in range (0,q):
                               for k in range (0,nzp):
                                   for kk in range (0,r):
                                       a=my_array_p_y1[k*r+kk,jj,i*p+ii]
                                       Kinv_by1[i,k]+=1/float(micro_k[np.squeeze(np.where(phases==a))])/p/q/r                      

                #proc k to k+1              
                if (ipz<NPZ-1):
                   for i in range (0,nxp):
                       for ii in range (0,p):                       
                           for j in range (0,nyp):
                               for jj in range (0,q):
                                   for kk in range (0,r):
                                       a=my_array_p_z1[kk,j*q+jj,i*p+ii]
                                       Kinv_bz1[i,j]+=1/float(micro_k[np.squeeze(np.where(phases==a))])/p/q/r                      
                
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
                f.write("dimensions      [0 0 0 0 0 0 0];"+'\n')
                f.write('\n')
                f.write("internalField   nonuniform List<scalar> "+'\n')
                f.write(str(ncells)+'\n')
                f.write("("+'\n')
                for k in range (0,nzp):
                    for j in range (0, nyp):
                        for i in range (0, nxp):
                            f.write(str(Kinv[i,j,k])+'\n')
                f.write(")"+'\n')
                f.write(";"+'\n')
                f.write(""+'\n')
                f.write("boundaryField"+'\n')
                f.write("{"+'\n')

                f.write("    inlet"+'\n')
                f.write("    {"+'\n')
                f.write("        type            zeroGradient;"+'\n')
                f.write("    }"+'\n')

                f.write("    outlet"+'\n')
                f.write("    {"+'\n')
                f.write("        type            zeroGradient;"+'\n')
                f.write("    }"+'\n')

                f.write("    \"wall_.*\""+'\n')
                f.write("    {"+'\n')
                f.write("        type            zeroGradient;"+'\n')
                f.write("    }"+'\n')


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
                            f.write(str(Kinv_bz0[i,j])+'\n')                        
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
                            f.write(str(Kinv_by0[i,k])+'\n')
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
                            f.write(str(Kinv_bx0[j,k])+'\n')
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
                            f.write(str(Kinv_bx1[j,k])+'\n')
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
                            f.write(str(Kinv_by1[i,k])+'\n')
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
                            f.write(str(Kinv_bz1[i,j])+'\n')
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



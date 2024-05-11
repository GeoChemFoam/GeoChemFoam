import numpy as np
import h5py
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
parser.add_argument('--nLevel', type=int, help='nLevel')
parser.add_argument('--refineStokes', type=int,help='refineStokes')
parser.add_argument('--res', type=float, help='resolution')
parser.add_argument('--Image_name', help='name of image')
parser.add_argument('--padWidth', type=int, help='pad Width')
parser.add_argument('--pores_value', type=int, help='value of pores')
parser.add_argument('--solid_value', type=float, help='value of solid phase')
parser.add_argument('--eps_min', type=float, help='minimum porosity')
parser.add_argument('--direction', type=int, help='flow in x y or z?')

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
nLevel=opt.nLevel
refineStokes=opt.refineStokes

res=opt.res
Image_name= opt.Image_name
padWidth=opt.padWidth
pores_value=opt.pores_value
solid_value=opt.solid_value
eps_min=opt.eps_min
direction=opt.direction

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
    
    #number of cells
    p=int((xMax-xMin)/nX)
    q=int((yMax-yMin)/nY)
    r=int((zMax-zMin)/nZ)

    nx1=int((xmax-xmin)/p)
    ny1=int((ymax-ymin)/q)
    nz1=int((zmax-zmin)/r)
    ncell = nx1*ny1*nz1


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
    
    #number of cells
    p=int((xMax-xMin)/nX)
    q=int((yMax-yMin)/nY)
    r=int((zMax-zMin)/nZ)

    nx1=int((xmax-xmin)/p)
    ny1=int((ymax-ymin)/q)
    nz1=int((zmax-zmin)/r)
    ncell = nx1*ny1*nz1 

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
    ncell = nx1*ny1*nz1 

print('calculate eps')
eps=np.zeros((nx1,ny1,nz1),dtype=float)
for i in range (0,nx1):
    for ii in range (0,p):
        for j in range (0,ny1):
            for jj in range (0,q):
                for k in range (0,nz1):
                    for kk in range (0,r):
                        eps[i,j,k]+=((my_array[k*r+kk,j*q+jj,i*p+ii]-solid_value)/(pores_value-solid_value)+ eps_min*(pores_value-my_array[k*r+kk,j*q+jj,i*p+ii])/(pores_value-solid_value))/p/q/r


print('create eps')
f=open('0/eps','a')
f.seek(0) #get to the first position
f.write("FoamFile"+'\n')
f.write("{"+'\n')
f.write("    version     2.0;"+'\n')
f.write("    format      ascii;"+'\n')
f.write("    class       volScalarField;"+'\n')
f.write("    object      eps;"+'\n')
f.write("}"+'\n')
f.write(""+'\n')
f.write("dimensions      [0 0 0 0 0 0 0];"+'\n')
f.write("internalField   nonuniform List<scalar>"+'\n')
f.write(str(ncell)+'\n')
f.write("("+'\n')
for k in range (0,nz1):
    for j in range (0, ny1):
        for i in range (0, nx1):
            f.write(str(eps[i,j,k])+'\n')
f.write(")"+'\n')
f.write(";"+'\n')
f.write(""+'\n')
f.write("boundaryField"+'\n')
f.write("{"+'\n')
f.write("    left"+'\n')
f.write("    {"+'\n')
f.write("        type cyclic;"+'\n')
f.write("    }"+'\n')
f.write("    right"+'\n')
f.write("    {"+'\n')
f.write("        type cyclic;"+'\n')
f.write("    }"+'\n')
f.write("    top"+'\n')
f.write("    {"+'\n')
f.write("        type cyclic;"+'\n')
f.write("    }"+'\n')
f.write("    bottom"+'\n')
f.write("    {"+'\n')
f.write("        type cyclic;"+'\n')
f.write("    }"+'\n')
f.write("    front"+'\n')
f.write("    {"+'\n')
f.write("        type cyclic;"+'\n')
f.write("    }"+'\n')
f.write("    back"+'\n')
f.write("    {"+'\n')
f.write("        type cyclic;"+'\n')
f.write("    }"+'\n')
f.write("}"+'\n')
f.close()

print('create blockMeshDict')

os.system('sed -i "s/nx/'+str(nx1)+'/g" system/blockMeshDict')
os.system('sed -i "s/ny/'+str(ny1)+'/g" system/blockMeshDict')
os.system('sed -i "s/nz/'+str(nz1)+'/g" system/blockMeshDict')

os.system('sed -i "s/res/'+str(res)+'/g" system/blockMeshDict')

os.system('sed -i "s/xMin/'+str(xmin)+'/g" system/blockMeshDict')
os.system('sed -i "s/yMin/'+str(ymin)+'/g" system/blockMeshDict')
os.system('sed -i "s/zMin/'+str(zmin)+'/g" system/blockMeshDict')
os.system('sed -i "s/xMax/'+str(xmax)+'/g" system/blockMeshDict')
os.system('sed -i "s/yMax/'+str(ymax)+'/g" system/blockMeshDict')
os.system('sed -i "s/zMax/'+str(zmax)+'/g" system/blockMeshDict')

os.system("blockMesh > blockMesh.out")

for i in range (0,nLevel):
    os.system('echo "refine mesh"')
    os.system('echo "smooth solid surface"')
    os.system('smoothSolidSurface > smoothSolidSurface.out')


    os.system('rm -f system/topoSetDict')
    f=open("system/topoSetDict",'a')
    f.seek(0) #get to the first position
    f.write("FoamFile"+'\n')
    f.write("{"+'\n')
    f.write("    version     2.0;"+'\n')
    f.write("    format      ascii;"+'\n')
    f.write("    class       dictionary;"+'\n')
    f.write("    object      topoSetDict;"+'\n')
    f.write("}"+'\n')
    f.write(""+'\n')
    f.write("actions"+'\n')
    f.write("("+'\n')
    f.write("{"+'\n')
    f.write("name refinementRegion;"+'\n')
    f.write("type cellSet;"+'\n')
    f.write("action new;"+'\n')
    f.write("source fieldToCell;"+'\n')
    f.write("field eps;"+'\n')
    f.write("min "+str(1e-3+eps_min)+";"+'\n')
    f.write("max "+str(1.0-(1-refineStokes)*1e-3)+";"+'\n')
    f.write("}"+'\n')  
    f.write(");")
    f.close()

    os.system('echo "topoSet and refineHexMesh"')
    os.system('topoSet > topoSet.out')
    os.system('refineHexMesh refinementRegion -overwrite > refineHexMesh.out')
                                
    os.system('echo "process mesh center"')
    os.system('processMeshCellCenters > processMeshCellCenter.out')

    nz1=2*nz1
    ny1=2*ny1
    nx1=2*nx1
    p=int((xmax-xmin)/nx1)
    q=int((ymax-ymin)/ny1)
    r=int((zmax-zmin)/nz1)
    os.system('echo "calculate eps for fine mesh"')
    eps=np.zeros((nx1,ny1,nz1),dtype=float)
    for i in range (0,nx1):
        for ii in range (0,p):
            for j in range (0,ny1):
                for jj in range (0,q):
                    for k in range (0,nz1):
                        for kk in range (0,r):
                            eps[i,j,k]+=((my_array[k*r+kk,j*q+jj,i*p+ii]-solid_value)/(pores_value-solid_value)+ eps_min*(pores_value-my_array[k*r+kk,j*q+jj,i*p+ii])/(pores_value-solid_value))/p/q/r

    dx = res*(xmax-xmin)/nx1
    dy = res*(ymax-ymin)/ny1
    dz = res*(zmax-zmin)/nz1
    
    ix = np.zeros(nx1*ny1*nz1)
    iy = np.zeros(nx1*ny1*nz1)
    iz = np.zeros(nx1*ny1*nz1)

    file = open("0/cellCenters","r")
    Lines = file.readlines()
    count =0
    wbool=0
    for line in Lines:
      ls = line.strip()
      if (ls==")"):
          break
      if (wbool==1):
          x=float(ls.split("(")[1].split(")")[0].split()[0])
          ix[count] = np.floor((x-res*xmin)/dx);
          y=float(ls.split("(")[1].split(")")[0].split()[1])
          iy[count] = np.floor((y-res*ymin)/dy);
          z=float(ls.split("(")[1].split(")")[0].split()[2])
          iz[count] = np.floor((z-res*zmin)/dz);
          count +=1
      if (ls=="("):
          wbool=1

    ncell = count

    newEps = np.zeros(ncell)

    os.system('echo "modify eps according to finer mesh for cells at interface using cell center"')

    file = open("0/eps","r")
    Lines = file.readlines()
    count=0
    wbool=0
    for line in Lines:
      ls = line.strip()
      if (ls==")"):
          break
      if (wbool==1):
          epsVal=float(ls)
          if (epsVal<1) and (epsVal>eps_min):
            newEps[count] = eps[ix[count].astype(int),iy[count].astype(int),iz[count].astype(int)]
          else:
            newEps[count] = epsVal
          count +=1
      if (ls=="("):
          wbool=1

    os.system('rm -f 0/eps')
    os.system('rm -f 0/Kinv')
    f=open('0/eps','a')
    f.seek(0) #get to the first position
    f.write("FoamFile"+'\n')
    f.write("{"+'\n')
    f.write("    version     2.0;"+'\n')
    f.write("    format      ascii;"+'\n')
    f.write("    class       volScalarField;"+'\n')
    f.write("    object      eps;"+'\n')
    f.write("}"+'\n')
    f.write(""+'\n')
    f.write("dimensions      [0 0 0 0 0 0 0];"+'\n')
    f.write("internalField   nonuniform List<scalar>"+'\n')
    f.write(str(ncell)+'\n')
    f.write("("+'\n')

    for k in range(0,ncell):
            f.write(str(newEps[k])+'\n')
    f.write(")"+'\n')
    f.write(";"+'\n')
    f.write(""+'\n')
    f.write("boundaryField"+'\n')
    f.write("{"+'\n')
    f.write("    left"+'\n')
    f.write("    {"+'\n')
    f.write("        type cyclic;"+'\n')
    f.write("    }"+'\n')
    f.write("    right"+'\n')
    f.write("    {"+'\n')
    f.write("        type cyclic;"+'\n')
    f.write("    }"+'\n')
    f.write("    top"+'\n')
    f.write("    {"+'\n')
    f.write("        type cyclic;"+'\n')
    f.write("    }"+'\n')
    f.write("    bottom"+'\n')
    f.write("    {"+'\n')
    f.write("        type cyclic;"+'\n')
    f.write("    }"+'\n')
    f.write("    front"+'\n')
    f.write("    {"+'\n')
    f.write("        type cyclic;"+'\n')
    f.write("    }"+'\n')
    f.write("    back"+'\n')
    f.write("    {"+'\n')
    f.write("        type cyclic;"+'\n')
    f.write("    }"+'\n')
    f.write("}"+'\n')
    f.close()

    os.system('rm -f 0/cellCenters')


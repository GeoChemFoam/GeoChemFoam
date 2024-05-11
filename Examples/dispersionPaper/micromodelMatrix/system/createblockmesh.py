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
img = np.reshape(img,(yDim,xDim))
img_crop = img[yMin:yMax,xMin:xMax]
my_array = np.pad(img_crop,pad_width=padWidth,mode='constant',constant_values=pores_value)

if direction==0:

    #crop image to remove unecessary pad
    my_array = my_array[padWidth:padWidth+yMax-yMin,0:2*padWidth+xMax-xMin]

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

    nx1=int((xmax-xmin)/p)
    ny1=int((ymax-ymin)/q)
    ncell = nx1*ny1

else:

    #crop image to remove unecessary pad
    my_array = my_array[0:2*padWidth+yMax-yMin,padWidth:padWidth+xMax-xMin]
    
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

    nx1=int((xmax-xmin)/p)
    ny1=int((ymax-ymin)/q)
    ncell = nx1*ny1 

print('calculate eps')
eps=np.zeros((nx1,ny1),dtype=float)
for i in range (0,nx1):
    for ii in range (0,p):
        for j in range (0,ny1):
            for jj in range (0,q):
                eps[i,j]+=((my_array[j*q+jj,i*p+ii]-solid_value)/(pores_value-solid_value)+ eps_min*(pores_value-my_array[j*q+jj,i*p+ii])/(pores_value-solid_value))/p/q

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
for j in range (0, ny1):
    for i in range (0, nx1):
        f.write(str(eps[i,j])+'\n')
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
f.write("    frontandback"+'\n')
f.write("    {"+'\n')
f.write("        type empty;"+'\n')
f.write("    }"+'\n')
f.write("}"+'\n')
f.close()

print('create blockMeshDict')

os.system('sed -i "s/nx/'+str(nx1)+'/g" system/blockMeshDict')
os.system('sed -i "s/ny/'+str(ny1)+'/g" system/blockMeshDict')

os.system('sed -i "s/res/'+str(res)+'/g" system/blockMeshDict')

os.system('sed -i "s/x_min/'+str(xmin)+'/g" system/blockMeshDict')
os.system('sed -i "s/y_min/'+str(ymin)+'/g" system/blockMeshDict')
os.system('sed -i "s/z_min/'+str(zmin)+'/g" system/blockMeshDict')
os.system('sed -i "s/x_max/'+str(xmax)+'/g" system/blockMeshDict')
os.system('sed -i "s/y_max/'+str(ymax)+'/g" system/blockMeshDict')
os.system('sed -i "s/z_max/'+str(zmax)+'/g" system/blockMeshDict')

os.system("blockMesh > blockMesh.out")

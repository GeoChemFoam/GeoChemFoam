from mpi4py import MPI
import subprocess
import numpy as np
import array
import argparse

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

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
parser.add_argument('--refineStokes', type=int, help='refineStokes')
parser.add_argument('--res', type=float, help='resolution')
parser.add_argument('--Image_name', help='name of image')
parser.add_argument('--padWidth', type=int, help='pad Width')
parser.add_argument('--pores_value', type=int, help='value of pores')
parser.add_argument('--solid_value', type=float, help='value of solid phase')
parser.add_argument('--direction', type=int, help='flow in x y or z?')
parser.add_argument('--micro_por', nargs='+')
parser.add_argument('--micro_k', nargs='+')
parser.add_argument('--phases', nargs='+', type=int)

opt = parser.parse_args()

x_dim=opt.xDim
y_dim=opt.yDim
z_dim=opt.zDim

x_min=opt.xMin
x_max=opt.xMax
y_min=opt.yMin
y_max=opt.yMax
z_min=opt.zMin
z_max=opt.zMax

n_x=opt.nX
n_y=opt.nY
n_z=opt.nZ

nlevel = opt.nLevel
refineStokes=opt.refineStokes
res = opt.res

Image_name= opt.Image_name
padWidth=opt.padWidth
pores_value=opt.pores_value
solid_value=opt.solid_value
direction=opt.direction

micro_por=opt.micro_por
micro_k=opt.micro_k
phases=opt.phases

if rank == 0:
    print(f"create cells\n")

subprocess.run(['python', 'system/createblockmeshpar.py',
                   '--xDim', str(x_dim), 
                   '--yDim', str(y_dim),
                   '--zDim', str(z_dim),
                   '--xMin', str(x_min),
                   '--xMax', str(x_max),
                   '--yMin', str(y_min),
                   '--yMax', str(y_max),
                   '--zMin', str(z_min),
                   '--zMax', str(z_max),
                   '--nX', str(n_x),
                   '--nY', str(n_y),
                   '--nZ', str(n_z),
                   '--nLevel', str(nlevel), 
                   '--refineStokes', str(refineStokes),
                   '--res', str(res), 
                   '--Image_name', str(Image_name), 
                   '--padWidth', str(padWidth), 
                   '--pores_value', str(pores_value),
                   '--solid_value', str(solid_value), 
                   '--direction', str(direction),
                   '--micro_por'] + [str(floats) for floats in micro_por] +
                   ['--micro_k']  + [str(floats) for floats in micro_k] +
                   ['--phases'] + [str(integers) for integers in phases] +
                   ['--rank', str(rank)])

MPI.Finalize()



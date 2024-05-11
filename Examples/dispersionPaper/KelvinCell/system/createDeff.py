import numpy as np
import h5py
import array
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--Diff', type=float, help='molecular diffusion')
parser.add_argument('--eps0', type=float, help='porosity of microporous phase')
parser.add_argument('--tau', type=float, help='tortuosity of microporous phase')
parser.add_argument('--Lpore', type=float, help='reference pore size in microporous phase')
parser.add_argument('--beta1', type=float, help='dispersion constant beta1')
parser.add_argument('--alpha1', type=float, help='dispersion constant alpha1')
parser.add_argument('--alpha2', type=float, help='dispersion constant alpha2')
parser.add_argument('--beta2', type=float, help='dispersion constant beta2')
parser.add_argument('--gamma1', type=float, help='dispersion constant gamma1')
parser.add_argument('--gamma2', type=float, help='dispersion constant gamma2')



opt = parser.parse_args()

Diff=opt.Diff
eps0=opt.eps0
tau=opt.tau
Lpore=opt.Lpore
beta1=opt.beta1
alpha1=opt.alpha1
alpha2=opt.alpha2
beta2=opt.beta2
gamma1=opt.gamma1
gamma2=opt.gamma2


file = open("0/eps","r")
Lines = file.readlines()
count=0
wbool=0
for line in Lines:
  ls = line.strip()
  if (ls==")"):
      break
  if (wbool==1):
      count +=1
  if (ls=="("):
      wbool=1
ncell=count
file.close()

eps = np.zeros(ncell)
file = open("0/eps","r")
Lines = file.readlines()
count=0
wbool=0
for line in Lines:
  ls = line.strip()
  if (ls==")"):
      break
  if (wbool==1):
      eps[count]=float(ls)
      count +=1
  if (ls=="("):
      wbool=1
file.close()

Ux = np.zeros(ncell)
Uy = np.zeros(ncell)
Uz = np.zeros(ncell)
file = open("0/U","r")
Lines = file.readlines()
count=0
wbool=0
for line in Lines:
  ls = line.strip()
  if (ls==")"):
      break
  if (wbool==1):
      Ux[count]=float(ls.split("(")[1].split(")")[0].split()[0])
      Uy[count]=float(ls.split("(")[1].split(")")[0].split()[1])
      Uz[count]=float(ls.split("(")[1].split(")")[0].split()[2])
      count +=1
  if (ls=="("):
      wbool=1
file.close()


Dx = np.zeros(ncell)
Dy = np.zeros(ncell)
Dz = np.zeros(ncell)
for k in range(0,ncell):
  epsVal=eps[k]
  p=(tau-1)/(1-eps0)
  tinv=1.0/(1.0+p*(1-epsVal))
  magU=np.sqrt(Ux[k]*Ux[k]+Uy[k]*Uy[k])
  Pe=magU/epsVal*Lpore/Diff
  if (Pe<1):
      Dx[k] = Diff*tinv*(1+beta1*(1-epsVal)/(1-eps0)*pow(Pe,alpha1))
      Dy[k] = Diff*tinv*(1+beta2*(1-epsVal)/(1-eps0)*pow(Pe,gamma1))
      Dz[k] = Diff*tinv*(1+beta2*(1-epsVal)/(1-eps0)*pow(Pe,gamma1))
  else:
      Dx[k] = Diff*tinv*(1+beta1*(1-epsVal)/(1-eps0)*pow(Pe,alpha2))
      Dy[k] = Diff*tinv*(1+beta2*(1-epsVal)/(1-eps0)*pow(Pe,gamma2))
      Dz[k] = Diff*tinv*(1+beta2*(1-epsVal)/(1-eps0)*pow(Pe,gamma2))

f=open('0/D','a')
f.seek(0) #get to the first position
f.write("FoamFile"+'\n')
f.write("{"+'\n')
f.write("    version     2.0;"+'\n')
f.write("    format      ascii;"+'\n')
f.write("    class       volTensorField;"+'\n')
f.write("    object      D;"+'\n')
f.write("}"+'\n')
f.write(""+'\n')
f.write("dimensions      [0 2 -1 0 0 0 0];"+'\n')
f.write("internalField   nonuniform List<tensor>"+'\n')
f.write(str(ncell)+'\n')
f.write("("+'\n')
for k in range(0,ncell):
        f.write('('+str(Dx[k])+' 0 0 0 '+str(Dy[k])+' 0 0 0 '+str(Dz[k])+')'+'\n')
f.write(")"+'\n')
f.write(";"+'\n')
f.write(""+'\n')
f.write("boundaryField"+'\n')
f.write("{"+'\n')
f.write("    top"+'\n')
f.write("    {"+'\n')
f.write("        type cyclic;"+'\n')
f.write("    }"+'\n')
f.write("    bottom"+'\n')
f.write("    {"+'\n')
f.write("        type cyclic;"+'\n')
f.write("    }"+'\n')
f.write("    left"+'\n')
f.write("    {"+'\n')
f.write("        type cyclic;"+'\n')
f.write("    }"+'\n')
f.write("    right"+'\n')
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


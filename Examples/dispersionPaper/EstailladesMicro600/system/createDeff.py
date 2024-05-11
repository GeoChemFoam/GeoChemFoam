import numpy as np
import h5py
import array
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--Diff', type=float, help='molecular diffusion')
parser.add_argument('--micro_por', nargs='+')
parser.add_argument('--micro_tau', nargs='+')
parser.add_argument('--micro_Lpore', nargs='+')
parser.add_argument('--micro_betax', nargs='+')
parser.add_argument('--micro_alpha1x', nargs='+')
parser.add_argument('--micro_alpha2x', nargs='+')
parser.add_argument('--micro_betay', nargs='+')
parser.add_argument('--micro_alpha1y', nargs='+')
parser.add_argument('--micro_alpha2y', nargs='+')
parser.add_argument('--micro_betaz', nargs='+')
parser.add_argument('--micro_alpha1z', nargs='+')
parser.add_argument('--micro_alpha2z', nargs='+')



opt = parser.parse_args()

Diff=opt.Diff
micro_Lpore=opt.micro_Lpore
micro_por=opt.micro_por
micro_tau=opt.micro_tau
micro_betax=opt.micro_betax
micro_alpha1x=opt.micro_alpha1x
micro_alpha2x=opt.micro_alpha2x
micro_betay=opt.micro_betay
micro_alpha1y=opt.micro_alpha1y
micro_alpha2y=opt.micro_alpha2y
micro_betaz=opt.micro_betaz
micro_alpha1z=opt.micro_alpha1z
micro_alpha2z=opt.micro_alpha2z

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
micro_size=len(micro_por)
for k in range(0,ncell):
  epsVal=eps[k]
  for i in range(0,micro_size):
      poro=float(micro_por[i])
      if (np.abs(epsVal-poro)<1e-4):
          tau=float(micro_tau[i])
          alpha1x=float(micro_alpha1x[i])
          alpha2x=float(micro_alpha2x[i])
          alpha1y=float(micro_alpha1y[i])
          alpha2y=float(micro_alpha2y[i])
          alpha1z=float(micro_alpha1z[i])
          alpha2z=float(micro_alpha2z[i])
          betax=float(micro_betax[i])
          betay=float(micro_betay[i])
          betaz=float(micro_betaz[i])
          Lpore=float(micro_Lpore[i])
          Pe=np.abs(Uy[k])/epsVal*Lpore/Diff
          if (Pe<1):
              Dx[k] = Diff/tau*(1+betax*pow(Pe,alpha1x))
              Dy[k] = Diff/tau*(1+betay*pow(Pe,alpha1y))
              Dz[k] = Diff/tau*(1+betaz*pow(Pe,alpha1z))
          else:
              Dx[k] = Diff/tau*(1+betax*pow(Pe,alpha2x))
              Dy[k] = Diff/tau*(1+betay*pow(Pe,alpha2y))
              Dz[k] = Diff/tau*(1+betaz*pow(Pe,alpha2z))
          break


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


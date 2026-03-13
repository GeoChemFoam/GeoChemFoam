import numpy as np
import array
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--NPX', type=int, help='NPX')
parser.add_argument('--NPY', type=int, help='NPY')
parser.add_argument('--NPZ', type=int, help='NPZ')
parser.add_argument('--PDROP',type=float,help='PDROP')

opt = parser.parse_args()

NPX=opt.NPX
NPY=opt.NPY
NPZ=opt.NPZ

PDROP=opt.PDROP

if (NPX*NPY*NPZ>1):
    for ipz in range(0,NPZ):
        for ipy in range(0,NPY):
            for ipx in range(0,NPX):
                iproc=ipz*NPX*NPY+ipy*NPX+ipx
                
                ###################################################################
                ###### p ##########################################################
                ###################################################################
 
                
                f=open('processor'+str(iproc)+'/0/p','a')
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
                f.write("    object      p;"+'\n')
                f.write("}"+'\n')
                f.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //"+'\n')
                f.write(""+'\n')
                f.write("dimensions      [0 2 -2 0 0 0 0];"+'\n')
                f.write('\n')
                f.write("internalField   uniform 0;"+'\n')
                f.write('\n')
                f.write("boundaryField"+'\n')
                f.write("{"+'\n')
                f.write("    solidwalls"+'\n')
                f.write("    {"+'\n')
                f.write("        type            zeroGradient;"+'\n')
                f.write("    }"+'\n')
                f.write("    inlet"+'\n')
                f.write("    {"+'\n')
                f.write("        type            fixedValue;"+'\n')
                f.write("        value           uniform "+str(PDROP)+";"+'\n')
                f.write("    }"+'\n')
                f.write("    outlet"+'\n')
                f.write("    {"+'\n')
                f.write("        type            fixedValue;"+'\n')
                f.write("        value           uniform 0;"+'\n')
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
                    f.write("        value           uniform 0;"+'\n')
                    f.write("    }"+'\n')
                    
                ##proc j to j-1                
                if (ipy>0):
                    f.write("    procBoundary"+str(iproc)+"to"+str(iproc-NPX)+'\n')
                    f.write("    {"+'\n')
                    f.write("        type            processor;"+'\n')                    
                    f.write("        value           uniform 0;"+'\n')
                    f.write("    }"+'\n')
                    
                ##proc i to i-1                
                if (ipx>0):
                    f.write("    procBoundary"+str(iproc)+"to"+str(iproc-1)+'\n')
                    f.write("    {"+'\n')
                    f.write("        type            processor;"+'\n')                    
                    f.write("        value           uniform 0;"+'\n')          
                    f.write("    }"+'\n')
                    
                ##proc i to i+1                
                if (ipx<NPX-1):
                    f.write("    procBoundary"+str(iproc)+"to"+str(iproc+1)+'\n')
                    f.write("    {"+'\n')
                    f.write("        type            processor;"+'\n')                    
                    f.write("        value           uniform 0;"+'\n')            
                    f.write("    }"+'\n')

                ##proc j to j+1                
                if (ipy<NPY-1):
                    f.write("    procBoundary"+str(iproc)+"to"+str(iproc+NPX)+'\n')
                    f.write("    {"+'\n')
                    f.write("        type            processor;"+'\n')                    
                    f.write("        value           uniform 0;"+'\n')
                    f.write("    }"+'\n')

                ##proc k to k+1                
                if (ipz<NPZ-1):
                    f.write("    procBoundary"+str(iproc)+"to"+str(iproc+NPX*NPY)+'\n')
                    f.write("    {"+'\n')
                    f.write("        type            processor;"+'\n')                    
                    f.write("        value           uniform 0;"+'\n')
                    f.write("    }"+'\n')


                f.write("}"+'\n')
                ##So that the files are exactly the same than with blockMesh - remove later                
                f.write('\n')
                f.write('\n')                
                f.write("// ************************************************************************* //")

                f.close()              

else:

    ###################################################################
    ###### p ##########################################################
    ###################################################################

    f=open('0/p','a')
    f.seek(0) #get to the first position
    f.write("FoamFile"+'\n')
    f.write("{"+'\n')
    f.write("    version     2.0;"+'\n')
    f.write("    format      ascii;"+'\n')
    f.write("    class       volVectorField;"+'\n')
    f.write("    object      U;"+'\n')
    f.write("}"+'\n')
    f.write(""+'\n')
    f.write("dimensions      [0 2 -2 0 0 0 0];"+'\n')
    f.write("internalField   uniform 0;"+'\n')
    f.write('\n')
    f.write("boundaryField"+'\n')
    f.write("{"+'\n')
    f.write("    inlet"+'\n')
    f.write("    {"+'\n')
    f.write("        type zeroGradient;"+'\n')
    f.write("    }"+'\n')
    f.write("    outlet"+'\n')
    f.write("    {"+'\n')
    f.write("        type            fixedValue;"+'\n')
    f.write("        value           uniform 0;"+'\n')
    f.write("    }"+'\n')
    f.write("    \"wall_.*\""+'\n')
    f.write("    {"+'\n')
    f.write("        type zeroGradient;"+'\n')
    f.write("    }"+'\n')
    f.write("}"+'\n')
    f.close()


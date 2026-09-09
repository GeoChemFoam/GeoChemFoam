# Reproducing the DBS1 and DBS2 Simulations

## Overview

The simulations provided in this repository compare two Darcy–Brinkman–Stokes formulations, referred to as **DBS1** and **DBS2** in the accompanying paper.

The principal difference between the two formulations is the discretisation of the momentum equation contained in the `UEqn.H` file of the `simpleDBSFoam` solver.

* **DBS2** is the formulation implemented in the current version of `simpleDBSFoam` in GeoChemFoam.
* **DBS1** is the alternative formulation used for comparison in the paper.

The DBS1 momentum-equation file is provided in the folder named `UEqnForDBS1`.

## Running the DBS2 Simulations

DBS2 is the default formulation supplied with the current version of GeoChemFoam. Therefore, no modification to `simpleDBSFoam` is required.

After installing and compiling GeoChemFoam according to its standard installation instructions, the supplied simulation cases can be run directly using `simpleDBSFoam`.

## Running the DBS1 Simulations

No separate DBS1 solver is provided. Instead, DBS1 is reproduced by modifying the momentum equation in the existing `simpleDBSFoam` solver.

The following procedure should be used:

1. Locate the source-code folder for `simpleDBSFoam` in the GeoChemFoam installation.

2. Identify the existing `UEqn.H` file in that folder. This file contains the default DBS2 formulation.

3. Make a backup copy of the existing `UEqn.H` file so that the DBS2 formulation can be restored later.

4. Open the `UEqnForDBS1` folder supplied with these simulation files.

5. Copy the `UEqn.H` file from `UEqnForDBS1` into the `simpleDBSFoam` source-code folder, replacing the existing `UEqn.H` file.

6. Recompile `simpleDBSFoam` using the standard GeoChemFoam compilation procedure.

7. Run the supplied simulation cases using the recompiled `simpleDBSFoam` solver.

The executable name remains `simpleDBSFoam` after recompilation. Therefore, the commands and case settings used to run the simulations do not need to be changed.

Alternatively, rather than copying the supplied file, the existing `UEqn.H` file may be edited manually so that its contents match the version provided in `UEqnForDBS1`. The solver must still be recompiled before running the DBS1 simulations.

## Switching Back to DBS2

To return to the DBS2 formulation:

1. Restore the original `UEqn.H` file that was backed up before installing the DBS1 version.
2. Recompile `simpleDBSFoam`.
3. Run the cases again using the restored solver.

## Case Prerequisites and Commands

The following commands assume that the current directory is `Examples/ConservativeDBSPaper` in a fresh GeoChemFoam checkout.

Before running the cases:

- install and compile GeoChemFoam and load its OpenFOAM environment;
- ensure that `simpleDBSFoam`, `simpleGCFoam`, `processPoroPerm`, MPI, and the standard OpenFOAM utilities are available;
- ensure that Python, NumPy, h5py, and `bc` are available; and
- request at least the number of MPI processes listed below.

The image-based cases obtain their input automatically from the `raw_images` directory. It must contain:

- `Bentheimer400-5mum_binarized.raw.tar.gz`
- `micromodel_1200by1200_heteroSquares.raw.tar.gz`

No external image-path environment variable is required.

| Simulation | Case directory | Command | MPI processes |
|---|---|---|---:|
| DBS1 or DBS2 | `DBS/Bentheimer_400cube` | `(cd DBS/Bentheimer_400cube && ./Allrun.sh)` | 64 |
| DBS1 or DBS2 | `DBS/micromodel_1200by1200_heteroSquares` | `(cd DBS/micromodel_1200by1200_heteroSquares && ./Allrun.sh)` | 32 |
| DBS1 or DBS2 | `DBS/microChannel_500_150_1` | `(cd DBS/microChannel_500_150_1 && ./runCaseFlow.sh)` | 16 |
| DNS | `DNS/Bentheimer_400cube` | `(cd DNS/Bentheimer_400cube && ./Allrun.sh)` | 64 |
| DNS | `DNS/micromodel_1200by1200_heteroSquares` | `(cd DNS/micromodel_1200by1200_heteroSquares && ./Allrun.sh)` | 32 |
| DNS | `DNS/microChannel_500_150_1` | `(cd DNS/microChannel_500_150_1 && ./runCaseFlow.sh)` | 16 |

For the image-based cases, `Allrun.sh` creates the mesh, initializes the fields, runs the flow solver, and performs post-processing. For the microchannel cases, `runCaseFlow.sh` performs the complete workflow.

The DBS commands use whichever version of `simpleDBSFoam` was most recently compiled: the default DBS2 formulation or the DBS1 formulation described above. The DNS commands use `simpleGCFoam`.

## Important Note

The compiled `simpleDBSFoam` executable will use whichever version of `UEqn.H` was present during the most recent compilation. Users should therefore confirm that the intended formulation has been installed and compiled before running each group of simulations.

To avoid mixing results from the two formulations, outputs generated using DBS1 and DBS2 should be stored in clearly labelled, separate directories.

#!/bin/bash
set -e

# blockMesh
cd "${0%/*}" || exit 1

# Source tutorial run functions
. "$WM_PROJECT_DIR/bin/tools/RunFunctions"

runApplication blockMesh

./initCaseFlow.sh

#runApplication setFields

runApplication decomposePar

runParallel simpleGCFoam

runApplication reconstructPar -withZero

rm -rf processor*

./processFlow.sh



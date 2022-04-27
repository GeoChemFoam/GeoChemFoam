## Hi there 👋, Welcome to the GeoChemFoam github! Here you will find links to the [source code](https://github.com/GeoChemFoam/GeoChemFoam-4.6/blob/main/doc/GeoChemFoam-User-Guide.pdf), [precompiled dockers](https://hub.docker.com/r/jcmaes/geochemfoam-4.6), jupyter notebook and video tutorials, [a users wiki](https://github.com/GeoChemFoam/GeoChemFoam/wiki), [publications](https://github.com/GeoChemFoam/GeoChemFoam/tree/main/GeoChemFoam_Papers), a [discussion forum](https://github.com/GeoChemFoam/GeoChemFoam/discussions) and more!

### The GeoChemFoam source code is hosted here on [github](https://github.com/GeoChemFoam/GeoChemFoam-4.6/blob/main/doc/GeoChemFoam-User-Guide.pdf). A precompiled docker of the latest version is also available on the [docker hub](https://hub.docker.com/r/jcmaes/geochemfoam-4.6).

GeochemFoam is the world most advanced open source pore-scale numerical simulator based on OpenFOAM developed at the Institute for GeoEnergy Engineering at Heriot-Watt University. GeoChemFoam is made specifically for researching pore-scale processes related to the energy transition. Below is a list of current capabilities, but __we are always adding new stuff and we welcome contributions from the community.__ Drop us a line at j.maes@hw.ac.uk or h.menke@hw.ac.uk.

#### __Current capabilities:__
- Multiphase Reactive Transport (e.g. [scCO2 dissolving in brine](https://arxiv.org/pdf/2103.03579.pdf))

<img src="https://github.com/GeoChemFoam/GeoChemFoam/blob/main/wikiImages/multiphaseReactive.gif" width="300"> <img src="https://github.com/GeoChemFoam/GeoChemFoam/blob/main/wikiImages/CavityDissolution.gif" width="400">

- Improved Multiphase solver (e.g. [benchmarking viscous fingering in a micromodel](https://github.com/GeoChemFoam/GeoChemFoam/blob/main/GeoChemFoam_Papers/Zhaoetal2019_PoreScaleModels_PNAS.pdf))

<img src="https://github.com/GeoChemFoam/GeoChemFoam/blob/main/wikiImages/multiphaseFlow.gif" width="200">

- Two-phase flow at low capillary number (Ca=10<sup>-7</sup>) (e.g. [drainage & imbibition of oil in brine](https://arxiv.org/abs/2105.10576))

<img src="https://github.com/GeoChemFoam/GeoChemFoam/blob/main/wikiImages/multiphaseFlowLowCa.gif" width="200"> 

- Conjugate Heat Transfer (e.g. [cold water injection into hot porous media](https://arxiv.org/abs/2110.03311))

<img src="https://github.com/GeoChemFoam/GeoChemFoam/blob/main/wikiImages/spherePacking.gif" width="250">

- Reactive Dissolution (e.g. [acid-well stimulation](https://www.earthdoc.org/content/papers/10.3997/2214-4609.202035250))

<img src="https://github.com/GeoChemFoam/GeoChemFoam/blob/main/wikiImages/HM120_60_120Pe100_K10AnimatedSlices.gif" width="200"> <img src="https://github.com/GeoChemFoam/GeoChemFoam/blob/main/wikiImages/HM120_60_120Pe1_K0.1AnimatedSlices.gif" width="200"> 

- Contaminant transport (e.g. [plume migration](https://arxiv.org/abs/2103.03597))

<img src="https://github.com/GeoChemFoam/GeoChemFoam/blob/main/wikiImages/ns_het.gif" width="300"> 

- Multi-species molecular reaction 
 
<img src="https://github.com/GeoChemFoam/GeoChemFoam/blob/main/wikiImages/singlePhaseBimolecularReaction.gif" width="400">

- Darcy-Stokes-Brinkman (e.g. [permeability upscaling](https://www.nature.com/articles/s41598-021-82029-2))

<img src="https://github.com/GeoChemFoam/GeoChemFoam/blob/main/wikiImages/EstailladesStreamlineNewPNGGIF.gif" width="400"> 

#### __Currently in development:__
- Charge Balance for fuel cells and electrolyzers
- On-demand machine learning for reaction with [Reaktoro](https://reaktoro.org)

#### __We are looking to collaborate on:__
- Particle nucleation and precipitation
- Bubble nucleation
- Phase transition
- Wettability alteration
- Machine learning acceleration
- Biological clogging



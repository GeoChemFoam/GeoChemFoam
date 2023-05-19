## Hi there 👋, welcome to The GeoChemFoam Project github! Here you will find links to the [source code](https://github.com/GeoChemFoam/GeoChemFoam-5.0), [precompiled dockers](https://hub.docker.com/r/jcmaes), [a users wiki](https://github.com/GeoChemFoam/GeoChemFoam/wiki), [publications](https://github.com/GeoChemFoam/GeoChemFoam/tree/main/GeoChemFoam_Papers), a [discussion forum](https://github.com/GeoChemFoam/GeoChemFoam/discussions) and more!

### The GeoChemFoam Project source code is hosted here on [github](https://github.com/GeoChemFoam/GeoChemFoam-5.0). A precompiled docker of the latest version is also available on the [docker hub](https://hub.docker.com/r/jcmaes/geochemfoam-5.0).

The GeochemFoam Project is the world's most advanced open source pore-scale numerical simulator based on OpenFOAM founded at the Institute of GeoEnergy Engineering at Heriot-Watt University in 2019 by [__Dr Julien Maes__](www.julienmaes.com) and [__Dr Hannah Menke__](https://scholar.google.co.uk/citations?user=tVSGe5IAAAAJ&hl=en). GeoChemFoam is made specifically for researching pore-scale processes related to the energy transition and our NetZero carbon future. Below is a list of current capabilities, but __we are always adding new stuff and we welcome contributions from the community.__ Drop us a line at GeoChemFoam@hw.ac.uk.
#### __Project Partners:__
__Dr Shaina Kelly__ ([Kelly Lab, Columbia University](https://kellylab.engineering.columbia.edu/))


#### __Current capabilities:__
- Multiphase Reactive Transport (e.g. [scCO2 dissolving in brine](https://arxiv.org/pdf/2103.03579.pdf))

<img src="https://github.com/GeoChemFoam/GeoChemFoam/blob/main/wikiImages/multiphaseReactive.gif" width="300"> <img src="https://github.com/GeoChemFoam/GeoChemFoam/blob/main/wikiImages/CavityDissolution.gif" width="400">

- Improved Multiphase solver (e.g. [benchmarking viscous fingering in a micromodel](https://github.com/GeoChemFoam/GeoChemFoam/blob/main/GeoChemFoam_Papers/Zhaoetal2019_PoreScaleModels_PNAS.pdf))

<img src="https://github.com/GeoChemFoam/GeoChemFoam/blob/main/wikiImages/multiphaseFlow.gif" width="200">

- Two-phase flow at low capillary number (Ca=10<sup>-7</sup>) (e.g. [drainage & imbibition of oil in brine](https://arxiv.org/abs/2105.10576))

<img src="https://github.com/GeoChemFoam/GeoChemFoam/blob/main/wikiImages/multiphaseFlowLowCa.gif" width="200"> 

- Conjugate Heat Transfer (e.g. [cold water injection into hot porous media](https://arxiv.org/abs/2110.03311))

<img src="https://github.com/GeoChemFoam/GeoChemFoam/blob/main/wikiImages/BentheimerT.gif" width="250">

- Improved Reactive Dissolution solver (e.g. [acid-well stimulation](https://www.earthdoc.org/content/papers/10.3997/2214-4609.202035250) and [CCS](https://arxiv.org/abs/2204.07019))

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
- Singularity
- Machine learning acceleration

#### __We are looking to collaborate on:__
- Particle nucleation and precipitation
- Bubble nucleation
- Phase transition
- Wettability alteration
- Biological clogging



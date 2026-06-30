# User Questionnaire

Ask these before final deck generation.

## Common

- Device name and type
- Route: DevEdit + ATLAS, ATHENA + ATLAS, or ATLAS direct control baseline
- Simulation target: electrical, optical, optoelectronic, process, or mixed
- Required outputs and curves
- Units and coordinate convention
- Whether all recommended parameters are confirmed by the user

## PN / PIN diode

- Geometry dimensions and layer/region boundaries
- Material for every region
- P/N/I doping species, concentration, and extent
- Contact names and locations
- Ohmic or Schottky contact assumptions
- Mesh refinement near junctions and contacts
- ATLAS models, method, solve init, sweep electrode, bias range, step, log, and save files

## Schottky

- Metal work function
- Semiconductor doping and interface area
- Barrier target or extraction target
- Interface charge or traps if needed

## MOS

- Gate oxide thickness and dielectric
- Gate material/workfunction
- Substrate/body doping
- Source/drain geometry and doping
- Gate bias and drain bias sweeps

## SiGe PD / waveguide PD

- Si/Ge/SiGe layer stack and dimensions
- Ge fraction and material parameter source
- Optical wavelength, optical source type, incident direction, power, beam width, and angle
- Electrical bias sweep
- Target outputs: photocurrent, responsivity, QE, absorption, optical generation
- Whether Luminous is required

## ATHENA process

- Substrate material, orientation, and initial doping
- Mesh line x/y
- Oxidation, deposition, etch, lithography/mask, implant, diffuse/anneal steps
- Implant species, dose, energy, tilt/rotation
- Electrode definitions and final structure file name

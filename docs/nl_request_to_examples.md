# Natural Language Request to Example Mapping

Use `scripts/search_silvaco_examples.py` before recommending syntax or models.

## PN diode I-V

Search tags: `pn_diode,iv,atlas,devedit_atlas_flow`.
Recommend checking examples with `go atlas`, `models`, `solve`, `log`, and DevEdit/ATLAS flow when the user wants a full structure-to-simulation route.
Ask for geometry, p/n doping, contact locations, mesh strategy, sweep electrode, voltage range, step, log file, and structure file names.

## PIN photodiode

Search tags: `pin_diode,photodiode,optical,atlas,luminous`.
Ask for intrinsic layer thickness, p/i/n doping, optical wavelength, source type, incidence direction, power, absorption region, bias sweep, and output target.

## SiGe photodiode

Search tags: `sige,ge,photodiode,luminous,optical`.
Ask for Si/Ge/SiGe layer stack, Ge fraction, strain/band-offset assumptions, optical constants source, waveguide or vertical incidence, wavelength, power, bias sweep, and target outputs.

## ATHENA process simulation

Search tags: `athena,process,implantation,diffusion,oxidation,etch,deposition`.
Ask for substrate, orientation, mesh lines, process steps, implant species/dose/energy, diffusion conditions, masks, electrodes, and final structure output.

## MOSFET

Search tags: `mos,mosfet,athena_atlas_flow,iv,cv`.
Ask for gate oxide, gate material/workfunction, source/drain, substrate, channel dimensions, interface charge/traps, and Vg/Vd sweeps.

## Luminous optical simulation

Search tags: `luminous,optical,beam,wavelength,photodiode`.
Ask for wavelength, source power, beam size, incidence direction, polarization if relevant, bias setup, material optical constants, and output metrics.


## Learned example: dryrun_learn_atlas_iv

- Path: `cases\dryrun_pn_complete\decks\02_atlas_simulation.in`
- Verification: user verified
- Purpose: DevEdit generated PN structure read by ATLAS I-V simulation
- Tags: atlas, iv, log, mesh, mesh_infile, method, mobility, models, pn_diode, save, solve
- Reusable command forms: mesh infile="dryrun_pn_complete_device.str"; models srh conmob fldmob fermi; method newton; solve init; log outf="dryrun_pn_complete_iv.log"; save outf="dryrun_pn_complete_final.str"; mesh infile="dryrun_pn_complete_device.str"

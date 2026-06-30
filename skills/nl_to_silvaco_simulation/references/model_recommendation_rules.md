# Model Recommendation Rules

Recommendations must cite local index patterns or be labeled as general TCAD experience. User confirmation is required before final deck generation.

## Si PN / PIN I-V

Candidate: `srh conmob fldmob fermi`.
Reason: local diode-like ATLAS patterns and verified PN control baseline use recombination, concentration-dependent mobility, high-field mobility, and Fermi statistics for heavily doped contacts.
Ask user to confirm before use.

## Reverse breakdown

Ask whether impact ionization is required. Confirm breakdown bias range, step size, compliance, and convergence settings. Do not add impact models automatically.

## Highly doped tunneling

Ask whether band-to-band tunneling or other tunneling models are required. Search examples for confirmed syntax before generating.

## MOS / MOSFET

Ask about CVT/SRH models, interface charge/traps, oxide, gate workfunction, and source/drain setup. Search MOS/MOSFET examples before recommending model sets.

## SiGe / Ge heterojunction

Ask for material parameters, Ge fraction, band offsets, strain, mobility model, recombination model, and optical constants. Do not assume material parameters.

## Photodiode / Luminous

Ask for optical source, wavelength, power, beam geometry, lifetime/recombination, absorption region, and whether built-in optical constants are acceptable.


## Learned example: dryrun_learn_atlas_iv

- Path: `cases\dryrun_pn_complete\decks\02_atlas_simulation.in`
- Verification: user verified
- Purpose: DevEdit generated PN structure read by ATLAS I-V simulation
- Tags: atlas, iv, log, mesh, mesh_infile, method, mobility, models, pn_diode, save, solve
- Reusable command forms: mesh infile="dryrun_pn_complete_device.str"; models srh conmob fldmob fermi; method newton; solve init; log outf="dryrun_pn_complete_iv.log"; save outf="dryrun_pn_complete_final.str"; mesh infile="dryrun_pn_complete_device.str"

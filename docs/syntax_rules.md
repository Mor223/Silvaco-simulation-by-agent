# Syntax Rules

Extracted from local Silvaco example indexes. This file records command forms and reference paths, not full example source.

## Devedit Patterns
### `elec.id`
- Reference examples: `diode\diodeex07\diodeex07.in`
- Command form: `region reg=1 name=anode mat=Gold elec.id=1 work.func=0 color=0x595959 pattern=0xb \`

### `impurity`
- Reference examples: `solar\solarex06\solarex06.in`; `sic\sicex02\sicex02.in`; `sic\sicex03\sicex03.in`; `sic\sicex04\sicex04.in`; `sic\sicex05\sicex05.in`
- Command form: `impurity id=1 region.id=1 imp=Boron \`
- Command form: `impurity id=1 region.id=1 imp=Arsenic \`
- Command form: `impurity id=1 region.id=1 imp=Arsenic \`
- Command form: `extract name="al30" curve(depth,impurity="Aluminum" material="All" x.val=0.0) \`

### `mat=`
- Reference examples: `thermal\thermalex01\thermalex01.in`; `thermal\thermalex02\thermalex02.in`; `thermal\thermalex03\thermalex03.in`; `thermal\thermalex04\thermalex04.in`; `thermal\thermalex05\thermalex05.in`
- Command form: `region reg=1 mat=Silicon color=0xffc000 pattern=0x4 Z1=0 Z2=100 \`
- Command form: `region reg=1 mat=Silicon color=0xffc000 pattern=0x4 Z1=0 Z2=10 \`
- Command form: `region reg=1 mat=Silicon color=0xffc000 pattern=0x4 Z1=0 Z2=10 \`
- Command form: `region reg=1 mat=GaAs color=0xffcb pattern=0x9 Z1=0 Z2=75 \`

### `mesh mode=meshbuild`
- Reference examples: `thermal\thermalex01\thermalex01.in`; `thermal\thermalex02\thermalex02.in`; `thermal\thermalex03\thermalex03.in`; `thermal\thermalex05\thermalex05.in`; `thermal\thermalex06\thermalex06.in`
- Command form: `Mesh Mode=MeshBuild`
- Command form: `mesh infile=thermalex01.str`
- Command form: `Mesh Mode=MeshBuild`
- Command form: `mesh infile=thermalex02.str`

### `region`
- Reference examples: `vcsel\vcselex01\vcselex01.in`; `vcsel\vcselex01\vcselex01_1.set`; `vcsel\vcselex02\vcselex02.in`; `vcsel\vcselex02\vcselex02_1.set`; `vcsel\vcselex03\vcselex03.in`
- Command form: `region material=GaAs thick=0.01 sy=0.005 accept=4e19 top`
- Command form: `region param -101`
- Command form: `region material=GaAs thick=0.01 sy=0.005 accept=4e19 top`
- Command form: `region param -101`

### `struct outf`
- Reference examples: `solar\solarex06\solarex06.in`; `sic\sicex02\sicex02.in`; `sic\sicex03\sicex03.in`; `power\powerex09\powerex09.in`; `power\powerex10\powerex10.in`
- Command form: `struct outf=solarex06_0.str`
- Command form: `struct outf=sicex02_0.str`
- Command form: `struct outf=sicex03_0.str`
- Command form: `struct outf=powerex09_0.str`

### `structure outf`
- Reference examples: `tft\tftex05\tftex05.in`; `tft\tftex12\tftex12.in`; `solar\solarex01\solarex01.in`; `solar\solarex13\solarex13_aux.in`; `solar\solarex16\solarex16_aux.in`
- Command form: `structure outf=tftex05_0.str`
- Command form: `structure outfile=tftex12_0.str`
- Command form: `structure outf=solarex01_0.str`
- Command form: `structure outf=solarex13_$'nbcells'cells_0.str`

## Athena Patterns
### `depo`
- Reference examples: `tft\tftex05\tftex05.in`; `tft\tftex10\tftex10.in`; `tft\tftex12\tftex12.in`; `tft\tftex21\tftex21_aux.in`; `solar\solarex01\solarex01.in`

### `deposit`
- Reference examples: `tft\tftex05\tftex05.in`; `tft\tftex10\tftex10.in`; `tft\tftex12\tftex12.in`; `tft\tftex21\tftex21_aux.in`; `solar\solarex01\solarex01.in`

### `diffuse`
- Reference examples: `solar\solarex01\solarex01.in`; `solar\solarex06\solarex06.in`; `soi\soiex08\soiex08.in`; `power\powerex02\powerex02.in`; `power\powerex07\powerex07.in`
- Command form: `diffuse time=10 temp=900`
- Command form: `diffuse time=10 min temp=900 c.phosphor=2e20`
- Command form: `diffuse time=3 temp=900 weto2 press=1.0`
- Command form: `diffuse time=100 temp=1100`

### `electrode`
- Reference examples: `vcsel\vcselex01\vcselex01.in`; `vcsel\vcselex02\vcselex02.in`; `vcsel\vcselex03\vcselex03.in`; `vcsel\vcselex04\vcselex04.in`; `thermal\thermalex01\thermalex01_0.set`
- Command form: `electrode num=1 name=anode top x.max=6`
- Command form: `electrode num=1 name=anode top x.max=6`
- Command form: `electrode num=1 name=anode top x.max=6`
- Command form: `electrode num=1 name=anode top x.max=6`

### `etch`
- Reference examples: `tft\tftex05\tftex05.in`; `tft\tftex12\tftex12.in`; `solar\solarex01\solarex01.in`; `solar\solarex07\solarex07.in`; `solar\solarex13\solarex13_aux.in`

### `extract`
- Reference examples: `tft\tftex05\tftex05.in`; `tft\tftex12\tftex12.in`; `tft\tftex20\tftex20_aux.in`; `tft\tftex21\tftex21.in`; `tft\tftex21\tftex21_aux.in`
- Command form: `extract name="max_rev_id" y.val from curve(v."gate",i."drain") where x.val=-20`
- Command form: `extract name="Vth" x.val from curve(v."gate", i."drain") where y.val=1e-5`
- Command form: `extract init infile="tftex20_1_$'dt'.log"`
- Command form: `extract init infile="tftex21_vd01_igzo-tokyo_253.log"`

### `implant`
- Reference examples: `solar\solarex01\solarex01.in`; `solar\solarex16\solarex16_aux.in`; `soi\soiex08\soiex08.in`; `sic\sicex04\sicex04.in`; `sic\sicex04\sicex04.set`
- Command form: `implant phos dose=1e15 energy=30`
- Command form: `implant phosph dose=5e15 energy=10`
- Command form: `implant boron dose=8e12 energy=100 pears`
- Command form: `implant aluminum n.ion=10000 dose=3.0e13 tilt=9 rot=45 energy=30 bca sampling`

### `init`
- Reference examples: `vcsel\vcselex01\vcselex01.in`; `vcsel\vcselex02\vcselex02.in`; `vcsel\vcselex03\vcselex03.in`; `vcsel\vcselex04\vcselex04.in`; `tft\tftex01\tftex01.in`
- Command form: `solve init`
- Command form: `solve init`
- Command form: `solve init`
- Command form: `solve init`

### `line x`
- Reference examples: `tft\tftex05\tftex05.in`; `tft\tftex12\tftex12.in`; `solar\solarex01\solarex01.in`; `solar\solarex13\solarex13_aux.in`; `solar\solarex16\solarex16_aux.in`
- Command form: `line x loc=0   spac=0.2`
- Command form: `line x loc=0  spac=1`
- Command form: `line x loc=0.00 spac=1`
- Command form: `line x loc=0.00 				                  spac=200`

### `line y`
- Reference examples: `soi\soiex08\soiex08.in`; `mos2\mos2ex04\mos2ex04.in`; `athena_oxidation\anoxex01\anoxex01.in`; `athena_oxidation\anoxex04\anoxex04.in`; `athena_oxidation\anoxex08\anoxex08.in`
- Command form: `line y loc=0    spac=0.02   tag=top`
- Command form: `line y loc=0    spac=0.05`
- Command form: `line y loc=0    spac=0.05`
- Command form: `line y loc=0  spac=0.05`

### `structure outfile`
- Reference examples: `tft\tftex12\tftex12.in`; `solar\solarex16\solarex16_aux.in`; `soi\soiex08\soiex08.in`; `sic\sicex04\sicex04.in`; `sic\sicex05\sicex05.in`
- Command form: `structure outfile=tftex12_0.str`
- Command form: `structure outfile=solarex16_0_$"Length_half_pyr".str`
- Command form: `structure outfile=soiex08_0.str`
- Command form: `structure outfile=sicex04_init.str`

## Atlas Patterns
### `contact`
- Reference examples: `tft\tftex01\tftex01.in`; `tft\tftex02\tftex02.in`; `tft\tftex03\tftex03.in`; `tft\tftex04\tftex04.in`; `tft\tftex05\tftex05.in`
- Command form: `contact	num=1 alum`
- Command form: `contact	num=1 alum`
- Command form: `contact	num=1 n.polysilicon`
- Command form: `contact	num=1 n.polysilicon`

### `doping`
- Reference examples: `tft\tftex01\tftex01.in`; `tft\tftex02\tftex02.in`; `tft\tftex03\tftex03.in`; `tft\tftex04\tftex04.in`; `tft\tftex06\tftex06.in`
- Command form: `doping     reg=2  uniform conc=7.e14 n.type`
- Command form: `doping     reg=2  uniform conc=7.e14 n.type`
- Command form: `doping     reg=2  uniform conc=1.e11 n.type`
- Command form: `doping     reg=2  uniform conc=1.e11 n.type`

### `electrode`
- Reference examples: `vcsel\vcselex01\vcselex01.in`; `vcsel\vcselex02\vcselex02.in`; `vcsel\vcselex03\vcselex03.in`; `vcsel\vcselex04\vcselex04.in`; `thermal\thermalex01\thermalex01_0.set`
- Command form: `electrode num=1 name=anode top x.max=6`
- Command form: `electrode num=1 name=anode top x.max=6`
- Command form: `electrode num=1 name=anode top x.max=6`
- Command form: `electrode num=1 name=anode top x.max=6`

### `extract`
- Reference examples: `tft\tftex05\tftex05.in`; `tft\tftex12\tftex12.in`; `tft\tftex20\tftex20_aux.in`; `tft\tftex21\tftex21.in`; `tft\tftex21\tftex21_aux.in`
- Command form: `extract name="max_rev_id" y.val from curve(v."gate",i."drain") where x.val=-20`
- Command form: `extract name="Vth" x.val from curve(v."gate", i."drain") where y.val=1e-5`
- Command form: `extract init infile="tftex20_1_$'dt'.log"`
- Command form: `extract init infile="tftex21_vd01_igzo-tokyo_253.log"`

### `log off`
- Reference examples: `quantum\quantumex22\quantumex22.in`
- Command form: `log off`

### `log outf`
- Reference examples: `vcsel\vcselex01\vcselex01.in`; `vcsel\vcselex02\vcselex02.in`; `vcsel\vcselex03\vcselex03.in`; `vcsel\vcselex04\vcselex04.in`; `thermal\thermalex08\thermalex08.in`
- Command form: `log outf=vcselex01.log`
- Command form: `log outf=vcselex02.log`
- Command form: `log outf=vcselex03.log`
- Command form: `log outf=vcselex04.log`

### `material`
- Reference examples: `vcsel\vcselex01\vcselex01.in`; `vcsel\vcselex02\vcselex02.in`; `vcsel\vcselex03\vcselex03.in`; `vcsel\vcselex04\vcselex04.in`; `thermal\thermalex01\thermalex01.in`
- Command form: `region material=GaAs thick=0.01 sy=0.005 accept=4e19 top`
- Command form: `material material=AlGaAs eg300=1.42 affin=4.07 nc300=4.35e17 nv300=8.16e18 permi=13.2`
- Command form: `region material=GaAs thick=0.01 sy=0.005 accept=4e19 top`
- Command form: `material material=AlGaAs eg300=1.42 affin=4.07 nc300=4.35e17 nv300=8.16e18 permi=13.2`

### `mesh infile`
- Reference examples: `thermal\thermalex01\thermalex01.in`; `thermal\thermalex02\thermalex02.in`; `thermal\thermalex03\thermalex03.in`; `thermal\thermalex04\thermalex04.in`; `thermal\thermalex05\thermalex05.in`
- Command form: `Mesh Mode=MeshBuild`
- Command form: `mesh infile=thermalex01.str`
- Command form: `Mesh Mode=MeshBuild`
- Command form: `mesh infile=thermalex02.str`

### `method`
- Reference examples: `vcsel\vcselex02\vcselex02.in`; `vcsel\vcselex03\vcselex03.in`; `thermal\thermalex01\thermalex01.in`; `thermal\thermalex02\thermalex02.in`; `thermal\thermalex03\thermalex03.in`
- Command form: `method block`
- Command form: `method block`
- Command form: `method`
- Command form: `method`

### `models`
- Reference examples: `thermal\thermalex01\thermalex01.in`; `thermal\thermalex02\thermalex02.in`; `thermal\thermalex03\thermalex03.in`; `thermal\thermalex04\thermalex04.in`; `thermal\thermalex05\thermalex05.in`
- Command form: `models thermal`
- Command form: `models thermal`
- Command form: `models thermal`
- Command form: `models thermal`

### `region`
- Reference examples: `vcsel\vcselex01\vcselex01.in`; `vcsel\vcselex01\vcselex01_1.set`; `vcsel\vcselex02\vcselex02.in`; `vcsel\vcselex02\vcselex02_1.set`; `vcsel\vcselex03\vcselex03.in`
- Command form: `region material=GaAs thick=0.01 sy=0.005 accept=4e19 top`
- Command form: `region param -101`
- Command form: `region material=GaAs thick=0.01 sy=0.005 accept=4e19 top`
- Command form: `region param -101`

### `save outf`
- Reference examples: `vcsel\vcselex01\vcselex01.in`; `vcsel\vcselex02\vcselex02.in`; `vcsel\vcselex03\vcselex03.in`; `vcsel\vcselex04\vcselex04.in`; `tft\tftex01\tftex01.in`
- Command form: `save outf=vcselex01_0.str`
- Command form: `save outf=vcselex02_0.str`
- Command form: `save outf=vcselex03_0.str`
- Command form: `save outf=vcselex04_0.str`

### `solve`
- Reference examples: `vcsel\vcselex01\vcselex01.in`; `vcsel\vcselex02\vcselex02.in`; `vcsel\vcselex03\vcselex03.in`; `vcsel\vcselex04\vcselex04.in`; `thermal\thermalex01\thermalex01.in`
- Command form: `solve init`
- Command form: `solve init`
- Command form: `solve init`
- Command form: `solve init`

### `solve init`
- Reference examples: `vcsel\vcselex01\vcselex01.in`; `vcsel\vcselex02\vcselex02.in`; `vcsel\vcselex03\vcselex03.in`; `vcsel\vcselex04\vcselex04.in`; `tft\tftex01\tftex01.in`
- Command form: `solve init`
- Command form: `solve init`
- Command form: `solve init`
- Command form: `solve init`

## Luminous Patterns
### `luminous`
- Reference examples: `vcsel\vcselex01\vcselex01.in`; `vcsel\vcselex02\vcselex02.in`; `vcsel\vcselex03\vcselex03.in`; `vcsel\vcselex04\vcselex04.in`; `thermal\thermalex08\thermalex08.in`

### `optical`
- Reference examples: `thermal\thermalex08\thermalex08.in`; `solar\solarex01\solarex01.in`; `solar\solarex01\solarex01_1.set`; `solar\solarex01\solarex01_3.set`; `solar\solarex02\solarex02.in`

### `photocurrent`
- Reference examples: `solar\solarex01\solarex01.in`; `solar\solarex01\solarex01_1.set`; `solar\solarex01\solarex01_3.set`; `solar\solarex04\solarex04.in`; `solar\solarex04\solarex04_0.set`

## Known Risk / Incompatible Patterns

- `imp.refine x=...`: failed in local DevEdit; prefer confirmed forms or omit.
- `-ascii` / `dbascii`: unavailable in the current Windows DeckBuild installation.
- DevEdit electrode inheritance into ATLAS must be manually checked in DeckBuild logs.
- `tonyplot`: forbidden in generated automation decks.

### `tonyplot`
- Seen in indexed material: `vcsel\vcselex01\vcselex01.in`; `vcsel\vcselex02\vcselex02.in`; `vcsel\vcselex03\vcselex03.in`; `vcsel\vcselex04\vcselex04.in`; `thermal\thermalex01\thermalex01.in`; `thermal\thermalex02\thermalex02.in`; `thermal\thermalex03\thermalex03.in`; `thermal\thermalex04\thermalex04.in`


## ATLAS mesh infile missing device str

- Trigger scenario: user-provided Silvaco runtime log.
- Typical error: `ATLAS> mesh infile="missing_device.str"`
- Error stage: ATLAS mesh infile
- Common cause: inspect deck/log consistency, first-step structure output, electrode names, log/solve ordering, and confirmed syntax.
- Recommended fix form: No safe automatic rewrite rule matched this error.
- Requires user confirmation: yes, before final deck replacement.
- Static check rule: add or keep checks when the error is detectable from text.


## Learned example: dryrun_learn_atlas_iv

- Path: `cases\dryrun_pn_complete\decks\02_atlas_simulation.in`
- Verification: user verified
- Purpose: DevEdit generated PN structure read by ATLAS I-V simulation
- Tags: atlas, iv, log, mesh, mesh_infile, method, mobility, models, pn_diode, save, solve
- Reusable command forms: mesh infile="dryrun_pn_complete_device.str"; models srh conmob fldmob fermi; method newton; solve init; log outf="dryrun_pn_complete_iv.log"; save outf="dryrun_pn_complete_final.str"; mesh infile="dryrun_pn_complete_device.str"


## Error file not found or file system error 289

- Trigger scenario: user-provided Silvaco runtime log.
- Typical error: `Error: file not found or file system error. 289`
- Error stage: ATLAS mesh infile
- Common cause: inspect deck/log consistency, first-step structure output, electrode names, log/solve ordering, and confirmed syntax.
- Recommended fix form: Mesh infile/file-open errors require confirming the first-step `.str` filename and working directory; no safe automatic filename rewrite was made.
- Requires user confirmation: yes, before final deck replacement.
- Static check rule: add or keep checks when the error is detectable from text.

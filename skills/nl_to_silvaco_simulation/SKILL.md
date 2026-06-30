---
name: nl_to_silvaco_simulation
description: Generate Silvaco TCAD DevEdit/ATHENA + ATLAS .in files from natural-language semiconductor device simulation requirements. Use for parameter clarification, case-pattern lookup, model suggestion, deck generation, static checking, error-learning, and new-example learning. Does not run Silvaco.
---

# Purpose

Use this skill to turn natural-language semiconductor simulation requests into confirmed parameters, compact case-pattern lookup, model suggestions, and generated DevEdit/ATHENA + ATLAS `.in` files.

## When To Use

Use it for deck drafting, parameter clarification, model suggestion, static checking, user-provided error analysis, and compact learning from user-authorized examples.

## When Not To Use

Do not use it to run simulators, launch GUIs, manage licenses, parse runtime results by default, or redistribute proprietary examples.

## Inputs

Natural-language request, confirmed YAML specs, optional compact pattern indexes, optional user-provided deck/log text, and optional user-owned examples for summarization.

## Outputs

Questionnaires, completed specs, generated `.in` deck files, static-check reports, model recommendation notes, error-analysis reports, and compact learned summaries.

## Workflow Router

New deck requests use Generate Deck Workflow. Error logs use Error Analysis Workflow. User-authorized examples use New Example Learning Workflow. Documentation/index updates use Knowledge Update Workflow.

## Generate Deck Workflow

Classify route, ask for missing parameters, search compact public patterns, suggest models, render first-step and ATLAS decks, then run static checks only.

## Error Analysis Workflow

Read user-provided deck/log text, locate the first explicit error, classify the stage, propose a limited fix, and record reusable knowledge.

## New Example Learning Workflow

Summarize user-owned or user-authorized examples as tags, snippets, reusable patterns, risk notes, and verification status. Do not copy complete commercial decks.

## Knowledge Update Workflow

Synchronize references and public data after learning, then audit for local paths, license hints, runtime outputs, and proprietary content.

## DevEdit + ATLAS Deck Rules

Use DevEdit to generate a structure file, then use ATLAS `mesh infile=`. Do not invent unverified DevEdit syntax.

## ATHENA + ATLAS Deck Rules

Use ATHENA only when the user requested process simulation. The ATLAS deck must read the ATHENA structure output.

## ATLAS Simulation Deck Rules

Confirm models, contacts, sweep electrode, sweep range, output names, and final save file. Ensure `log outf=` is followed by solve commands and `log off`.

## Luminous / Optical Deck Rules

Confirm wavelength, source type, incidence direction, power/intensity, optical constants, bias condition, and requested outputs before rendering.

## Model Recommendation Rules

Tie each recommendation to confirmed material, device type, transport regime, optical effects, and requested outputs.

## Static Checking Rules

Check plotting commands, unavailable helper flags, missing `mesh infile`, inconsistent structure filenames, missing `solve init`, missing `log off`, and unconfirmed complex-physics tokens.

## Sanitization And Copyright Rules

Keep public artifacts free of local paths, user identity, license data, runtime outputs, and full proprietary examples.

## Absolute Prohibitions

- Do not run Silvaco.
- Do not launch DeckBuild.
- Do not call ATLAS / ATHENA / DevEdit.
- Do not use text-mode helper flags that depend on unavailable helper binaries.
- Do not parse simulation outputs as part of the default workflow.
- Do not include or redistribute proprietary Silvaco examples.
- Do not guess unconfirmed device or simulation parameters.
- Do not use local absolute paths in generated public artifacts.

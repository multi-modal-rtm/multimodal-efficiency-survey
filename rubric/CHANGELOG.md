# Rubric Changelog

## v1.1 — 2026-05-24 (post-pilot revisions)

Pilot coding of 12 papers (`coding/pilot/coder_A_pilot.csv`) surfaced rubric gaps in specific axes. Changes:

### Added
- Axis 3a (Optimizer): `federated-optimizer`, `policy-gradient`, `Adam-no-WD`, `LAMB-LARS` (4 papers required `other-specify` for these families)
- Axis 4b (Sparsity): `MoE-over-PEFT` (MMLORA paper applies MoE routing to LoRA modules, distinct from architectural backbone MoE)
- Cross-cutting field: `domain_relevance` (enum: `core-affective` / `adjacent-interaction` / `method-source`)

### Changed
- Axis 4b gotcha note expanded to distinguish architectural MoE, MoE-over-PEFT, and MoE topology (Axis 5)

### Rejected after consideration
- TPU-pod as Axis 5 topology category. TPU is hardware (captured in `hardware_reported`), not topology. A TPU pod can run any topology.
- Fourth efficiency_engagement code for foundational-but-inefficient anchor papers. Three-level scale preserved; anchor status captured in `coder_notes` free text.

### Pilot findings driving v1.1
- NR rates validated by spot-check: the field genuinely underreports precision, memory techniques, and compute. Real methodology finding.
- 5 of 12 pilot papers were vision-language instruction-following (LLaMA-Adapter family, LaVIN, VideoLLaMA, others) — adjacent to scope, not core. `domain_relevance` field added rather than dropping them.

## v1.0 — 2026-05-23 (pre-registration)

Initial release.

Status# Multimodal Efficiency Survey — Coding Rubric

**Version:** 1.1
**Date:** 2026-05-24
**Previous version:** v1.0 (tagged 2026-05-23)
**Status**: Active. Pre-registered as v1.0 on 2026-05-23; revised to v1.1 on 2026-05-24 following pilot coding of twelve papers. Subsequent rubric changes require a new tagged release and CHANGELOG entry.

## Scope

This rubric governs systematic qualitative coding of papers for a survey on efficient multimodal architectures for human interaction modeling, targeting the Journal of Artificial Intelligence Research (JAIR). In-scope papers: multimodal models that analyze human social and affective behavior from audio, visual, and text streams. All coding is performed manually by two independent human coders.

## Global Coding Conventions

- Each axis (except multi-label sub-axes) takes a `primary` value plus an optional `secondary` array.
- `NA` means the axis does not engage with the paper's contribution.
- `NR` means the axis applies but the paper does not report enough information to code it.
- `NA` and `NR` are distinct codes. Do not conflate them. The NR rate per axis is itself a finding.
- `other-specify` requires a free-text justification in `coder_notes`.
- Coding unit is per paper, against the paper's headline/recommended configuration. Variants and ablations go in the `variants_explored` free-text field.

---

## Axis 1: Architecture and Fusion

### Axis 1a — Encoder Configuration

**Field:** `axis_1a_encoder_config`
**Type:** primary + secondary

| Code | Definition |
|------|-----------|
| `unimodal-pretrained-frozen` | Each modality uses a unimodal pretrained encoder (e.g., HuBERT, ViT) with frozen weights |
| `unimodal-pretrained-tuned` | Unimodal pretrained encoders, updated during training |
| `multimodal-pretrained` | Multimodal pretrained encoder used as a unit (CLIP, ImageBind, LanguageBind, AV-HuBERT) |
| `from-scratch` | No pretrained encoder; trained from random initialization |
| `mixed` | Some encoders frozen, others tuned |
| `NA` | Paper does not involve an encoder |
| `NR` | Encoder configuration not reported |

**Evidence rule:** Read from the methods section's pretraining/initialization paragraph. Look for explicit statements about which components are frozen versus updated.

### Axis 1b — Fusion Mechanism

**Field:** `axis_1b_fusion_mechanism`
**Type:** primary + secondary

| Code | Definition |
|------|-----------|
| `early-concat` | Feature concatenation before any cross-modal layer |
| `late-fusion` | Per-modality predictions combined at logit or decision level |
| `dense-cross-attention` | Full pairwise cross-attention; MulT-style |
| `bottleneck-attention` | Learned tokens mediating modalities; MBT-style (Nagrani et al. 2021) |
| `progressive` | Staged modality injection; CREMA-style |
| `query-based` | Learned queries; Q-Former, Perceiver-style |
| `linear-mlp-projection` | Modality projected into language model token space; LLaVA-style |
| `gated-mixture` | Gating networks or mixture-of-experts over modalities |
| `tensor-fusion` | Outer-product or low-rank tensor operations; TFN (Zadeh 2017), LMF (Liu 2018) and descendants |
| `subspace-decomposition` | Modality-invariant + modality-specific subspace factorization; MISA, Self-MM |
| `other-specify` | Mechanism does not fit; requires free-text justification in `coder_notes` |
| `NA` | Paper is single-modality |
| `NR` | Fusion mechanism not reported |

**Evidence rule:** Read the architecture figure plus the description of what attention or projection sits between modalities. Coders must be able to point to a specific equation or block. If the paper invents a fusion variant, code by closest family and note the variant in free text.

**Gotcha:** A "transformer encoder over concatenated modality tokens" is `dense-cross-attention` if attention is unconstrained, `bottleneck-attention` if there's a constraint on which tokens attend to which, and `other-specify` (note as modality-aware-masking) if attention masks are modality-aware in a Perceiver-IO sense. Coders frequently conflate the first two.

### Axis 1c — Modality Set

**Field:** `axis_1c_modality_set`
**Type:** multi-label array (no primary, no NA — every paper has at least one modality)

| Code | Definition |
|------|-----------|
| `audio` | Speech, music, environmental sound |
| `vision-image` | Static images, individual frames |
| `vision-video` | Temporal video sequences |
| `text` | Tokenized natural language |
| `physiological` | Heart rate, GSR, EEG, etc. |
| `motion` | Body pose, gesture tracking, motion capture |
| `other` | Modality not listed; specify in `coder_notes` |

**Decision rule:** Only code modalities the model actually processes. Future-work mentions do not count.

---

## Axis 2: Adaptation Strategy

**Field:** `axis_2_adaptation`
**Type:** primary + secondary

| Code | Definition |
|------|-----------|
| `full-FT` | All parameters updated |
| `frozen-backbone-linear` | Linear or shallow head only, encoders frozen |
| `LoRA-family` | LoRA, DoRA, VeRA — low-rank additive updates |
| `adapter-modules` | Houlsby or Pfeiffer-style inserted MLP adapters |
| `prefix-prompt-tuning` | Learned tokens, no weight updates |
| `zero-init-attention` | LLaMA-Adapter family — gated cross-attention with zero-initialized gates |
| `bias-only` | BitFit and related — only bias parameters updated |
| `partial-FT` | Specific layers or modules unfrozen, no PEFT module used |
| `hybrid` | Combination, e.g., LoRA on text encoder plus full FT on fusion module |
| `NA` | Paper does not involve adaptation (e.g., random init architecture study) |
| `NR` | Adaptation strategy not reported |

**Evidence rule:** Look for explicit statement of which parameters are trainable, parameter count of trainable subset, or a "trainable parameters" table. If the paper says "we fine-tune" without specifying scope, code as `NR` and flag.

**Gotcha:** "Fine-tuning the fusion module" while keeping encoders frozen is `partial-FT`, not `full-FT`. The unit of analysis is the whole model.

---

## Axis 3: Optimization

### Axis 3a — Optimizer

**Field:** `axis_3a_optimizer`
**Type:** primary + secondary

| Code | Definition |
|------|-----------|
| `AdamW-standard` | Standard AdamW |
| `Adam-8bit` | bitsandbytes 8-bit Adam |
| `SGD-momentum` | SGD with momentum |
| `Lion` | Lion optimizer |
| `LOMO-AdaLOMO` | Hook-fused gradient + update (LOMO, AdaLOMO) |
| `GaLore` | Gradient low-rank projection |
| `Adafactor` | Adafactor |
| `federated-optimizer` | Federated learning optimizers including FedAvg, FedProx, FedDisc-family |
| `policy-gradient` | Policy-gradient methods including GRPO, PPO, RLHF-style training |
| `Adam-no-WD` | Adam without weight decay (distinct from AdamW) |
| `LAMB-LARS` | Layer-wise adaptive optimizers (LAMB, LARS) for large-batch training |
| `other-specify` | Other optimizer; specify in `coder_notes` |
| `NA` | Paper does not involve training |
| `NR` | Optimizer not reported |

**Evidence rule:** Usually in the training or implementation section. If the paper uses an unmodified PyTorch default without specifying, code as `NR`.

### Axis 3b — Memory Techniques

**Field:** `axis_3b_memory_techniques`
**Type:** multi-label array

| Code | Definition |
|------|-----------|
| `gradient-checkpointing` | Trading compute for activation memory |
| `activation-recomputation` | Distinct from gradient-checkpointing when explicitly named separately |
| `gradient-accumulation` | Accumulating gradients across micro-batches |
| `CPU-offload` | Moving optimizer state or parameters to CPU |
| `NVMe-offload` | Moving state to NVMe storage |
| `kernel-fusion-Triton` | Triton-based fused kernels including Liger Kernel and Unsloth |
| `FlashAttention` | IO-aware attention kernels (Dao et al.) |
| `paged-optimizers` | Paged optimizer state (QLoRA-style) |
| `none-reported` | No memory technique mentioned |

**Evidence rule:** Often in implementation details or appendix. Ctrl-F for "checkpointing," "offload," "Flash," "Triton," "Liger," "Unsloth," "fused." If the paper names Unsloth or Liger as a framework, code the kernel-fusion-Triton entry as present even if specific kernels are not enumerated.

**Gotcha:** Mixed-precision training is Axis 4a, not Axis 3b. Do not code it here.

---

## Axis 4: Precision and Sparsity

### Axis 4a — Precision

**Field:** `axis_4a_precision`
**Type:** primary + secondary

| Code | Definition |
|------|-----------|
| `FP32` | Full 32-bit precision |
| `FP16-mixed` | Mixed-precision AMP with FP32 master weights |
| `BF16-mixed` | BFloat16 mixed precision |
| `INT8-PTQ` | Post-training quantization for inference |
| `INT8-QAT` | Quantization-aware training |
| `INT4-NF4` | 4-bit NormalFloat (QLoRA-style) base |
| `mixed-other` | Mixed precision not falling into above categories |
| `NA` | Paper does not involve numerical precision choices |
| `NR` | Precision not reported |

### Axis 4b — Sparsity

**Field:** `axis_4b_sparsity`
**Type:** primary + secondary

| Code | Definition |
|------|-----------|
| `none` | No sparsity used |
| `unstructured-pruning` | Magnitude-based or gradual unstructured pruning |
| `structured-pruning` | Head, channel, or layer pruning |
| `N-M-structured` | N:M structured sparsity (e.g., 2:4) |
| `RigL-family` | Dynamic sparse training (RigL, SRigL) |
| `MoE-architectural` | MoE used as explicit architectural efficiency choice (not inherited) |
| `MoE-over-PEFT` | Mixture-of-Experts routing applied to PEFT modules (LoRA experts, adapter experts), distinct from architectural backbone MoE |
| `NA` | Paper does not engage with sparsity |
| `NR` | Sparsity mentioned but not characterized |

**Evidence rule:** Needs an explicit method named or a sparsity ratio reported.

**Gotcha:** Distillation is not sparsity. A paper using Mixtral as a backbone is not "doing MoE for efficiency" — it inherits MoE. Code `MoE-architectural` only when the paper makes an architectural sparsity choice for the model being built. Code `MoE-over-PEFT` when MoE routing is applied to inserted PEFT modules (e.g., MoE-over-LoRA-experts as in MMLORA). MoE topology (X-MoE-style expert parallelism) goes in Axis 5.

---

## Axis 5: Training Topology

**Field:** `axis_5_topology`
**Type:** primary + secondary

| Code | Definition |
|------|-----------|
| `single-GPU` | One accelerator |
| `single-node-multi-GPU-DDP` | Standard data parallel within one node |
| `ZeRO-1` | DeepSpeed ZeRO stage 1 |
| `ZeRO-2` | DeepSpeed ZeRO stage 2 |
| `ZeRO-3` | DeepSpeed ZeRO stage 3 |
| `FSDP` | PyTorch Fully Sharded Data Parallel |
| `ZeRO-family-NR-stage` | DeepSpeed/ZeRO used but stage not specified |
| `tensor-pipeline-parallel` | Tensor parallel, pipeline parallel, or both |
| `3D-parallel` | Combined data + tensor + pipeline parallelism |
| `DiLoCo-family` | Asynchronous low-communication distributed training |
| `Petals-family` | Decentralized inference or training over heterogeneous nodes |
| `MoE-distributed` | X-MoE-style expert parallelism as primary topology choice |
| `federated` | Federated learning (FedAvg-family, edge-distributed) |
| `NA` | Inference-only paper |
| `NR` | Topology not specified |

**Evidence rule:** Hardware section plus framework section (DeepSpeed config, FSDP wrapping, training launcher). If the paper says "8x A100" without further framework detail, code as `single-node-multi-GPU-DDP` (PyTorch default) and flag in `coder_notes`.

**Gotcha:** A paper may use DeepSpeed but only ZeRO-1, which is barely different from DDP. Stage matters. If unclear, use `ZeRO-family-NR-stage`.

---

## Cross-Cutting Fields

These are coded per paper but are not categorical axes.

| Field | Type | Description |
|-------|------|-------------|
| `hardware_reported` | string | Verbatim hardware string from the paper |
| `hardware_tier` | enum | `consumer` / `prosumer` / `enterprise` / `hyperscaler` / `NR` |
| `compute_reported` | object | `{value: string, reported: boolean}` — captures both the figure and whether the paper reported any compute figure |
| `trainable_params` | object | `{count: string, percent: number}` — e.g., `{"7B", 0.6}` |
| `datasets` | array | Controlled vocabulary, multi-label |
| `task` | string | Controlled vocabulary |
| `efficiency_engagement` | enum | `primary` / `secondary` / `incidental` |
| `domain_relevance` | enum | `core-affective` / `adjacent-interaction` / `method-source` |
| `simulation_methodology` | string (free text) | Pre-flight tooling, theoretical cost analysis |
| `variants_explored` | string (free text) | Ablations or model variants tested |
| `coder_notes` | string (free text) | Coder rationale, ambiguities, `other-specify` elaborations |

### Hardware Tier (VRAM-Based Cuts)

Tier is determined by aggregate VRAM and node count, not chip-class identity.

| Tier | Definition |
|------|-----------|
| `consumer` | ≤24 GB aggregate VRAM (e.g., single RTX 3090, 4090, 5090) |
| `prosumer` | 24–80 GB single-node (e.g., single A100 40 GB, dual A6000, RTX 6000 Ada) |
| `enterprise` | >80 GB aggregate VRAM or multi-node A100/H100 cluster (DGX-class) |
| `hyperscaler` | ≥128 chips OR explicit cluster-scale framework operating at production scale (Megatron-LM, DeepSpeed-MII production, analogous) |
| `NR` | Hardware not reported |

**Worked examples:**
- 8× A100 80 GB DGX → `enterprise`
- 1× A100 40 GB on Colab Pro → `prosumer`
- 1× RTX 4090 24 GB → `consumer`
- 1024× H100 cluster with Megatron-LM → `hyperscaler`
- 2× A6000 48 GB workstation → `prosumer` (single-node, between thresholds)

### Efficiency Engagement

| Code | Definition |
|------|-----------|
| `primary` | Efficiency is the paper's headline contribution |
| `secondary` | Paper makes a meaningful efficiency choice as part of a larger contribution |
| `incidental` | Paper mentions infrastructure choices but they are not load-bearing |

**Why this field matters:** NR rates partitioned by `efficiency_engagement` separate "the field underreports memory techniques where they matter" (real finding) from "this paper didn't need to report because efficiency was orthogonal to the contribution" (not a finding).

### Domain Relevance

| Code | Definition |
|------|-----------|
| `core-affective` | Paper's primary task is human social or affective behavior analysis (emotion recognition, sentiment, engagement, social action detection on IEMOCAP/MELD/CMU-MOSEI/AffWild2/Social-IQ/etc.) |
| `adjacent-interaction` | Paper analyzes human-generated multimodal content but not specifically social/affective (general multimodal activity recognition, audio-visual event localization without affective component) |
| `method-source` | Paper develops a method on non-affective data (vision-language instruction-following, image captioning, ScienceQA) that is cited because the method transfers to affective work |

**Why this field exists:** Downstream analyses defending claims about "the affective computing field" should filter to `core-affective` papers. `method-source` papers establish that a technique exists but should not be used to support claims about how the affective community adopts techniques.

### Controlled Vocabularies

**Datasets (multi-label):** IEMOCAP, MELD, CMU-MOSEI, CMU-MOSI, AffWild2, AudioSet, VGGSound, AVA, EPIC-KITCHENS, Social-IQ, RAVDESS, CREMA-D, SAVEE. Add entries as encountered; document additions in `CHANGELOG.md`.

**Tasks:** categorical-emotion-recognition, dimensional-affect, sentiment, engagement, multimodal-activity-recognition, social-action-detection, audio-visual-event-localization, multimodal-sentiment-analysis. Add entries as encountered.

---

## Coding Procedure

1. Read the paper's abstract, introduction, and methods section first.
2. Identify the headline contribution. This determines `efficiency_engagement` and constrains which axis values count as "primary."
3. Code each axis in order. Use `NA` if the axis does not engage with the paper. Use `NR` if it engages but information is missing.
4. For `other-specify` codes, write the justification in `coder_notes` before moving on.
5. Add any axis where you felt uncertain to `uncertainty_flags`.
6. Log time spent per paper.

## Pre-Registration

The rubric was pre-registered as v1.0 on 2026-05-23 prior to any paper coding. Post-pilot revisions were tagged as v1.1 on 2026-05-24 with the full diff documented in CHANGELOG.md. All future changes require a new tagged version and a CHANGELOG.md entry. Retroactive re-coding of already-coded papers requires explicit documentation of which papers were affected and why.

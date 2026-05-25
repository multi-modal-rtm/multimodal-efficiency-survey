# 3. Pilot Study and Methodology Refinement
Prior to executing the full systematic search, we conducted a pilot coding phase on a stratified sample of 12 papers spanning 2017 to 2025. The objective of this pilot was to stress-test the pre-registered taxonomy (v1.0), estimate baseline coding time, and surface any semantic drift or structural gaps in the rubric. The pilot sample included foundational dense models, bottleneck architectures, and recent parameter-efficient fine-tuning (PEFT) approaches.

This phase proved critical for calibrating our methodological boundaries, resulting in a revised v1.1 rubric that governs the full survey. The rubric was pre-registered on GitHub as release v1.0 prior to coding. Post-pilot revisions were tagged as v1.1. The full audit trail is publicly available at [https://github.com/multi-modal-rtm/multimodal-efficiency-survey/releases/tag/v1.1].

## 3.1 Resolving Scope and Corpus Boundaries
The most significant structural challenge surfaced during the pilot pertained to corpus inclusion boundaries. Five of the twelve pilot papers evaluated highly efficient multimodal architectures (e.g., LLaMA-Adapter V1/V2, LaVIN) but were optimized for general vision-language instruction following (e.g., ScienceQA, WebVid) rather than human social or affective analysis. Excluding these papers entirely would prevent us from quantitatively tracking the cross-pollination delay—the migration of efficiency techniques from general multimodal LLMs into specific interaction domains—which is a central hypothesis of this survey. To preserve this data without polluting the denominator of our target distributions, we introduced a domain_relevance field in v1.1, partitioning papers into core-affective, adjacent-interaction, and method-source.

Distinct from the domain_relevance partitioning, we also established a strict binary exclusion rule for pure infrastructure papers (e.g., PyTorch FSDP, VeOmni). Papers that invent a distributed training framework or memory kernel, but do not propose or evaluate a multimodal architecture, are relegated to the background literature and excluded from the coded corpus to prevent systemic skew in our architectural axes.

## 3.2 Rubric Calibration and Strained Cases
The pilot revealed specific areas where the v1.0 taxonomy lacked sufficient granularity, forcing an artificially high rate of other-specify codings.

Expansion of Optimization Categories (Axis 3a): We observed a 33% other-specify rate for optimization strategies. To rectify this, Axis 3a was expanded to include federated-optimizer (e.g., FedAvg, FedOpt), policy-gradient (capturing PPO and GRPO used in modern modality selection networks), and Adam-no-WD.

Sparse Adaptation vs. Architectural Sparsity (Axis 4b): The coding of MMLORA (Fang et al., 2025) highlighted a critical edge case. The model utilizes a Mixture-of-Experts (MoE) routing mechanism, but applies it exclusively to inserted LoRA adapters rather than the frozen LLM backbone. To prevent coders from conflating this with architectural sparsity, we added a MoE-over-PEFT category to Axis 4b.

Fusion Ambiguities (Axis 1b): The pilot exposed the necessity of strict adherence to mathematical definitions over terminology. For instance, FedMultimodal (Feng et al., 2023) describes using "attention-based fusion." Upon reviewing the mathematical formulation in the text, it was revealed to be an additive/hierarchical attention mechanism over concatenated temporal embeddings. This necessitated an other-specify coding rather than dense-cross-attention (which implies pairwise token attention) or late-fusion (logit-level combination), highlighting the importance of deep-reading methodologies rather than relying on abstract keywords.

Structured Re-verification: The pilot also demonstrated the value of structured re-verification on every coded row. One pilot paper (originally bibkey'd lei2025grpo) was misattributed during initial coding; the actual author is Chen et al. (2025). This error, alongside an accompanying task miscoding (sentiment-analysis vs. categorical-emotion-recognition), was caught and corrected in v1.1.

## 3.3 Reporting Standards and the "NR" Verification
Initial pilot coding yielded high "Not Reported" (NR) rates for both numerical precision (Axis 4a) and memory techniques (Axis 3b). Because an inflated NR rate could indicate a superficial coder pass rather than a literature deficit, the first coder conducted a targeted 20-minute verification on two high-NR papers, examining appendices, implementation details, and supplementary code where available.

The verification confirmed that the high NR rates reflect a systemic reporting deficit rather than coder oversight. The affective computing community appears to frequently omit lower-level optimization and memory parameters that are considered standard reporting in core natural language processing literature.

Additionally, we calibrated the efficiency_engagement field. Coders were instructed to be highly conservative, reserving the primary designation solely for papers where computational or memory efficiency is the headline contribution. Papers where efficiency is a beneficial byproduct of an architectural innovation were downgraded to secondary.

## 3.4 Coder Burden and Reliability
Estimated coding time, based on session retrospection, was approximately 28 minutes per paper for the first batch, stabilizing to approximately 18 minutes per paper as the rubric's decision rules became familiar. Assuming this stabilized rate generalizes to the full corpus of 80 to 150 papers, the dual-coder methodology requires approximately 45 hours of independent coding time per researcher prior to consensus reconciliation.

Intra-coder and inter-coder reliability will be reported in subsequent sections following the full coding pass; the pilot established the rubric stability required for those measurements to be meaningful.

## 3.5 Preliminary Field Insights
While the pilot sample of twelve papers is too small to support definitive statistical claims, several patterns emerged that warrant explicit verification in the full coded corpus.

The cross-pollination of parameter-efficient fine-tuning (PEFT) and memory-efficient optimization into human-interaction modeling appears highly nascent, surfacing primarily in 2024 and 2025 publications. Furthermore, this migration currently seems hyper-concentrated on specific tasks—primarily categorical emotion recognition on IEMOCAP, with secondary representation on MELD and CMU-MOSEI/MOSI—rather than being evenly distributed across engagement forecasting or physiological fusion domains. These hypotheses will be tested against the full systematic sample in §6.
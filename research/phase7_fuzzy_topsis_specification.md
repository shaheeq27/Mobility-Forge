# Phase 7 — Fuzzy TOPSIS Methodology Specification

**Project:** MobilityForge — Building Better Mobility Systems
**Specification date:** 2026-10-22
**Status:** research design; no weights, fuzzy ratings, scores, or rankings have been generated.

## 1. Executive summary

The project will use Fuzzy TOPSIS because it is mandatory for the assignment. The smallest evidence-supported design remains the six Tumkur Road mid-block sections from BBMP Table 8 (PDF page 46), with peak PCU volume and V/C as the primary criteria. LOS remains a validation and interpretation field by default because the report defines LOS using service measures including V/C; treating it as a third independent criterion risks double-counting congestion.

Morning/evening and direction are not to be aggregated silently. The safest initial design is four separate model runs over the same six sections: morning/towards Yeshwanthpur, morning/towards Nagasandra, evening/towards Yeshwanthpur, and evening/towards Nagasandra. Exact clock-time windows for Table 8 remain unresolved; Table 7 times must not be transferred to Table 8.

This document specifies a Chen-style triangular-fuzzy-number workflow while separating literature-supported operations from project decisions that still require approval. The observed BBMP values remain the source matrix; no linguistic ratings, weights, or rankings are populated yet.

## 2. Methodological reference

**Primary reference**

Chen, C.-T. (2000). “Extensions of the TOPSIS for group decision-making under fuzzy environment.” *Fuzzy Sets and Systems*, 114(1), 1–9. DOI: [10.1016/S0165-0114(97)00377-1](https://doi.org/10.1016/S0165-0114(97)00377-1).

The publisher abstract describes the paper as an extension of TOPSIS to a fuzzy environment in which alternative ratings and criterion weights are represented by linguistic terms expressed as triangular fuzzy numbers. It proposes a vertex method for distance between triangular fuzzy numbers and defines a closeness coefficient using distances to both a fuzzy positive-ideal solution (FPIS) and fuzzy negative-ideal solution (FNIS). The record identifies the paper as *Fuzzy Sets and Systems*, volume 114, pages 1–9, published in 2000.

**What this reference supports:** triangular fuzzy ratings and weights, fuzzy decision matrices, FPIS/FNIS comparison, vertex distance, closeness coefficients, and closeness-based ordering.

**What it does not decide for MobilityForge:** which traffic criteria to use, how to elicit project weights, whether observed values should be singleton TFNs or linguistically assessed, how to preserve period/direction, whether LOS is included, or how to handle the unresolved Table 8 clock windows. Those are project decisions.

### Reference-access and equation-audit note

The publisher’s abstract and bibliographic record were accessible, but the full Chen article and its numbered equations were not retrievable here because the ScienceDirect full text returned an access restriction. Therefore, the exact equations below are not presented as fully verified against the original pagination. The audit status is:

| Item | Status in this specification |
|---|---|
| TFN notation and linguistic ratings/weights | Explicitly supported by Chen’s accessible abstract; the candidate five-term scale remains project-specific. |
| Benefit/cost linear normalization | The formulas are the commonly reproduced Chen variant and are corroborated by accessible academic reproductions, but the original equation number/text remains unverified here. |
| Weighted normalized matrix and fuzzy-weight arithmetic | The abstract supports criterion weights and fuzzy decision matrices; the exact multiplication and fuzzy-weight normalization convention remains a project choice pending full-text/reference verification. |
| FPIS/FNIS | The abstract explicitly supports both ideals. Some Chen-style reproductions use fixed `(1,1,1)` and `(0,0,0)` points, but those points are not selected here because crisp weighting scales the attainable matrix values. This specification uses weighted-matrix componentwise maxima/minima as an internally consistent project adaptation. |
| Vertex distance | The displayed Euclidean vertex formula is corroborated by accessible reproductions attributed to Chen; direct full-text confirmation remains unavailable. |
| Closeness coefficient | Chen’s abstract supports a coefficient based on distances to FPIS and FNIS; the displayed ratio is retained as the candidate convention and must be checked against the full paper before implementation. |
| S0–S4 weight scenarios and four-run policy | Entirely project-specific; these are sensitivity scenarios, not claims about Chen’s method or research findings. |

Accessible corroboration consulted: the Chen publisher record ([ScienceDirect abstract](https://www.sciencedirect.com/science/article/pii/S0165011497003771)) and Balioti, V., Tzimopoulos, C., & Evangelides, C. (2018), “Multi-Criteria Decision Making Using TOPSIS Method Under Fuzzy Environment. Application in Spillway Selection,” *Proceedings*, 2(11), 637, DOI [10.3390/proceedings2110637](https://doi.org/10.3390/proceedings2110637), an open methodological reproduction describing Chen’s linear normalization and workflow. Neither substitutes for checking the original full text before implementation.

## 3. Verified alternatives and criteria

### Alternatives

The six alternatives are the Table 8 sections listed in `data/extracted/bbmp_tumkur_midblock_vc_los_table8.csv`:

1. Yeshwanthpur TTMC
2. Yeshwanthpur Skywalk
3. Tumkur Road (Between Gorguntepalya-SRS)
4. Tumkur Road (Between SRS-Jalahalli Junction)
5. Tumkur Road (Between Jalahalli junction-Hesarghatta Junction)
6. Tumkur Road (Between Hesarghatta Junction-Nagasandra)

### Primary criteria

| Criterion | Meaning | Unit | Direction of priority | Status |
|---|---|---|---|---|
| Peak PCU volume | Source-reported peak-hour flow converted to passenger-car units | PCU | Higher congestion demand → higher priority | Verified for both directions and source-labelled morning/evening periods |
| V/C ratio | Source-reported peak-hour flow divided by adjusted capacity | Dimensionless ratio | Higher capacity pressure → higher priority | Verified for both directions and source-labelled morning/evening periods |

The source states that capacity uses road geometry and adjustment factors for conditions such as parking, bus stops, and access points. V/C must therefore be preserved as a source-derived measure with its assumptions.

### LOS treatment

LOS is reported for every Table 8 section, direction, and period, but it is provisionally excluded from the primary fuzzy matrix. The report defines LOS as a qualitative operating-condition measure and states that service measures include density and V/C. Using LOS and V/C as independent weighted criteria could count the same congestion condition twice.

LOS will be retained for:

- descriptive interpretation of the resulting criterion values;
- a consistency check between the source LOS label and the source V/C context; and
- a sensitivity scenario only if the instructor explicitly approves an ordinal fuzzy representation.

Delay, speed, journey time, and intervention cost remain excluded because compatible same-section observations or costs have not been established.

## 4. Period and direction policy

The CSV preserves two periods and two directions for each section. The implementation must retain these dimensions:

| Run identifier | Period | Direction |
|---|---|---|
| `morning_yeshwanthpur` | Source-labelled morning peak | Towards Yeshwanthpur |
| `morning_nagasandra` | Source-labelled morning peak | Towards Nagasandra |
| `evening_yeshwanthpur` | Source-labelled evening peak | Towards Yeshwanthpur |
| `evening_nagasandra` | Source-labelled evening peak | Towards Nagasandra |

These are four proposed independent runs, not four observations to be averaged. A later overall summary requires an approved aggregation policy and must report how it affects results.

### Peak-window evidence constraint

Table 8 (PDF page 46 / printed page 16) labels “Morning Peak” and “Evening Peak” but does not print clock times. Table 7 (PDF page 44 / printed page 14) prints clock windows for related traffic-volume counts, but its PCU values differ from Table 8. The exact Table 7 times must not be transferred to the Table 8 V/C/LOS matrix. The model metadata should therefore retain only the source period labels until a direct cross-reference is found. See `research/phase6_peak_time_evidence_audit.md`.

## 5. Triangular fuzzy numbers and linguistic scales

A triangular fuzzy number (TFN) is written as:

\[
\tilde{x}=(l,m,u), \qquad l\le m\le u,
\]

where `l`, `m`, and `u` are lower, modal, and upper values. Chen’s reference supports linguistic ratings and criterion weights represented by TFNs.

### Candidate linguistic scale (proposal only)

The following normalized five-term scale is a candidate for expert assessments, not a populated research dataset:

| Linguistic term | Candidate TFN |
|---|---|
| Very low | (0.00, 0.00, 0.25) |
| Low | (0.00, 0.25, 0.50) |
| Medium | (0.25, 0.50, 0.75) |
| High | (0.50, 0.75, 1.00) |
| Very high | (0.75, 1.00, 1.00) |

This scale is not yet approved and must not be applied to BBMP values without an agreed elicitation protocol. For measured PCU and V/C values, the least lossy option is to preserve the numerical values and represent each as a degenerate TFN `(x,x,x)` only if the instructor accepts that encoding. A linguistic conversion would require approved thresholds and would discard measurement precision.

## 6. Proposed mathematical workflow

The following is the project protocol to be confirmed against the selected Chen variant before implementation.

### Step 1 — Build one crisp source matrix per run

For each of the four period/direction runs, create a six-by-two matrix:

\[
X=[x_{ij}], \quad i=1,\ldots,6,\; j\in\{\text{PCU},\text{V/C}\}.
\]

Values must be read directly from the source-faithful CSV. No period, direction, section, or cost join is permitted.

### Step 2 — Represent ratings and weights as TFNs

If expert linguistic assessment is approved, map each assessment to the approved TFN scale. If measured values are kept numerical, use only an approved numerical-to-TFN rule; a singleton TFN is the transparent candidate, not a claim of measurement uncertainty.

For `K` decision makers, a project aggregation rule must be approved. A common Chen-style aggregation is to combine lower bounds by minimum, modal values by arithmetic mean, and upper bounds by maximum. This rule is specified here as a candidate protocol, not executed.

### Step 3 — Elicit and normalize criterion weights

Weights must come from an auditable source: instructor-prescribed values, documented expert elicitation, or a justified equal-weight baseline. Belton and Stewart describe weights as an explicit part of an MCDA model whose meaning and elicitation basis must be made clear; weights are not objective properties of the traffic measurements. No research weights currently exist.

After aggregation, normalize the fuzzy weights under the chosen reference’s fuzzy arithmetic so that the criterion-weight system is comparable and its normalization convention is explicit. The implementation must record the raw assessments, TFNs, aggregation rule, and normalized weights. It must not silently substitute equal weights.

#### Provisional weighting policy (two primary criteria)

Equal weighting is the most transparent candidate baseline for the two-criterion design:

\[
w_{\mathrm{PCU}}=0.5,\qquad w_{\mathrm{V/C}}=0.5.
\]

This is a modelling assumption for a baseline, not an objectively established truth and not a finding from the BBMP report. It may be used as the candidate primary scenario only after instructor review and after the project confirms how crisp measured values are represented as TFNs. If fuzzy weights are required, the implementation must state whether this baseline is represented as equal singleton TFNs or by an approved linguistic-weight protocol; those representations must not be conflated.

To expose dependence on the shared traffic-flow signal, the following pre-declared sensitivity scenarios are suitable for the two criteria. They are scenarios for robustness analysis, not approved research weights, and no results have been calculated:

| Scenario | PCU weight | V/C weight | Purpose |
|---|---:|---:|---|
| S0 — equal baseline | 0.50 | 0.50 | Transparent neutral reference |
| S1 — PCU emphasis | 0.70 | 0.30 | Tests greater emphasis on observed demand |
| S2 — V/C emphasis | 0.30 | 0.70 | Tests greater emphasis on capacity pressure |
| S3 — PCU-only robustness check | 1.00 | 0.00 | Shows the single-criterion demand ordering |
| S4 — V/C-only robustness check | 0.00 | 1.00 | Shows the single-criterion capacity-pressure ordering |

Every scenario sums to one. S3 and S4 are robustness checks, not replacements for the mandatory two-criterion Fuzzy TOPSIS model. If an instructor, expert panel, or approved source supplies different weights, those values supersede this illustrative scenario set and must be recorded with their source, date, rationale, and normalization convention. We must not choose a primary weight set because it produces a preferred ordering.

#### Redundancy and correlation check

PCU volume and V/C should not be described as independent criteria without evidence: V/C contains traffic flow in its numerator and also reflects source capacity assumptions. For each of the four runs, the project should therefore:

1. inspect the six paired observations and report a descriptive scatter/table;
2. calculate Pearson and/or Spearman association only as descriptive diagnostics, with the six-alternative sample size stated and no inferential claim;
3. explain that a weak observed association would not prove conceptual independence, while a strong association would reinforce the double-counting concern; and
4. compare the two-criterion result with S3 and S4, without silently replacing the mandated Fuzzy TOPSIS model.

LOS remains validation/interpretation by default. It should not receive a third weight unless a documented source or instructor decision justifies an ordinal fuzzy representation and addresses its relationship with V/C.

### Step 4 — Normalize benefit and cost criteria

Both proposed primary criteria are benefit-to-priority criteria: larger PCU demand and larger V/C indicate greater congestion pressure. Under the Chen linear-scale variant, for a benefit criterion with TFN `x̃ij = (aij, bij, cij)`:

\[
\tilde r_{ij}=\left(\frac{a_{ij}}{c_j^+},\frac{b_{ij}}{c_j^+},\frac{c_{ij}}{c_j^+}\right),
\qquad c_j^+=\max_i c_{ij}.
\]

For a cost criterion:

\[
\tilde r_{ij}=\left(\frac{a_j^-}{c_{ij}},\frac{a_j^-}{b_{ij}},\frac{a_j^-}{a_{ij}}\right),
\qquad a_j^- = \min_i a_{ij}.
\]

No cost criterion is currently in the matrix. These formulas and the selected Chen variant must be checked against the accessible full reference before code implementation.

### Step 5 — Construct the weighted normalized matrix

Multiply each normalized fuzzy criterion value by its normalized fuzzy weight using the approved TFN arithmetic:

\[
\tilde v_{ij}=\tilde r_{ij}\otimes\tilde w_j.
\]

The exact multiplication convention must be documented if all values are non-negative; no implementation choice is hidden here.

### Step 6 — Define FPIS and FNIS

The selected project formulation defines ideals from the weighted normalized matrix, after all criteria have been oriented as benefit-to-priority criteria. For criterion `j`, with weighted TFNs `ṽij = (lij, mij, uij)`:

\[
\tilde v_j^+ = (\max_i l_{ij},\;\max_i m_{ij},\;\max_i u_{ij}),
\qquad
\tilde v_j^- = (\min_i l_{ij},\;\min_i m_{ij},\;\min_i u_{ij}).
\]

Componentwise maxima/minima preserve TFN ordering because every input satisfies `l ≤ m ≤ u`. This keeps FPIS/FNIS on the same scale as the weighted matrix. Fixed `(1,1,1)` and `(0,0,0)` points appear in some Chen-style reproductions, but using them with crisp weighted values would compare each criterion to an unweighted upper bound; they remain an unresolved alternative, not the implemented convention.

### Step 7 — Calculate vertex distances

For two TFNs \(\tilde a=(a_1,a_2,a_3)\) and \(\tilde b=(b_1,b_2,b_3)\), the Chen vertex distance candidate is:

\[
d(\tilde a,\tilde b)=\sqrt{\frac{1}{3}\left[(a_1-b_1)^2+(a_2-b_2)^2+(a_3-b_3)^2\right]}.
\]

For each alternative, calculate distance to FPIS and FNIS across the two criteria using the approved aggregation of criterion distances. The aggregation rule must be stated before implementation.

### Step 8 — Closeness coefficient and ranking

For alternative `i`, the candidate closeness coefficient is:

\[
CC_i=\frac{D_i^-}{D_i^+ + D_i^-},
\]

where `Dᵢ⁺` is distance to FPIS and `Dᵢ⁻` is distance to FNIS. Larger `CCᵢ` indicates greater relative closeness to the positive ideal and therefore higher priority under the benefit-to-priority orientation.

No `CC` or ranking has been generated.

## 7. Sensitivity and validation plan

Before reporting any result:

- validate six expected section mappings, two criteria, four run identifiers, units, source page, and non-missing numeric values;
- independently reproduce one complete alternative/run calculation by hand;
- verify TFN arithmetic, normalization, FPIS/FNIS construction, distance, and closeness equations against the approved reference;
- compare results under the declared S0–S4 scenarios (or an approved replacement set), reporting whether each of the four separate runs is stable; sensitivity analysis is a robustness exercise, not evidence that any one scenario is true;
- compare all four period/direction runs without averaging them silently;
- test whether rankings change when LOS is used only for validation versus an explicitly approved ordinal scenario;
- check sensitivity to approved TFN scale choices and expert aggregation rules;
- for the six-alternative samples, report correlation diagnostics descriptively and avoid inferential claims about independence;
- report ties, instability, unresolved windows, and missing evidence honestly;
- ensure no interface labels provisional outputs as validated intervention benefits or accuracy.

## 8. Project decisions versus literature-supported definitions

**Literature-supported by Chen (2000):** TFN linguistic ratings and weights, fuzzy decision matrix, FPIS/FNIS comparison, vertex distance, closeness coefficient, and closeness-based ranking.

**MCDA weighting and sensitivity guidance:** Belton and Stewart (2002) treat criteria weights as explicit modelling inputs whose interpretation and elicitation basis should be documented. Triantaphyllou (2000), including the book chapter “A Sensitivity Analysis Approach for MCDM Methods,” provides a methodological basis for examining how MCDM conclusions respond to changes in model inputs. These references support documenting and testing weights; they do not select MobilityForge’s weights.

**Project decisions still requiring approval:**

- singleton TFNs for measured PCU/V/C versus an approved linguistic conversion;
- the exact linguistic scale and TFNs;
- whether the S0 equal-weight scenario is accepted as the primary baseline, or whether an approved elicitation supplies the primary fuzzy weights;
- weight elicitation, aggregation, and normalization;
- whether to use Chen’s linear normalization and ideal points exactly as written above;
- how distances across the two criteria are aggregated;
- whether LOS remains validation-only;
- four separate period/direction runs versus any later aggregation;
- treatment of unresolved Table 8 clock windows;
- acceptable worked example and independent validation standard.

## 9. Current implementation gate

**CONDITIONAL GO — methodology specification only.** Fuzzy TOPSIS is now the required method, but implementation of final rankings remains gated by approval of the TFN representation, linguistic scale, weights, normalization convention, distance aggregation, and period/direction policy. The source CSV and existing backend validation layer remain authoritative; no research values should be overwritten or transformed silently.

## 10. Mathematical primitives implemented (no research run)

`backend/mobility_engine/fuzzy_topsis.py` now contains independently tested, dataset-independent primitives for the following documented conventions:

- immutable non-negative TFNs with finite ordered components and non-negative scalar multiplication;
- Chen-style linear benefit and cost normalization;
- explicit **crisp** criterion weights that are finite, non-negative, and sum exactly to one, applied to normalized TFNs;
- weighted-matrix componentwise FPIS/FNIS maxima and minima;
- the Euclidean vertex distance;
- additive distance aggregation across criteria and the candidate closeness coefficient; and
- deterministic descending coefficient ordering with stable index tie handling.

The implementation deliberately does not infer fuzzy weights from crisp equal weights, elicit linguistic ratings, aggregate periods/directions, read the research CSV, or publish rankings. Crisp weights were selected for this primitive layer because the project has not approved a fuzzy-weight elicitation and normalization protocol. Weighted-matrix ideals and additive distance aggregation are explicit project adaptations; they must be reviewed against the full Chen text before a research run.

Tests use labelled synthetic TFNs only and cover invalid components, arithmetic, benefit/cost normalization, zero denominators, matrix dimensions, weights, ideal points, distance, closeness, ties, and boundary validation. The four source-labelled period/direction runs and the Table 8 peak-window evidence gap are unchanged.

## 11. Phase 9 execution boundary

The provisional execution service accepts exactly one source-labelled period
and direction, the six expected alternatives, and explicit crisp `pcu` and
`vc` weights that sum to one. It converts the two measured criteria to
singleton TFNs, applies the tested benefit normalization, weighted-matrix
componentwise ideals, vertex distance, additive criterion distances, and
closeness coefficients, then returns source values and all intermediate values
alongside a deterministic rank. The API requires an explicit acknowledgement
that the output is provisional.

This endpoint is an execution and transparency aid, not a validated research
result. It does not combine the four runs, infer missing peak windows, use LOS
as a scored criterion, select default weights, or establish intervention
efficacy. Instructor approval and the unresolved Table 8 clock-time evidence
remain gates before any ranking is reported as a research conclusion.

## Reference

Chen, C.-T. (2000). “Extensions of the TOPSIS for group decision-making under fuzzy environment.” *Fuzzy Sets and Systems*, 114(1), 1–9. https://doi.org/10.1016/S0165-0114(97)00377-1

Belton, V., & Stewart, T. J. (2002). *Multiple Criteria Decision Analysis: An Integrated Approach*. Springer. https://doi.org/10.1007/978-1-4615-1495-4

Triantaphyllou, E. (2000). *Multi-Criteria Decision Making Methods: A Comparative Study*. Springer, Applied Optimization, vol. 44. https://doi.org/10.1007/978-1-4757-3157-6. See especially Chapter 8, “A Sensitivity Analysis Approach for MCDM Methods.”

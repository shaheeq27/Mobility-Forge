# Phase 4 — Final Model Design

**Project:** MobilityForge — Building Better Mobility Systems  
**Assessment date:** 2026-10-22  
**Purpose:** specify the smallest transparent model that the verified evidence can support.

## Executive summary

The verified common alternative set is the six Tumkur Road mid-block sections in Table 8 of the BBMP report (PDF page 46). The extracted table contains complete directional morning and evening peak PCU volumes, V/C ratios, and LOS classifications for all six sections.

The seven citywide intersections have volume observations only for the purposes of a multi-criteria model. The five corridor intersection rows are a separate alternative set. Link-level speed and delay cannot be added to the six sections without a source-backed spatial and period crosswalk, and no comparable intervention costs are available.

The proposed minimal model therefore uses the six road sections and two quantitative criteria: peak PCU volume and V/C. LOS is retained for interpretation and validation, not automatically as a third weighted criterion. Because V/C is derived from flow and capacity, the two quantitative criteria are informative but not independent; any model must disclose and test the risk of double-counting congestion.

**Provisional recommendation: CONDITIONAL GO.** A transparent weighted-sum baseline is the simplest candidate method. Fuzzy TOPSIS should be implemented only if the instructor requires or approves it and specifies the methodological reference and variant.

## Verified data and scope

The following six alternatives and values were checked directly against `data/extracted/bbmp_tumkur_midblock_vc_los_table8.csv`, which identifies source page 46:

| Section | Morning PCU (Yeshwanthpur / Nagasandra) | Morning V/C | Morning LOS | Evening PCU (Yeshwanthpur / Nagasandra) | Evening V/C | Evening LOS |
|---|---:|---:|---|---:|---:|---|
| Yeshwanthpur TTMC | 3407 / 3285 | 1.26 / 1.22 | F / F | 3808 / 3362 | 1.41 / 1.25 | F / F |
| Yeshwanthpur Skywalk | 3668 / 4461 | 1.09 / 1.59 | F / F | 3725 / 4163 | 1.11 / 1.49 | F / F |
| Gorguntepalya–SRS | 5362 / 5496 | 1.31 / 1.35 | F / F | 5219 / 6071 | 1.28 / 1.49 | F / F |
| SRS–Jalahalli Junction | 3728 / 2601 | 0.91 / 0.64 | E / C | 3897 / 2502 | 0.96 / 0.61 | E / C |
| Jalahalli Junction–Hesarghatta Junction | 4451 / 2214 | 1.09 / 0.54 | F / C | 4843 / 2847 | 1.19 / 0.70 | F / C |
| Hesarghatta Junction–Nagasandra | 2938 / 2097 | 0.43 / 0.31 | B / B | 3752 / 2713 | 0.55 / 0.40 | C / B |

Verified source context:

- The report’s Table 8 defines the directional peak PCU volume, V/C, and LOS fields (PDF page 46; summarized in `research/phase2c_extraction_compatibility_audit.md`).
- The report states that capacity includes adjustments for on-street parking, bus stops, and access points. V/C is therefore a source-derived measure with assumptions, not an independently measured raw field.
- Morning and evening windows are reported by the source, but exact windows can vary by survey location. They must remain source-labelled.
- The PDF is preserved at `data/raw/bbmp-ctmp-tumkur-road-old-madras-road.pdf`; its verified SHA-256 is `c6a0b8b0695a087ba65f65b2f9ffe63c7180b2f4de3ab63f3bc74f6f65d0f8fa`.

The seven Table 158 intersections (PDF page 546) have daily, morning, and evening vehicle/PCU volumes but no verified matching V/C, LOS, delay, speed, or cost. The five Table 10 corridor intersections (PDF page 48) are a different five-location set. Neither set is the proposed model scope.

## Proposed model-specification table

| Criterion | Definition | Unit | Time period | Benefit/cost direction | Source | Missing-data handling | Justification |
|---|---|---|---|---|---|---|---|
| Peak PCU volume | Reported peak-hour traffic flow converted to passenger-car units | PCU per peak hour | Morning and evening; each source-labelled directional period | Higher congestion demand is treated as higher screening priority; this is a **benefit-to-priority**, not a beneficial outcome | BBMP Table 8, PDF p.46; extracted CSV | No imputation or interpolation. If a required section/direction/period is missing or invalid, stop that run and document the gap; do not silently substitute another period or direction | Directly available for every proposed alternative, period, and direction |
| V/C ratio | Peak-hour flow divided by source-estimated capacity | Dimensionless ratio | Morning and evening; each direction | Higher capacity pressure is higher screening priority | BBMP Table 8, PDF p.46; capacity explanation p.46 | Preserve the source value and capacity assumptions. Do not recompute or repair missing V/C without the original inputs and approved method | Directly available for every proposed alternative, period, and direction; operationally meaningful for congestion screening |
| LOS (provisional interpretation field) | Source categorical service-level classification associated with operating conditions | Letter category A–F | Morning and evening; each direction | Worse service category indicates greater concern, but no separate model weight by default | BBMP Table 8, PDF p.46 | Preserve missing/invalid labels as unresolved. Do not convert categories to invented numeric scores | Provides an interpretable validation/context label and helps communicate V/C results without automatically duplicating it as a criterion |

Excluded from the initial specification:

- **Delay, journey time, and speed:** present in link-level Tables 11–18 (PDF pages 49–57), but not proven to correspond one-to-one with all six Table 8 sections.
- **Intervention cost:** no comparable alternative-level cost field was verified.
- **Intersection alternatives:** insufficient common criteria for the proposed multi-criteria scope.

## Criterion redundancy assessment

Peak PCU volume and V/C provide related but not identical information:

- PCU volume describes observed demand during a stated peak period.
- V/C describes demand relative to the source’s estimated capacity, so it reflects both flow and capacity assumptions.

Using both may be useful because two sections with similar PCU flow can have different capacity pressure, and two sections with similar V/C can have different absolute demand. However, V/C contains the traffic-flow numerator, so the criteria are statistically and conceptually dependent. Assigning independent weights can double-count congestion demand.

The model specification should therefore:

1. disclose the dependence;
2. retain the source capacity assumptions;
3. treat LOS as interpretation-only by default; and
4. compare a volume-only or V/C-focused baseline with the two-criterion version during sensitivity analysis, without claiming independence.

No such comparison or score is calculated in Phase 4.

## Candidate method comparison

| Method | Strengths for this evidence | Limitations / risks | Status |
|---|---|---|---|
| Transparent weighted sum | Easy to explain and audit; works with two quantitative criteria; makes direction and weights explicit; straightforward to reproduce in a worked example | Requires normalisation and weights; sensitive to scale and double-counting; does not itself express uncertainty | Preferred provisional baseline |
| Fuzzy TOPSIS | Matches the proposed fuzzy-MCDM academic direction; represents uncertain linguistic inputs if those inputs are genuinely justified; provides ideal-solution distances | More assumptions and implementation choices; triangular fuzzy numbers and weights would be invented if not supported by evidence; multiple incompatible variants exist; harder to validate with only two related quantitative fields | Candidate only if instructor approves a specific reference/variant |
| LOS-only ordinal ranking | Very simple communication and source-aligned categories | Discards quantitative variation; LOS is related to V/C; categorical conversion rules could create arbitrary ties | Interpretation/validation, not preferred core method |

The evidence does not require a complex method. A weighted sum is the simplest transparent baseline. If the assignment explicitly requires fuzzy decision-making, Fuzzy TOPSIS may be a second implementation or comparison, but only after instructor approval and selection of one consistent methodological reference.

## Provisional model recommendation

**Provisional model:** a six-section, period-specific weighted-sum screening model using peak PCU volume and V/C, with LOS retained as a non-weighted interpretation field.

Design boundaries:

- Keep morning and evening conditions separate initially; do not silently average them.
- Preserve both directions initially, or obtain approval for one documented direction-aggregation rule.
- Do not join speed/delay links to sections without a documented crosswalk.
- Do not use intervention cost without comparable source data.
- Do not describe the output as intervention benefit, cost-effectiveness, or causal impact. It is a congestion-priority screening result.
- Keep Fuzzy TOPSIS unimplemented until its approval, reference, fuzzy-number construction, and weight elicitation are confirmed.

## Weighting plan without invented values

No weights are assigned in this document. Once the method is approved, weighting should be documented rather than hidden in code:

1. Obtain instructor/researcher agreement on whether volume and V/C are both retained despite dependence.
2. Choose an auditable elicitation basis: equal-weight baseline, documented expert judgement, or a literature/assignment-prescribed scheme. Equal weighting may be a comparison baseline, not an asserted truth.
3. Record the rationale, date, participants or reference, and any scale used.
4. Run sensitivity checks across a pre-declared range or alternative defensible weight sets.
5. Report whether priority ordering is stable, changes materially, or is indeterminate. Do not select weights because they produce a preferred ranking.

If Fuzzy TOPSIS is required, the same discipline applies to fuzzy weights and linguistic terms: the source and elicitation procedure must be documented before any numbers are created.

## Validation and sensitivity plan

Before presenting model results, the implementation should support:

- **Input validation:** confirm six expected alternatives, required source fields, valid numeric V/C and PCU values, valid LOS labels, and explicit period/direction identifiers.
- **Traceability check:** every returned value should point to the source CSV row and BBMP table/page.
- **Manual worked example:** independently reproduce one small case by hand using the approved equations and inputs.
- **Method check:** compare implementation output with the worked example; test benefit/cost orientation and missing-data behavior.
- **Redundancy check:** compare the two-criterion design with a V/C-focused or volume-focused variant to show dependence effects.
- **Period check:** keep morning and evening outputs separate and compare ordering stability only after the period definitions are documented.
- **Direction check:** test the approved direction rule or report direction-specific outputs.
- **Weight sensitivity:** vary only approved, defensible weight sets and record changes in ordering.
- **Input sensitivity:** perturbations may be considered only if an evidence-based uncertainty rule is supplied; do not invent error margins.
- **No-claim check:** ensure the UI/report does not call a screening score a validated intervention impact or accuracy percentage.

These are planned checks, not completed calculations.

## Unresolved decisions requiring approval or additional evidence

- Is the six-road-section scope formally accepted as the primary research scope?
- Is a weighted-sum baseline acceptable, or is Fuzzy TOPSIS required?
- If Fuzzy TOPSIS is required, which single methodological reference and variant governs normalisation, fuzzy numbers, ideal solutions, distances, and weights?
- Should volume and V/C both be retained, given the shared flow numerator?
- Should LOS remain interpretation-only, or must it be modelled as an ordinal criterion?
- Should morning and evening be separate model conditions or be combined using an approved rule?
- Should both directions remain separate, or how should a single direction-aggregation rule be justified?
- Are the source survey dates and protocols sufficiently comparable across Table 8 rows?
- Is it acceptable to proceed without intervention-cost data and direct benefit estimates?
- What validation example and independent checking standard will the instructor accept?
- What reuse/licensing conditions apply to the preserved BBMP report and extracted values?

## Recommendation

**CONDITIONAL GO.** The evidence is adequate to specify and later implement a small, transparent six-road-section screening model using peak PCU volume and V/C, with LOS for interpretation. It is not adequate for an unrestricted multi-criteria intervention ranking that adds speed, delay, cost, or unsupported joins. Implementation should begin only after the instructor resolves the method, scope, direction, period, redundancy, and validation decisions above.

## Checks performed

- Read the six requested research documents.
- Inspected `data/extracted/bbmp_tumkur_midblock_vc_los_table8.csv` directly and verified all six alternatives’ morning/evening directional PCU, V/C, and LOS values.
- Cross-checked source table/page references against the Phase 2C and Phase 3 records and the preserved BBMP PDF reference.
- Did not calculate weights, scores, fuzzy numbers, or rankings.
- Created only this new research document; no existing research file, CSV, PDF, frontend, or backend file was modified.
- Nothing was staged, committed, or pushed.


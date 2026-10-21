# Phase 3 — Data Readiness and Research Design

**Project:** MobilityForge — Building Better Mobility Systems<br>
**Assessment date:** 2026-10-22<br>
**Purpose:** determine whether the verified evidence supports a small, defensible multi-criteria decision-support model.

## Executive summary

The preserved BBMP report is suitable for a **small conditional road-section screening model**, not yet for the original broad intersection-intervention claim. The strongest common alternative set is the six Tumkur Road mid-block sections in Table 8 (PDF page 46). For every section, the source reports directional morning and evening peak PCU volume, V/C ratio, and LOS.

The seven citywide intersections in Table 158 (PDF page 546) have daily, morning, and evening vehicle/PCU volumes, but do not have matching delay, speed, V/C, LOS, or cost observations in the verified extracts. They therefore support descriptive volume analysis, not a defensible multi-criteria model without additional evidence.

The recommended smallest model is conditional: use peak-period PCU volume and V/C for the six road sections, retain LOS for interpretation/validation rather than automatically weighting it, and keep morning/evening and direction handling explicit. This is not approval of Fuzzy TOPSIS, and it does not justify adding link-level delay/speed or intervention cost.

**Recommendation: CONDITIONAL GO** to model design and implementation only after instructor confirmation of scope, method, direction/period handling, and the treatment of V/C and LOS.

## Evidence reviewed

- [`dataset_audit.md`](dataset_audit.md)
- [`phase2b_targeted_discovery.md`](phase2b_targeted_discovery.md)
- [`phase2c_extraction_compatibility_audit.md`](phase2c_extraction_compatibility_audit.md)
- [`phase2d_research_design.md`](phase2d_research_design.md)
- [`source_register.md`](source_register.md)
- [`bbmp_intersection_volume_table158.csv`](../data/extracted/bbmp_intersection_volume_table158.csv)
- [`bbmp_tumkur_intersection_volume_table10.csv`](../data/extracted/bbmp_tumkur_intersection_volume_table10.csv)
- [`bbmp_tumkur_midblock_vc_los_table8.csv`](../data/extracted/bbmp_tumkur_midblock_vc_los_table8.csv)
- Preserved source: `data/raw/bbmp-ctmp-tumkur-road-old-madras-road.pdf`, SHA-256 `c6a0b8b0695a087ba65f65b2f9ffe63c7180b2f4de3ab63f3bc74f6f65d0f8fa`.

The PDF remains accessible, unencrypted, and 628 pages. No source file or extracted CSV was modified.

## Alternatives and available evidence

### BBMP Table 8 — six road-section alternatives

Source: PDF page 46; source-faithful extract in `data/extracted/bbmp_tumkur_midblock_vc_los_table8.csv`.

| Alternative | Measured criteria | Units / periods | Coverage |
|---|---|---|---|
| Yeshwanthpur TTMC | PCU volume, V/C, LOS | Directional morning and evening peak; PCU, ratio, A–F | Complete in extracted table |
| Yeshwanthpur Skywalk | PCU volume, V/C, LOS | Directional morning and evening peak; PCU, ratio, A–F | Complete |
| Tumkur Road (Gorguntepalya–SRS) | PCU volume, V/C, LOS | Directional morning and evening peak; PCU, ratio, A–F | Complete |
| Tumkur Road (SRS–Jalahalli Junction) | PCU volume, V/C, LOS | Directional morning and evening peak; PCU, ratio, A–F | Complete |
| Tumkur Road (Jalahalli Junction–Hesarghatta Junction) | PCU volume, V/C, LOS | Directional morning and evening peak; PCU, ratio, A–F | Complete |
| Tumkur Road (Hesarghatta Junction–Nagasandra) | PCU volume, V/C, LOS | Directional morning and evening peak; PCU, ratio, A–F | Complete |

The report also describes source capacity adjustments for parking, bus stops, and access points. V/C is therefore a source-derived measure, not an independently measured raw field.

### BBMP Table 158 — seven citywide intersection alternatives

Source: PDF page 546; extract in `data/extracted/bbmp_intersection_volume_table158.csv`.

| Alternatives | Measured criteria | Units / periods | Coverage |
|---|---|---|---|
| CN Rao underpass Junction; Bangalore Cantt Junction; Basaveshwara circle; KR Circle; Cubbon Park UB City signal; Shoolay Circle; Lalbagh Chowk | Daily volume, morning peak volume, evening peak volume | Vehicles and PCUs; daily totals; one reported AM and PM window per location | Complete for volume only |

The exact peak windows differ by location. No same-alternative delay, journey time, speed, V/C, LOS, or intervention-cost field was verified.

### BBMP Table 10 — five Tumkur corridor intersection alternatives

Source: PDF page 48; extract in `data/extracted/bbmp_tumkur_intersection_volume_table10.csv`.

| Alternatives | Measured criteria | Units / periods | Coverage |
|---|---|---|---|
| Gorgunte Palya Junction–Near Taj Vivanta; 100 Ft Ring Road Junction; SRS Junction; Jalahalli Junction; Hesarghatta Main Road Junction | Peak-hour traffic volume | Vehicles and PCUs; one morning and one evening window per location | Complete for volume only |

This is a distinct five-location corridor set. It must not be merged with the seven Table 158 intersections or the six Table 8 sections.

### Other discovered candidate alternatives

- **CTTP:** 24 mid-block locations and 16 selected speed/delay routes. The inspected chapter reports 12-hour vehicles/PCUs, peak-window labels, and describes AM/PM/off-peak route runs, but does not expose a complete location-by-period delay matrix. These are road-link/route alternatives, not intersections.
- **BMD-45:** anonymised CCTV images and vehicle annotations from junction and mid-block views. No verified location-level volume, speed, delay, capacity, or congestion matrix exists in the dataset card.
- **Traffic Monitor Lizard:** predetermined routes with date/time, duration, distance, and derived speed from Google Maps estimates. These are route alternatives and cannot be silently joined to BBMP sections.
- **BTP signal-timing PDF:** metadata only; contents and measurements were not retrieved. No ranking criterion is available.

## Criteria compatibility table

| Criterion | Operational definition | Unit / classification | Preferable direction for congestion intervention | Same alternatives and compatible periods? | Source evidence |
|---|---|---|---|---|---|
| Peak traffic volume | Traffic flow reported as vehicles or passenger-car units during a stated peak window | Vehicles or PCU; peak hour | Higher value generally indicates greater demand/priority | **Yes for six sections** as directional AM/PM PCU; **yes for seven intersections** as volume only | Table 8 p.46; Table 10 p.48; Table 158 p.546 |
| V/C ratio | Peak-hour flow divided by source-estimated capacity | Ratio | Higher value indicates greater capacity pressure | **Yes for six sections**, directional AM/PM | Table 8 p.46; capacity assumptions p.46 |
| LOS | Source service-level category associated with operating conditions | A–F categorical scale | Worse service (for example F) suggests greater intervention priority | **Yes for six sections**, directional AM/PM; unavailable for seven intersections | Table 8 p.46 |
| Delay | Link delay during a surveyed movement | Seconds | Higher delay suggests greater priority | **No verified compatible join** to all six sections or seven intersections | Tables 11–18, pp.49–57 |
| Journey time | Total link travel time, including delay | Seconds | Higher time suggests greater priority | **No verified compatible join** | Tables 11–18, pp.49–57 |
| Journey/running speed | Link speed based on total or moving time | km/h | Lower speed or greater slowdown suggests greater priority | **No verified compatible join** | Tables 11–18, pp.49–57 |
| Intervention cost | Comparable cost for an intervention applied to the same alternative | Currency, if sourced | Lower cost may be preferable, depending on objective | **Unavailable** | No compatible cost field verified |

## Missing data, incompatibilities, and unsupported assumptions

1. The seven intersections have no verified same-location delay, speed, V/C, LOS, or cost values.
2. The five corridor intersections, seven citywide intersections, and six road sections are different alternative sets.
3. Speed/delay tables are link-wise, directional, vehicle-specific, and period-specific. A nearby named junction is not proof that a link is the same as a Table 8 section.
4. Morning and evening windows vary by location. They must remain source-labelled; they must not be silently treated as simultaneous or identical periods.
5. The survey collection date and exact comparability of all bundled report sections remain unresolved.
6. Direction handling is unresolved: the Table 8 rows contain two directional observations per period, but no approved aggregation rule exists.
7. V/C depends on source capacity assumptions and is not independent of traffic volume.
8. LOS is closely related to V/C and may duplicate the same congestion signal if both receive separate weights.
9. Intervention costs, benefits, and feasibility constraints are absent for the candidate alternatives.
10. No weights, fuzzy numbers, scores, rankings, imputations, or cross-dataset joins are justified at this stage.

## Can volume and V/C support a small initial model?

**Yes, conditionally, for the six road sections.** Both criteria are present for every section in both reported peak periods and both directions. This supports a deliberately small congestion-screening model if it is described as prioritising observed demand and capacity pressure—not as estimating intervention benefit, cost-effectiveness, or causal impact.

The relationship between the criteria must be made explicit. V/C is calculated from flow and capacity, so volume and V/C are not fully independent evidence. A later analysis should test whether using both materially double-counts demand, document the capacity assumptions, and avoid presenting the two criteria as unrelated measurements.

For the seven intersections, volume alone is available. A two-criterion model cannot be defended for that scope from the current evidence.

## LOS: criterion or interpretation?

The recommended default is to use **V/C as the continuous congestion criterion and LOS for interpretation/validation only**. This preserves the source’s categorical service information without assigning a second weight to a measure that is closely tied to V/C.

LOS could become an explicit ordinal criterion only if the instructor requires it and the methodology documents its scale, direction, dependence on V/C, and sensitivity treatment. It should not be added automatically to a V/C-weighted model.

## Recommended minimal model

Subject to approval, the smallest defensible model is:

- **Alternatives:** six Table 8 Tumkur Road sections.
- **Core criteria:** directional peak PCU volume and V/C ratio.
- **Conditions:** morning and evening kept separate unless an approved aggregation rule is supplied.
- **Direction:** report both directions separately initially, or obtain approval for one documented aggregation rule before combining them.
- **LOS:** interpretation/validation field, not an additional weighted criterion by default.
- **Delay, journey time, speed:** excluded until a source-backed link-to-section crosswalk and period match are established.
- **Cost:** excluded until comparable, traceable alternative-level costs are found.

This is a design recommendation, not a calculated model. Fuzzy TOPSIS remains unapproved and no fuzzy representation, criterion weights, or ideal solutions should be implemented yet.

## Research decisions requiring instructor confirmation

- Is the six-road-section scope acceptable as the primary scope, with the seven intersections retained only for descriptive context?
- Is Fuzzy TOPSIS required or permitted, and which single methodological reference/variant must be followed?
- May morning and evening be modelled as separate conditions rather than collapsed into one matrix?
- Should the two directions remain separate alternatives/observations, or is a specific aggregation rule required?
- Is it acceptable to use volume and V/C despite their dependence, with LOS used for interpretation only?
- Is a congestion-screening model acceptable without intervention cost and without direct benefit estimates?
- What independent worked example and validation standard must be satisfied before results are presented?

## Recommendation

**CONDITIONAL GO.** Proceed to model implementation planning only after the instructor confirms the scope and methodology decisions above. The available data support a small, transparent six-road-section screening model using volume and V/C, but do not support an unrestricted fuzzy intervention-ranking claim. If the instructor requires intersection alternatives or rejects the reduced criteria set, the correct decision is to pause implementation and obtain additional compatible evidence rather than invent or silently join measurements.

## Checks performed

- Read all five existing research Markdown documents named in the Phase 3 request.
- Inspected all files under `data/extracted/`.
- Confirmed the preserved PDF is accessible, unencrypted, 628 pages, and matches SHA-256 `c6a0b8b0695a087ba65f65b2f9ffe63c7180b2f4de3ab63f3bc74f6f65d0f8fa`.
- Cross-checked alternative names, criteria, units, periods, and source pages against the existing extracts and Phase 2 audit records.
- Created only this research document; no original source, CSV, frontend, backend, rankings, or model code was modified.
- Nothing was staged, committed, or pushed.

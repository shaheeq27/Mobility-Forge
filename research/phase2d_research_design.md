# Phase 2D — Research Scope and Methodology Decision

**Project:** MobilityForge — Building Better Mobility Systems<br>
**Academic topic:** *A Fuzzy Multi-Criteria Decision Support Framework for Prioritising Urban Traffic Congestion Interventions*<br>
**Decision date:** 2026-10-18

## 1. Evidence reviewed

This decision uses the verified BBMP/ Government of Karnataka feasibility report and the Phase 2C source-faithful extracts. The raw PDF is preserved at `data/raw/bbmp-ctmp-tumkur-road-old-madras-road.pdf`; its recorded SHA-256 is `c6a0b8b0695a087ba65f65b2f9ffe63c7180b2f4de3ab63f3bc74f6f65d0f8fa`.

Reviewed artifacts:

- [`phase2c_extraction_compatibility_audit.md`](phase2c_extraction_compatibility_audit.md)
- [`source_register.md`](source_register.md)
- [`bbmp_intersection_volume_table158.csv`](../data/extracted/bbmp_intersection_volume_table158.csv)
- [`bbmp_tumkur_intersection_volume_table10.csv`](../data/extracted/bbmp_tumkur_intersection_volume_table10.csv)
- [`bbmp_tumkur_midblock_vc_los_table8.csv`](../data/extracted/bbmp_tumkur_midblock_vc_los_table8.csv)

No project-specific instructor method sheet or assignment rubric was present in the repository. Therefore, Fuzzy TOPSIS remains a proposal requiring instructor confirmation.

## 2. Candidate scope comparison

### Scope A — Seven citywide intersections

The alternatives are the seven named locations in Table 158 (PDF page 546): CN Rao underpass Junction, Bangalore Cantt Junction, Basaveshwara circle, KR Circle, Cubbon Park UB City signal, Shoolay Circle, and Lalbagh Chowk.

Available evidence for every alternative:

- Daily vehicles and daily PCUs.
- One reported morning peak period with vehicles and PCUs.
- One reported evening peak period with vehicles and PCUs.

The table supports comparable volume observations across the seven rows, although peak windows vary by location. It does not provide same-alternative delay, journey time, speed, V/C, LOS, or intervention cost. The Table 10 five-intersection corridor dataset is a different alternative set and cannot be joined to these seven rows without additional evidence.

**Assessment:** strong for descriptive daily/AM/PM volume comparison; insufficiently multi-criteria for the proposed intervention-prioritisation study unless additional intersection-level criteria are obtained or the research question is narrowed.

### Scope B — Six Tumkur Road sections

The alternatives are the six Table 8 mid-block sections: Yeshwanthpur TTMC; Yeshwanthpur Skywalk; Gorguntepalya–SRS; SRS–Jalahalli Junction; Jalahalli Junction–Hesarghatta Junction; and Hesarghatta Junction–Nagasandra.

Available evidence for every alternative and both reported directions/periods:

- Peak-hour PCU volume.
- V/C ratio.
- LOS classification.
- Morning and evening peak observations.

The report also contains corridor link-level bus and car delay/speed tables. However, those links are not demonstrated to be a one-to-one segmentation of the six Table 8 sections. They must not be joined as section criteria until a source-backed spatial crosswalk and matching survey-period evidence are obtained.

**Assessment:** the stronger candidate for a defensible road-section MCDA because volume, V/C, and LOS cover all six alternatives in the same corridor. It still requires care about criterion redundancy and should not claim that link-level delay/speed has been aligned.

## 3. Criteria feasibility matrix

| Criterion | Operational definition and unit | Direction | Seven intersections | Six road sections | Evidence and limitations |
|---|---|---:|---|---|---|
| Traffic volume | Counted vehicles or passenger-car units (PCUs); daily total and peak-hour values | Higher congestion priority | **Available** for all seven, daily/AM/PM | **Available** for all six, directional AM/PM peak PCUs | Units and windows are reported in source tables. Vehicle counts and PCUs are related representations, not independent criteria. |
| V/C ratio | Peak-hour traffic volume divided by source-estimated capacity | Higher priority | **Unavailable** | **Available** for all six, by direction and period | Capacity uses source adjustment factors for parking, bus stops, and access. It is a derived source output, not an independent raw observation. |
| LOS | Source categorical service classification (A–F) associated with V/C conditions | Lower LOS letter / worse service implies higher priority | **Unavailable** | **Available** for all six, by direction and period | LOS is a classification derived from service conditions and is closely related to V/C; using both as separate weighted criteria may double-count congestion. |
| Delay | Link delay in seconds | Higher priority | **Unavailable for the same seven alternatives** | **Not yet compatible**; link-wise tables exist but section mapping is unverified | Bus/car, direction, route link, and period are explicit. No unsupported link-to-section join is permitted. |
| Journey time | Link journey time in seconds | Higher priority | **Unavailable for the same seven alternatives** | **Not yet compatible** for the six sections | Link-level, not alternative-level; includes delay according to the report’s definition. |
| Journey/running speed | Link speed in km/h | Lower speed / greater slowdown implies higher priority | **Unavailable for the same seven alternatives** | **Not yet compatible** for the six sections | Vehicle type, direction, link sequence, and period vary across tables. |
| Intervention cost | Comparable cost per alternative and intervention | Lower cost may be preferable, subject to objective | **Unavailable** | **Unavailable** | No verified location-specific cost observations were found. Exclude unless a credible compatible source is obtained. |

### Redundancy decision: V/C and LOS

V/C and LOS should not automatically be treated as two independent weighted criteria. In the report, LOS is assigned alongside the V/C assessment and both express service congestion. A later model should either:

1. use V/C as the continuous congestion criterion and retain LOS for interpretation/validation; or
2. use LOS as an ordinal criterion only if the instructor explicitly requires categorical service quality and the dependence is acknowledged.

The project should not assign separate weights to both without a documented redundancy rationale or an approved sensitivity analysis.

## 4. Time-aware extension feasibility

The evidence supports a limited, honest time-aware comparison:

- **Seven intersections:** daily, morning, and evening vehicle/PCU values are available for every Table 158 alternative. The exact peak window varies by location, so comparisons must preserve those windows and must not be described as simultaneous citywide measurements.
- **Six road sections:** directional morning and evening PCU volume, V/C, and LOS are available for every section. This is the most complete period-matched evidence in the current extracts.
- **Delay, journey time, and speed:** morning/evening tables exist for bus and car links, but their alternative mapping and exact survey comparability are unresolved. No period value should be inferred for a section from a nearby link.

Recommended extension definition, conditional on selecting road sections: compare a baseline model using the report’s selected peak-period representation with a time-aware analysis that keeps morning and evening observations separate, reports period-specific priorities, and examines whether section ordering is stable across periods. This is a proposed design, not a result. It requires an explicit rule for directional aggregation and confirmation that the survey protocols are comparable.

## 5. Recommended research design

### Recommendation

Use the **six Tumkur Road sections as the primary MCDA scope**, conditional on instructor approval and a final protocol that treats the source’s V/C/LOS definitions correctly. This scope has the best evidence coverage for a multi-criteria study and supports a meaningful morning-versus-evening comparison without pretending that link-level speed/delay has been aligned.

Retain the seven-intersection table as a secondary descriptive analysis or as a fallback if the instructor requires intersection alternatives. If forced to use the seven intersections, the defensible initial question is traffic-volume prioritisation, not a full multi-criteria intervention ranking, unless additional same-location criteria are found.

### Candidate research question

> How can verified peak-period traffic volume, capacity utilisation, and service-level evidence be used to prioritise Bengaluru urban road sections for congestion intervention, and how does separating morning and evening observations affect the resulting priority ordering?

This wording does not claim that the time-aware extension improves decisions; it asks whether and how the ordering changes.

### Proposed baseline and extension

- **Baseline:** one clearly documented road-section decision matrix using criteria supported for all six sections and one stated period/aggregation rule.
- **Time-aware extension:** retain morning and evening observations as separate comparable conditions, report period-specific outputs, and evaluate ranking stability/change across periods.
- **Delay/speed:** remain excluded from the core matrix until a defensible section crosswalk is established.
- **Cost:** remain excluded until comparable, traceable cost data are found.

No weights, fuzzy numbers, rankings, or scores are assigned in this phase.

## 6. Methodology status

Fuzzy TOPSIS with triangular fuzzy numbers remains a candidate method only. Before implementation, the team must confirm:

- that Fuzzy TOPSIS is permitted by the instructor;
- which methodological reference and variant must be followed;
- how source PCU/V/C values should be represented and normalised;
- how categorical LOS is handled or whether it is interpretation-only;
- how directional and morning/evening observations are aggregated or kept separate; and
- what worked example and independent verification are required.

Once approved, one consistent reference must define normalisation, criterion orientation, fuzzy-number construction, weights, ideal solutions, distances, and closeness coefficients. Those choices must not be invented by the software implementation.

## 7. Risks and evidence still required

1. **Spatial compatibility:** obtain a report map, GIS/network definition, or other source-backed crosswalk for link-to-section correspondence before using delay or speed.
2. **Survey comparability:** verify collection dates, typical-working-day protocol, vehicle type, direction, and peak-window definitions across the tables.
3. **Criterion dependence:** document that V/C and LOS describe related congestion conditions; avoid double counting.
4. **Directional aggregation:** decide whether each direction is an alternative observation, whether a conservative rule is used, or whether direction-specific results are reported separately. This requires instructor/researcher approval.
5. **Intervention meaning:** identify what “intervention” means for a road section and whether the study is prioritising congestion severity rather than estimating project benefit or cost.
6. **Licensing:** preserve and cite the BBMP source and confirm academic-use/reuse conditions before redistribution.
7. **Method approval:** obtain the instructor’s method and scope confirmation before building the ranking engine.

## 8. Decisions requiring instructor confirmation

- Is road-section prioritisation acceptable as the primary scope, given that intersection-level data lack comparable multi-criteria coverage?
- Is Fuzzy TOPSIS the required or permitted method? If yes, which reference/variant is required?
- Should LOS be interpretation-only while V/C is the continuous congestion criterion?
- Should morning and evening be modelled separately, or should a single aggregation be used?
- How should the two directions be handled?
- Is a volume/V/C-focused prioritisation acceptable without intervention-cost data?

## 9. Phase 2D conclusion

The evidence does not justify merging the seven citywide intersections, five corridor intersections, and six road sections into one dataset. The six road sections are the most defensible primary scope for the proposed MCDA, while the seven intersections remain a valuable descriptive and potential fallback dataset. The study should proceed to data-protocol clarification and instructor approval—not algorithm implementation—until the remaining compatibility and methodology decisions are resolved.

# Dataset audit — Phase 2A: Traffic data discovery

Audit date: 2026-10-18<br>
Project: MobilityForge — Urban Mobility Intelligence<br>
Research objective: prioritise urban traffic congestion interventions using defensible multi-criteria decision-making.<br>
Scope boundary: this is a discovery audit. No data have been cleaned, combined, transformed, ranked, or used in fuzzy calculations.

## Verified findings

### CTTP existing-travel chapter

The inspected CTTP chapter is a credible planning-study source of *historical road-link evidence*. It contains a table of 24 mid-block counts, expressed as total 12-hour vehicle and PCU counts with AM/PM peak-hour windows. It also reports screenline counts and describes a moving-car speed/delay study on 16 routes. The source explicitly distinguishes mid-block, screenline, outer-cordon, and route surveys.

The report says moving-car observations covered three morning-peak runs, three evening-peak runs, and one afternoon off-peak run; it says travel time between nodes and queueing delay were recorded in data sheets. However, the inspected published chapter exposes lane-category aggregate parameters rather than the location-by-period travel-time/delay observations. Therefore, the existence of time-of-day collection is verified, but a public time-sliced analytical matrix is **not** verified.

The CTTP table must not be treated as intersection data merely because several road labels mention a circle or junction. It is explicitly labelled “Traffic Volume at Mid-Block Locations.” Likewise, a route-level speed/delay observation cannot automatically be joined to a mid-block count without a documented spatial crosswalk and matching period.

### Bengaluru City Traffic Signal Data

OpenCity metadata confirms a Bengaluru Traffic Police PDF resource named for signal timings at Sony World and Arbindo Circle Junctions. This could supply operational context for those two junctions if its contents and reuse rights are later obtained. It does not currently close the key gaps: comparable traffic volume, observed delay, congestion severity, or intervention cost across alternatives.

## Candidate comparison

| Candidate | Inspected evidence | Legitimate alternative unit | Criteria supported now | Time-of-day feasibility | Decision |
|---|---|---|---|---|---|
| CTTP, mid-block volume table | 24 named mid-block road locations; 12-hour vehicles and PCUs; AM/PM peak windows | Road sections/mid-block locations only | Traffic volume (vehicles or PCUs over 12 hours) | Peak timing is available; per-location AM-vs-PM volumes are not published in the inspected table | Potential baseline after authorised, reproducible extraction and a defined road-section scope |
| CTTP, 16-route speed/delay study | Route list; stated AM/PM/off-peak survey design; aggregate lane-category outputs | Routes/links only | No location-level delay/speed table verified | Raw time-sliced observations are described but not present in inspected output | Not usable until original route-level survey sheets or an equivalent table is obtained |
| BTP signal-timing PDF | Metadata/title only, for two junctions | Two named junctions, pending content inspection | None verified | Unknown | Auxiliary context only; not a ranking dataset |

## Criterion evidence assessment

| Provisional criterion | Evidence status | What is defensible now | Gap / restriction |
|---|---|---|---|
| Traffic volume | Partially available | CTTP mid-block 12-hour vehicle or PCU counts | Historical, link-level, and not directly comparable to junction observations without a justified reframing |
| Congestion severity | Not directly available as a comparable location-level field | CTTP narrates congestion and derives category-level speed-flow relationships | Do not substitute narrative statements or category averages for per-alternative severity values |
| Travel delay | Collection described, values not verified at route/location level | None for a decision matrix | Obtain source data sheets or a public table with route/link and period values |
| Intervention cost | Not found | None | Cost must be excluded unless a compatible, traceable intervention-cost source is acquired |
| Time of day | Survey design verified for CTTP moving-car work | Existence of AM/PM/off-peak collection design | Need location-level values for each period; peak-hour labels alone cannot support a morning-versus-evening ranking |

## Feasibility conclusion

No candidate currently supports the original, broad claim: “prioritise urban road intersections” using volume, congestion severity, delay, and intervention cost with a time-aware comparison.

The most defensible potential narrowing is a **historical road-section congestion-intervention screening study**, using only a homogeneous subset of CTTP mid-block locations *if* the original PDF can be lawfully retrieved, its table can be reproducibly extracted, and the methodology is explicit that the alternatives are road sections—not intersections. That narrowing would initially support traffic volume only. A multi-criteria model must wait for at least one additional compatible, location-level criterion rather than manufacturing one from labels or narrative.

Time-of-day research is not feasible from the inspected published values. It becomes feasible only if route/link observations are obtained for AM and PM from the original survey sheets or an equivalent verified source, with the same alternatives, period definitions, and units.

## Data integrity decisions

- No raw source was saved. The CTTP resource was viewable through a portal proxy, but the attempted direct download returned HTTP 404; the signal-timing document was not retrievable. Preserving a cached or transformed substitute would violate the raw-data requirement.
- `data/raw/` was not created because it would be empty and no genuine download occurred.
- No processed dataset, decision matrix, joins, imputations, or rankings were produced.
- No source has been approved for modelling. Licence/reuse clarification remains required because both portal listings report no licence.

## Required next evidence before Phase 2B

1. Obtain an authorised original CTTP file or a first-party/official dataset download and record a checksum, file name, and stable URL.
2. Verify the CTTP report year and field collection dates from the complete source, not portal metadata.
3. Identify a compatible source containing per-road-section or per-intersection travel speed/delay/congestion values, preferably by AM and PM period.
4. Decide whether the academic scope may be narrowed from intersections to road sections. If not, obtain a genuine intersection-level dataset instead.
5. Exclude intervention cost unless a source defines comparable interventions and cost estimates for the exact same alternatives.

## Verification performed

- Inspected repository status and confirmed no pre-existing `data/` or `research/` files.
- Examined OpenCity CTTP dataset/resource metadata and the 29-page “Existing Travel and Characteristics” PDF through the portal proxy.
- Checked the CTTP table of contents and relevant volume, speed/delay, and survey-method sections.
- Examined OpenCity metadata for the Bengaluru City Traffic Signal Data resource.
- Tested an attempted CTTP direct download endpoint using HTTP headers; it returned 404, so no file was preserved.

# Phase 2C — Data Extraction and Compatibility Audit

**Project:** MobilityForge — Building Better Mobility Systems<br>
**Audit date:** 2026-10-18<br>
**Scope:** Source-faithful extraction and compatibility assessment only. No fuzzy calculations, rankings, imputation, or backend/frontend implementation were performed.

## 1. Source verification

The preserved primary source is:

> Government of Karnataka / BBMP, *Comprehensive Bengaluru City Traffic Management Infrastructure Plan: Final Feasibility Report*, December 2024, Tumkur Road–Old Madras Road corridor and citywide travel-demand sections.

Preserved file: `data/raw/bbmp-ctmp-tumkur-road-old-madras-road.pdf`<br>
SHA-256: `c6a0b8b0695a087ba65f65b2f9ffe63c7180b2f4de3ab63f3bc74f6f65d0f8fa`<br>
File size: 61,530,920 bytes<br>
PDF metadata: 628 pages; PDF 1.7; unencrypted.

The hash was recomputed locally with `shasum -a 256` and matches the value recorded during retrieval. The source remains unchanged.

## 2. Extracted intersection observations

The report contains two different intersection tables. They must not be silently combined:

1. **Seven citywide critical intersections — Table 158, PDF page 546.** This table has daily vehicle and PCU totals plus one morning and one evening peak observation for each location. The source labels the final field “Direction of maximum Flow”; the extracted values are retained as the report’s associated direction label without interpreting it as an additional measurement.
2. **Five Tumkur corridor turning-count intersections — Table 10, PDF page 48.** This is a separate corridor survey with peak-hour vehicles and PCUs only. It is not the same seven-location set.

Source-faithful CSV extracts:

- [`bbmp_intersection_volume_table158.csv`](../data/extracted/bbmp_intersection_volume_table158.csv)
- [`bbmp_tumkur_intersection_volume_table10.csv`](../data/extracted/bbmp_tumkur_intersection_volume_table10.csv)

Units are preserved as reported: vehicles and PCUs; daily totals where provided; peak periods as source text. No totals were recomputed and no missing periods were filled.

The seven-location table supports a **descriptive daily/AM/PM traffic-volume comparison**. It does not, by itself, provide comparable delay, speed, intervention cost, or intersection-level LOS criteria for the same seven alternatives.

## 3. Extracted road-section observations

Table 8 (PDF page 46) reports six Tumkur Road mid-block sections. For each section it provides directional morning and evening peak PCU volumes, V/C ratios, and LOS classifications. Direction labels are preserved as “Towards Yeshwanthpur” and “Towards Nagasandra”.

Source-faithful extract: [`bbmp_tumkur_midblock_vc_los_table8.csv`](../data/extracted/bbmp_tumkur_midblock_vc_los_table8.csv)

The report states that capacity is adjusted for on-street parking, bus stops, and access points, and that a bus-stop factor of 0.6 is used at specified locations. Therefore, the V/C values are source-model outputs, not raw observations. Their definition and adjustment assumptions must be retained if this table is later used.

The six sections are:

- Yeshwanthpur TTMC
- Yeshwanthpur Skywalk
- Gorguntepalya–SRS
- SRS–Jalahalli Junction
- Jalahalli Junction–Hesarghatta Junction
- Hesarghatta Junction–Nagasandra

The report explicitly describes the first three sections as LOS F in both directions for the reported peaks; later sections contain E/C, F/C, and B/C combinations as recorded in the CSV.

## 4. Delay, journey-time, and speed correspondence

The report’s speed-and-delay tables are **link-wise**, directional, vehicle-specific, and period-specific. They are not a seven-intersection table and are not a one-to-one copy of the six Table 8 mid-block sections.

Evidence inspected:

- Table 10 (PDF page 48): five corridor intersection peak-volume locations.
- Tables 11–18 (PDF pages 49–57): bus and car link sequences for morning and evening peaks in both directions.
- The links use nodes such as TTMC, MEI Junction, Goraguntepalya, 100 Ft Junction, SRS, Jalahalli, 8th Mile, and Nice Interchange. Segment boundaries and direction change between tables.
- The tables report delay in seconds, journey/running time in seconds, and journey/running speed in km/h. The report defines journey speed as distance divided by total travel time including delay, and running speed as distance divided by moving time.

This establishes genuine speed/delay evidence for the corridor, but not an automatic compatible join to every Table 8 section or to the seven Table 158 intersections. A spatial/link crosswalk, matching observation-period metadata, and a rule for aggregating directional links would be required before treating them as criteria in one decision matrix. No such join has been performed here.

## 5. Scope feasibility assessment

### Preferred intersection scope

The seven citywide intersections can legitimately support a comparative traffic-volume analysis using daily, morning-peak, and evening-peak vehicles/PCUs. However, the inspected source does not yet support a defensible multi-criteria ranking of those seven locations because comparable delay, speed, LOS/V/C, and intervention-cost values for the same alternatives were not established.

The five Tumkur corridor intersections have richer nearby corridor evidence, but they are a different alternative set from Table 158 and should not be merged without an explicit spatial and methodological justification.

### Road-section fallback

The six road sections have the strongest currently demonstrated multi-criteria evidence within one corridor: directional PCU volumes, source-derived V/C ratios, LOS, and related corridor speed/delay links. Nevertheless, the speed/delay links do not map one-to-one to all six Table 8 sections in the inspected tables. Road-section prioritisation is therefore a **credible fallback candidate**, not yet a ready-to-rank matrix.

### Intervention cost

No comparable, location-specific intervention-cost observations were verified in the extracted tables. Cost must be excluded unless a traceable source with compatible scope and period is found.

### Time-of-day extension

Time-of-day comparison is feasible descriptively: the source reports daily, morning, and evening volumes for Table 158 and morning/evening corridor observations for Tables 8 and 10. A defensible time-aware decision model remains conditional on selecting one alternative set and aligning all criteria to the same locations, directions, and observation periods.

## 6. Recommendation and unresolved questions

1. Retain intersections as the preferred research scope, but narrow the claim initially to verified traffic-volume prioritisation unless additional compatible intersection-level criteria are obtained.
2. Treat the six Tumkur road sections as the strongest fallback for a multi-criteria study, subject to a documented link-to-section crosswalk and period alignment.
3. Do not combine the seven citywide intersections with the five corridor intersections or six road sections as if they were one dataset.
4. Exclude intervention cost until verified.
5. Obtain instructor confirmation that fuzzy TOPSIS and the proposed time-aware comparison are permitted before implementing the decision engine.

Remaining evidence questions:

- Can the report’s raw survey appendices or GIS/network definitions provide a defensible crosswalk between Table 8 sections and speed/delay links?
- Are the intersection and corridor surveys from the same collection date/typical working-day protocol?
- Can a traceable, comparable intervention-cost source be identified?
- Does the instructor require intersection alternatives specifically, or permit road-section alternatives as the fallback?

## 7. Verification record

Commands/checks performed:

- Local SHA-256 verification with `shasum -a 256`.
- PDF metadata inspection with `pdfinfo`.
- Text extraction of PDF pages 46–50, 545–546, and 57 using the bundled `pypdf` runtime.
- Manual comparison of extracted values against the source table text.

No frontend, backend, data-cleaning pipeline, fuzzy-ranking implementation, or calculated research result was added in Phase 2C. No commit was created.

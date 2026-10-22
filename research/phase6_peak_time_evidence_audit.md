# Phase 6 — Peak-Time Evidence Audit

**Project:** MobilityForge — Building Better Mobility Systems
**Audit date:** 2026-10-22
**Scope:** verify whether the BBMP report explicitly defines clock-time windows for the six Tumkur Road sections’ Table 8 V/C and LOS measurements.

## Conclusion

**NEEDS EVIDENCE.** The report explicitly labels the Table 8 observations as “Morning Peak” and “Evening Peak”, but Table 8 does not provide clock-time windows. The report does provide clock-time windows in the preceding Table 7 traffic-volume table for six similarly named sections. Because the Table 7 PCU values do not match the Table 8 PCU volume fields used with V/C and LOS, the Table 7 times cannot safely be assigned to Table 8 without an explicit source statement.

## Source inspected

Preserved PDF: `data/raw/bbmp-ctmp-tumkur-road-old-madras-road.pdf`
SHA-256 verified locally as `c6a0b8b0695a087ba65f65b2f9ffe63c7180b2f4de3ab63f3bc74f6f65d0f8fa`.

The relevant source pages were inspected with local `pypdf` extraction:

- PDF page 25 / printed report page 25: primary-survey methodology.
- PDF page 44 / printed report page 14: Table 6 and Table 7 traffic-volume material.
- PDF page 45 / printed report page 15: V/C and LOS definitions and interpretation.
- PDF page 46 / printed report page 16: Table 8 and its surrounding notes.
- PDF page 47 / printed report page 17: Table 9 V/C summary.

## Evidence that is explicitly stated

### Survey methodology — PDF page 25

The “Intersection Turning Volume” methodology says that videographic volume counts were conducted on a typical working day for six hours covering both morning and evening peak periods. It identifies outputs such as peak-hour vehicle/hour and PCU/hour values. It does not specify clock times for the Table 8 V/C/LOS observations.

### Table 7 traffic-volume windows — PDF page 44 / printed page 14

The section headed “Traffic Volume Counts” says that direction-wise peak-hour traffic volumes are presented in Table 7. Table 7 prints these windows for the six named road sections:

| Road section | Morning window in Table 7 | Evening window in Table 7 |
|---|---|---|
| Yeshwanthpur TTMC | 11.00–12.00 | 19.30–20.30 |
| Yeshwanthpur Skywalk | 9.30–10.30 | 18.00–19.00 |
| Tumkur Road (Between Gorguntepalya–SRS) | 9.15–10.15 | 17.45–18.45 |
| Tumkur Road (Between SRS–Jalahalli Junction) | 9.45–10.45 | 17.30–18.30 |
| Tumkur Road (Between Jalahalli Junction–Hesarghatta Junction) | 10.45–11.45 | 19.30–20.30 |
| Tumkur Road (Between Hesarghatta Junction–Nagasandra) | 10.45–11.45 | 19.30–20.30 |

These times are verified as Table 7 traffic-volume windows. They are not printed in Table 8.

### Table 8 V/C and LOS — PDF page 46 / printed page 16

The surrounding text defines V/C as the ratio of peak-hour traffic flow rate to capacity and says that the V/C ratio and LOS of the road sections are presented in Table 8. The table headings identify “Morning Peak” and “Evening Peak”, with directional PCU volume, V/C, and LOS fields.

Table 8 does **not** print clock-time windows. It also reports PCU volume fields that differ from the preceding Table 7 PCU traffic-volume fields. For example, Yeshwanthpur TTMC is 3,407 / 3,285 PCUs in Table 8, while Table 7 shows 3,210 / 3,089 PCUs for its listed morning window. This is evidence against silently treating the Table 7 time as the Table 8 measurement time.

### V/C and LOS interpretation — PDF pages 45–46

The report states that LOS ranges from A to F and that the service measures used to define LOS are density and V/C. It explains that capacity is adjusted for road geometry and site conditions, including parking, bus stops, and access points. These notes explain the measures but do not establish Table 8 clock-time windows.

## What can and cannot be concluded

**Verified:**

- Table 8 contains morning/evening peak labels and directional PCU, V/C, and LOS values for six sections.
- Table 7 contains the exact clock-time windows listed above for traffic-volume counts at the same section names.
- The methodology describes a six-hour typical-working-day survey spanning both peak periods.

**Not verified:**

- That each Table 7 clock-time window is the exact observation window for the corresponding Table 8 V/C/LOS values.
- That the Table 7 and Table 8 fields were collected in the same run, date, or processing step.
- A single common morning or evening clock-time window across all six sections.

## Effect on the Phase 4 specification

The exact Table 7 windows should not be added to the Table 8 V/C/LOS criteria as if the correspondence were proven. The safe model metadata is:

> Period labels: source-reported morning peak and evening peak; exact clock-time windows for the Table 8 V/C/LOS values remain unresolved.

The Table 7 windows may be retained as separately identified traffic-volume evidence, but only a source-backed cross-reference can promote them to Table 8 time metadata.

## Verification record

- Recomputed the preserved PDF SHA-256.
- Extracted and inspected PDF pages 25, 44–48 with the bundled `pypdf` runtime.
- Compared the Table 7 and Table 8 section names and PCU fields against `data/extracted/bbmp_tumkur_midblock_vc_los_table8.csv`.
- Confirmed no source data, CSVs, backend code, frontend code, model outputs, weights, or rankings were changed.

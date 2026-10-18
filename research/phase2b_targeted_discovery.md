# Phase 2B — Targeted traffic data discovery

Audit date: 2026-10-18<br>
Project: MobilityForge — Building Better Mobility Systems.<br>
Decision rule: intersections first; road sections if intersection data cannot support a compatible model; reassess if neither is feasible.

## Outcome

The targeted search found one substantially stronger candidate than the historical OpenCity CTTP chapter: the 2024 BBMP *Comprehensive Bengaluru City Traffic Management Infrastructure Plan* report. Its inspected pages contain real, named intersection alternatives with morning/evening peak traffic volumes and PCUs, and its corridor sections contain road-section V/C/LOS plus link-level speed and delay measurements. The original PDF was retrievable and has been preserved unchanged with a checksum.

This is a discovery result, not model approval. The intersection portion is currently volume-focused; it does not yet provide a complete set of multiple comparable criteria for every intersection. The road-section portion is richer, but its volume and speed-delay tables must still be matched through a documented spatial crosswalk before they can be combined.

## Candidate assessment

### 1. BBMP Comprehensive Traffic Management Infrastructure Plan — preferred candidate

The report cover identifies the Government of Karnataka and BBMP and dates the final feasibility report to December 2024. It names Altinok Consulting Engineering Pvt. Ltd. as consultant. The relevant report is 628 pages and contains several corridor/infrastructure sections; page numbers below refer to the PDF page labels extracted from the preserved file.

Evidence inspected:

- Page 25 says primary surveys included road inventory, intersection turning-volume surveys, speed/delay surveys, and classified traffic counts. It states video counts covered a typical working day and six hours spanning morning and evening peak periods.
- Pages 44–48 describe five turning-count intersections, two mid-block locations, 11 km of speed/delay survey, and five signal-phasing locations for the Tumkur Road corridor. They report peak traffic, PCUs, V/C, and LOS.
- Page 546 reports seven citywide critical intersections: CN Rao Underpass Junction/Mekhri Circle, Bangalore Cantt Junction, Basaveshwara Circle, KR Circle/Anand Rao Junction, Cubbon Park UB City signal, Shoolay Circle, and Lalbagh Chowk/South End Circle. Each row includes daily vehicles/PCUs and morning/evening peak-hour vehicles/PCUs with the peak window.
- Pages 53–56 contain car link-level distance, delay seconds, journey/running time, and journey/running speed for morning and evening directions along an 11 km corridor. Pages 50–52 contain the analogous bus speed/delay tables.

What it can legitimately support:

- Intersection scope: a transparent AM/PM traffic-volume comparison for seven named intersections, subject to checking the underlying survey definitions and exact table extraction.
- Road-section scope: a candidate multi-criteria design using volume or PCU flow, V/C or LOS, and link-level delay/speed, subject to proving that the alternatives and periods align.
- Time-aware analysis: feasible in principle because both morning and evening peak values are explicitly present.

What it does not yet support:

- A comparable intervention-cost criterion for the same alternatives. The report proposes infrastructure works, but no per-alternative cost field has been verified for the ranking set.
- A claim that the seven intersection rows contain measured delay or speed for those same seven alternatives. The delay tables are link/direction tables, not a seven-row intersection delay matrix.
- A direct join between every volume row and every speed-delay row without a formal spatial/period crosswalk.

### 2. Historical CTTP chapter — secondary context, not selected matrix

The earlier CTTP chapter remains useful for historical context: 24 mid-block counts, screenline counts, and a described 16-route speed/delay study. Its accessible publication did not provide a clean location-by-period matrix, and its attempted direct download returned 404. It is therefore not selected as the primary raw dataset.

### 3. BMD-45 — credible auxiliary computer-vision source

BMD-45 is an IISc AIM dataset with CC BY 4.0, Bengaluru CCTV images and vehicle annotations, including junction and mid-block views. It covers February 2025 daytime frames. However, its anonymised filenames prevent direct location inference, and it supplies images/boxes rather than measured traffic volume, speed, delay, or capacity. It is not a ready ranking dataset.

### 4. Traffic Monitor Lizard — temporal route context

This public CC BY dataset records Google Maps travel-duration estimates on predetermined Bengaluru routes roughly 10 km long, with date/time and distance fields. It can inform route-level travel-time variability, but it is not intersection data, has no traffic volume or PCU field, and cannot be silently combined with BBMP rows.

## Scope decision after discovery

The original intersection scope is no longer blocked at the level of *finding any observations*: the BBMP report provides seven named intersections and AM/PM volumes. It remains blocked at the level of a defensible **multi-criteria** ranking unless a second or third criterion can be aligned to those same intersections.

The most defensible working direction is therefore:

1. Keep the seven BBMP intersections as the preferred alternative set for a volume/time descriptive analysis and investigate whether the report contains matching intersection-level delay, signal, or pedestrian measures elsewhere in the preserved file.
2. Prepare a road-section fallback using the Tumkur corridor tables if the volume, V/C/LOS, and speed-delay alternatives can be matched exactly by segment and period.
3. Do not implement Fuzzy TOPSIS or choose weights until that alignment and the criterion definitions are verified.
4. Exclude intervention cost unless a source provides comparable costs for the exact alternatives.

## Data and provenance actions completed

- Downloaded the original BBMP report from the OpenCity resource URL into `data/raw/bbmp-ctmp-tumkur-road-old-madras-road.pdf`.
- Verified HTTP 200, `Content-Type: application/pdf`, `Content-Length: 61,530,920`, and `Last-Modified: 2025-11-25`.
- Calculated SHA-256: `c6a0b8b0695a087ba65f65b2f9ffe63c7180b2f4de3ab63f3bc74f6f65d0f8fa`.
- Confirmed with `pdfinfo`: 628 pages, unencrypted, PDF 1.7.
- Extracted and reviewed the methodology, traffic survey, intersection-volume, V/C/LOS, and speed-delay pages using the bundled PDF reader.
- No processed CSV, joins, interpolations, rankings, fuzzy calculations, backend code, or frontend changes were made.

## Remaining questions before Phase 2C / modelling

- Which of the report's sections are part of one internally consistent survey year and corridor, rather than separate infrastructure studies bundled in one PDF?
- Can exact intersection-to-link relationships be documented for the seven intersection alternatives and the speed-delay rows?
- Are the reported morning/evening periods comparable across alternatives, or must each row retain its stated local peak window?
- Can BBMP or the portal clarify reuse conditions beyond the consultant's purpose disclaimer?
- Is a second criterion available for the same seven intersections, or should the study explicitly narrow to road-section alternatives?

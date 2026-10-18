# Source register — Phase 2A

Retrieval date: 2026-10-18. This register records sources inspected during discovery. It does not assert that a source is ready for modelling.

## SR-01 — Comprehensive Traffic and Transportation Plan for Bengaluru (CTTP)

- Publisher/portal listing: OpenCity Urban Data Portal; dataset listing attributes the organisation as Bengaluru Traffic Police. The chapter itself identifies RITES Ltd.
- Dataset title: [Comprehensive Traffic and Transportation Plan for Bengaluru](https://data.opencity.in/dataset/comprehensive-traffic-and-transportation-plan-for-bengaluru).
- Inspected resource: [“003_Existing Travel and Characteristics-oct 07”](https://data.opencity.in/dataset/comprehensive-traffic-and-transportation-plan-for-bengaluru/resource/0e379d61-4077-4d31-91d8-33716a09a6db/proxy), PDF, 29 pages.
- Portal metadata observed: created 2022-04-11; portal last-updated metadata is not a survey or report publication date. The inspected chapter does not establish a single collection date in the material reviewed.
- Coverage/granularity: Bengaluru/Bangalore Metropolitan Area study context. It reports 24 mid-block locations, 16 screenline locations, 10 outer-cordon O-D surveys, and a separate 16-route moving-car study. These are road links/routes and survey points; they must not be relabelled as a common set of intersections.
- Variables verified in the inspected chapter:
  - Table 3.1: total 12-hour traffic volumes in vehicles and PCUs, plus AM and PM peak-hour *time windows*, at mid-block locations.
  - Table 3.2: total 16-hour traffic volumes in vehicles and PCUs at screenline locations.
  - Sections 3.9.1–3.9.4: a speed-and-delay study on 16 selected routes. The report states that runs were made in morning, evening, and afternoon; journey time and queueing delay were noted in survey data sheets.
  - Table 3.16: aggregated speed-flow parameters by lane category, including free-flow speed, assumed directional capacity, speed at capacity, and R². These are category-level results, not per-location observations.
- Units: vehicles/12 hours, PCUs/12 hours, vehicles/16 hours, PCUs/16 hours, km/h, PCU/hour/lane. The source describes AM peak generally as 09:00–11:00 and PM peak as 17:00–19:00 for the moving-car study.
- Licence/reuse: OpenCity displays “No License Provided.” Reuse rights must be clarified before redistributing or using extracted material beyond the academic project.
- Retrieval outcome: the portal resource was inspected through its accessible proxy. A direct HTTP request to the attempted original PDF download path returned HTTP 404 on 2026-10-18. No raw copy was saved.
- Suitability status: promising historical road-link evidence; not currently a verified intersection-level analytical dataset.

## SR-02 — Bengaluru City Traffic Signal Data

- Publisher/portal listing: OpenCity Urban Data Portal; organisation listed as Bengaluru Traffic Police.
- Dataset title: [Bengaluru City Traffic Signal Data](https://data.opencity.in/dataset/groups/bengaluru-city-traffic-signal-data).
- Inspected resource metadata: [“Signal Timings Data - Sony World and Arbindo Circle Junctions”](https://data.opencity.in/dataset/bengaluru-city-traffic-signal-data/resource/d5f2bfdd-7251-4e86-834c-594e524aca83), PDF.
- Portal metadata observed: PDF; resource created/last updated 2025-11-25; no licence provided; CKAN datastore inactive.
- Variables/granularity: the resource title establishes signal-timing material for two named junctions. The document contents could not be fetched through the portal during this audit, so no timing fields, collection period, or units are asserted.
- Licence/reuse: no licence provided.
- Retrieval outcome: metadata inspected; the resource document had a cache miss and was not retrieved. No raw copy was saved.
- Suitability status: possible auxiliary operational context only. It is not evidence of traffic volume, delay, congestion severity, or intervention cost.

## Sources screened but not admitted as evidence

- Search results surfaced a “Bangalore traffic pulse” dataset cited by a research paper and hosted through Kaggle. Its first-party provenance, collection method, licensing, and whether values are measured rather than constructed were not verified in this phase. It is not registered as a usable source and no file was downloaded.
- OpenCity also lists planning documents and road/safety datasets. None were treated as substitutes for link/intersection traffic observations without inspecting their contents and matching their granularity.

## SR-03 — Comprehensive Bengaluru City Traffic Management Infrastructure Plan

- Official entities named in the source: Government of Karnataka and Bruhat Bengaluru Mahanagara Palike (BBMP); consultant named as Altinok Consulting Engineering Pvt. Ltd., New Delhi.
- Report title: *Final Feasibility Report — Comprehensive Bengaluru City Traffic Management Infrastructure Plan: Proposals for Vehicular Tunnel / Grade Separator / Road Widening in Selected Corridors*.
- Publication/date evidence: cover says “December 2024.” The downloaded PDF's HTTP `Last-Modified` header was 2025-11-25; this is a portal file timestamp, not a survey date.
- Original download: [OpenCity PDF resource](https://data.opencity.in/dataset/2c324650-7caa-40b6-82ef-f99509d5b376/resource/be5f1ca6-4252-432b-b32a-caa54db69dd6/download/305c1726-cae5-43dc-81c1-c0ae0db22c92.pdf).
- Preserved raw file: `data/raw/bbmp-ctmp-tumkur-road-old-madras-road.pdf` (61,530,920 bytes; SHA-256 `c6a0b8b0695a087ba65f65b2f9ffe63c7180b2f4de3ab63f3bc74f6f65d0f8fa`).
- Geographic coverage: multiple Bengaluru corridor/infrastructure studies in one 628-page report. The inspected portions include the Tumkur Road–Old Madras Road corridor and a later citywide travel-demand section.
- Verified variables and granularity:
  - Tumkur corridor: five turning-count intersections, two mid-block locations, 11 km of speed/delay survey, and signal phasing at five intersections.
  - Intersection table (report page 546): seven named junctions with daily vehicles, daily PCUs, morning peak hour and vehicles/PCUs, and evening peak hour and vehicles/PCUs.
  - Corridor mid-block table (report pages 44–47): directional peak vehicles/PCUs, V/C ratios, and LOS for six mid-block alternatives.
  - Car and bus speed/delay tables (report pages 50–56): from-node/to-node link, distance (km), delay (seconds), journey/running time (seconds), journey/running speed (km/h), period/direction, and stated delay cause.
  - Later citywide travel-demand section (report pages 545–546): seven critical intersections with daily and morning/evening peak vehicles and PCUs.
- Time coverage: morning and evening peak periods are explicitly reported; the exact peak window varies by location and is recorded in the tables. The report states video counts were conducted on a typical working day for six hours covering both peak periods.
- Licensing/reuse: the OpenCity listing/licence terms were not established as an open licence in the inspected material. The report contains a consultant disclaimer restricting use to its commissioned purpose. Preserve and cite the raw source; obtain permission or confirm academic-use conditions before redistribution.
- Suitability status: strongest candidate found. It supports intersection-level AM/PM volume analysis and a more complete road-section fallback with volume, V/C/LOS, and speed-delay evidence. It does not provide comparable intervention costs for each alternative in the inspected sections.

## SR-04 — BMD-45: Bengaluru Mobility Dataset

- Source: [IISc AI for Integrated Mobility dataset card](https://huggingface.co/datasets/iisc-aim/BMD-45).
- Provenance/coverage: 45,986 CCTV images and approximately 481,947 vehicle annotations from about 3,679 Safe City cameras across Bengaluru; the card says both junction and mid-block perspectives are included.
- Time period: frames sampled during February 2025, 06:00–18:00 IST. Filenames are anonymised numeric IDs to prevent location inference.
- Variables/units: image frames and COCO bounding-box/category annotations, not precomputed traffic volume, speed, delay, capacity, or congestion fields.
- Licence: CC BY 4.0 on the dataset card.
- Suitability status: credible auxiliary source for a future vehicle-count extraction study, but not a ready-to-rank traffic matrix. It cannot establish intersection alternatives without recovering camera/location mapping and doing a separately validated computer-vision counting process.

## SR-05 — Traffic Monitor Lizard / traffiCOracle

- Source: [public GitHub repository](https://github.com/thecont1/traffic-monitor-lizard) and its [Datameet announcement](https://www.mail-archive.com/datameet%40googlegroups.com/msg09810.html).
- Coverage/granularity: predetermined Bengaluru routes, roughly 10 km each; route observations are not intersections.
- Variables/units documented by the repository: date, local time, route code, travel duration (minutes), route distance (km), and derived speed; weather fields are also stored. The repository describes twice-hourly Google Maps duration estimates and public versioned CSVs.
- Licence: repository README states the dataset is CC BY 4.0; code is AGPLv3.
- Provenance limitation: travel times are Google Maps estimates collected by an automated scraper, not stationary counts or direct field measurements. The route definitions and methodology must be inspected before using it as an academic measurement source.
- Suitability status: potentially useful for a road-route temporal reliability criterion, but it has no traffic volume, PCU, V/C, or intervention-cost fields and cannot be silently joined to the BBMP alternatives.

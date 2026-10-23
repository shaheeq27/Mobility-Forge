# MobilityForge research engine

This package is the Phase 5 data and calculation core for the verified BBMP Table 8 extract.

## Implemented

- Source-faithful CSV loading into explicit section/period/direction observations.
- Integrity validation for the six expected alternatives, source page, missing observations, numeric ranges, and LOS categories.
- Isolated min–max normalization and weighted-sum primitives that require the caller to provide criterion direction and weights explicitly.
- Independently testable Fuzzy TOPSIS primitives: validated TFNs, Chen-style linear benefit/cost normalization, explicit crisp-weight application, weighted-matrix FPIS/FNIS points, vertex distance, and closeness coefficients. These primitives are not connected to the research dataset.
- Tests using the standard-library `unittest` runner.

## Intentionally not implemented

- No default weights, normalization policy, period aggregation, or direction aggregation.
- No research Fuzzy TOPSIS run: the mathematical primitives use documented candidate conventions, but instructor approval of the TFN representation, weights, normalization variant, and distance aggregation remains required.
- No rankings are reported as validated research findings; the explicitly acknowledged Phase 9 endpoint is a provisional execution aid.
- No speed/delay joins, intervention costs, or fabricated peak-window metadata.
- The Phase 9 execution endpoint is provisional only and requires explicit weights and acknowledgement; it never aggregates periods or directions.

The CSV is not copied or modified. Run tests from the repository root with:

```bash
PYTHONPATH=backend python3 -m unittest discover -s backend/tests -v
```

## Read-only API and provisional execution endpoint

Install the minimal API dependencies from the repository root:

```bash
python3 -m pip install -r backend/requirements.txt
```

Run the API locally:

```bash
PYTHONPATH=backend python3 -m uvicorn api.main:app --reload --port 8000
```

The API exposes `GET /health`, `GET /observations`, `GET /observations/validation`,
and `POST /decision-engine/run`. The execution endpoint runs exactly one
period/direction slice using the documented singleton-TFN and weighted-matrix
ideal conventions, and returns transparent intermediate values labelled
provisional. It does not aggregate period or direction records. `MOBILITY_FRONTEND_ORIGINS` may be
set to a comma-separated list of allowed frontend origins; by default the
local Next.js origins `http://localhost:3000` and `http://127.0.0.1:3000` are
allowed.

The execution request must include `period`, `direction`, a `weights` object
with explicit `pcu` and `vc` Decimal-compatible values summing exactly to one,
and `acknowledge_provisional: true`. No default weights are supplied.

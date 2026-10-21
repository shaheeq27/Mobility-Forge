"""Source-faithful loader for the verified BBMP Table 8 CSV."""

from __future__ import annotations

import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path

from .models import Direction, Period, SectionObservation

DEFAULT_DATASET = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "extracted"
    / "bbmp_tumkur_midblock_vc_los_table8.csv"
)

_EXPECTED_COLUMNS = {
    "source_page",
    "section_no",
    "road_section",
    "configuration",
    "morning_volume_pcu_towards_yeshwanthpur",
    "morning_volume_pcu_towards_nagasandra",
    "morning_vc_towards_yeshwanthpur",
    "morning_vc_towards_nagasandra",
    "morning_los_towards_yeshwanthpur",
    "morning_los_towards_nagasandra",
    "evening_volume_pcu_towards_yeshwanthpur",
    "evening_volume_pcu_towards_nagasandra",
    "evening_vc_towards_yeshwanthpur",
    "evening_vc_towards_nagasandra",
    "evening_los_towards_yeshwanthpur",
    "evening_los_towards_nagasandra",
}


def _decimal(value: str, field: str, row_number: int) -> Decimal:
    try:
        return Decimal(value)
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"row {row_number}: {field} is not numeric: {value!r}") from exc


def load_observations(path: str | Path = DEFAULT_DATASET) -> list[SectionObservation]:
    """Load the CSV without changing its measurements or aggregating dimensions."""

    source = Path(path)
    with source.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        missing = _EXPECTED_COLUMNS - columns
        if missing:
            raise ValueError(f"missing required columns: {sorted(missing)}")

        observations: list[SectionObservation] = []
        for row_number, row in enumerate(reader, start=2):
            source_page = int(row["source_page"])
            section_no = int(row["section_no"])
            for period, prefix in ((Period.MORNING, "morning"), (Period.EVENING, "evening")):
                for direction, suffix in (
                    (Direction.YESHWANTHPUR, "towards_yeshwanthpur"),
                    (Direction.NAGASANDRA, "towards_nagasandra"),
                ):
                    observations.append(
                        SectionObservation(
                            source_page=source_page,
                            section_no=section_no,
                            road_section=row["road_section"],
                            configuration=row["configuration"],
                            period=period,
                            direction=direction,
                            volume_pcu=_decimal(row[f"{prefix}_volume_pcu_{suffix}"], "volume_pcu", row_number),
                            vc_ratio=_decimal(row[f"{prefix}_vc_{suffix}"], "vc_ratio", row_number),
                            los=row[f"{prefix}_los_{suffix}"].strip(),
                        )
                    )
        return observations

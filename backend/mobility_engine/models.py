"""Typed representations of the verified Table 8 extract.

Values remain Decimal instances so loading does not introduce binary floating
point rounding. The model deliberately preserves period and direction rather
than aggregating them.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum


class Period(StrEnum):
    MORNING = "morning"
    EVENING = "evening"


class Direction(StrEnum):
    YESHWANTHPUR = "towards_yeshwanthpur"
    NAGASANDRA = "towards_nagasandra"


@dataclass(frozen=True)
class SectionObservation:
    """One source row/period/direction observation; no derived aggregation."""

    source_page: int
    section_no: int
    road_section: str
    configuration: str
    period: Period
    direction: Direction
    volume_pcu: Decimal
    vc_ratio: Decimal
    los: str

    @property
    def source_row(self) -> str:
        return f"Table 8 page {self.source_page}, section {self.section_no}"

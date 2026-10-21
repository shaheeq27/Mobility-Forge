"""Integrity checks for the verified Table 8 observation set."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .models import Direction, Period, SectionObservation

EXPECTED_SECTIONS = (
    "Yeshwanthpur TTMC",
    "Yeshwanthpur Skywalk",
    "Tumkur Road (Between Gorguntepalya-SRS)",
    "Tumkur Road (Between SRS-Jalahalli Junction)",
    "Tumkur Road (Between Jalahalli junction-Hesarghatta Junction)",
    "Tumkur Road (Between Hesarghatta Junction-Nagasandra)",
)
VALID_LOS = frozenset("ABCDEF")


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    source_row: str | None = None


def validate_observations(observations: list[SectionObservation]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if len(observations) != 24:
        issues.append(ValidationIssue("row_count", f"expected 24 period/direction observations, found {len(observations)}"))

    sections = tuple(dict.fromkeys(item.road_section for item in observations))
    if sections != EXPECTED_SECTIONS:
        issues.append(ValidationIssue("alternatives", f"unexpected section set: {sections}"))

    expected_by_number = {number: section for number, section in enumerate(EXPECTED_SECTIONS, start=1)}
    names_by_number: dict[int, set[str]] = {}
    numbers_by_name: dict[str, set[int]] = {}
    for item in observations:
        names_by_number.setdefault(item.section_no, set()).add(item.road_section)
        numbers_by_name.setdefault(item.road_section, set()).add(item.section_no)

    for number, expected_name in expected_by_number.items():
        mapped_names = names_by_number.get(number, set())
        if mapped_names != {expected_name}:
            issues.append(
                ValidationIssue(
                    "section_mapping",
                    f"section number {number} must map to {expected_name!r}, found {sorted(mapped_names)!r}",
                )
            )

    for number, mapped_names in names_by_number.items():
        if len(mapped_names) > 1:
            issues.append(
                ValidationIssue(
                    "section_mapping_conflict",
                    f"section number {number} maps to multiple names: {sorted(mapped_names)!r}",
                )
            )

    for name, mapped_numbers in numbers_by_name.items():
        if len(mapped_numbers) > 1:
            issues.append(
                ValidationIssue(
                    "section_mapping_duplicate",
                    f"section name {name!r} maps to multiple numbers: {sorted(mapped_numbers)!r}",
                )
            )

    expected_keys = {
        (section, period, direction)
        for section in EXPECTED_SECTIONS
        for period in Period
        for direction in Direction
    }
    actual_keys = {(item.road_section, item.period, item.direction) for item in observations}
    missing = expected_keys - actual_keys
    if missing:
        issues.append(ValidationIssue("missing_observations", f"missing section/period/direction keys: {sorted(missing)}"))

    for item in observations:
        if item.source_page != 46:
            issues.append(ValidationIssue("source_page", "expected Table 8 source page 46", item.source_row))
        if item.section_no < 1 or item.section_no > 6:
            issues.append(ValidationIssue("section_number", "section number must be 1 through 6", item.source_row))
        if not item.road_section.strip():
            issues.append(ValidationIssue("missing_section", "road section is empty", item.source_row))
        if not item.volume_pcu.is_finite() or item.volume_pcu <= Decimal("0"):
            issues.append(ValidationIssue("volume_range", "PCU volume must be finite and greater than zero", item.source_row))
        if not item.vc_ratio.is_finite() or item.vc_ratio < Decimal("0"):
            issues.append(ValidationIssue("vc_range", "V/C must be finite and non-negative", item.source_row))
        if item.los not in VALID_LOS:
            issues.append(ValidationIssue("los_value", "LOS must be one of A, B, C, D, E, or F", item.source_row))

    return issues

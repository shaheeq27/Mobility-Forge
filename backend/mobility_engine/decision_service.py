"""Single-run Fuzzy TOPSIS execution service.

This is deliberately a provisional research execution boundary: it accepts one
period/direction slice, explicit crisp weights, and returns every intermediate
value needed for review.  It never aggregates the four source slices.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Sequence

from .fuzzy_topsis import (
    TriangularFuzzyNumber,
    closeness_coefficients,
    fuzzy_ideal_solutions,
    normalize_fuzzy_criterion,
    rank_by_closeness,
    vertex_distance,
    weighted_normalized_matrix,
    validate_crisp_weights,
)
from .models import Direction, Period, SectionObservation
from .validation import EXPECTED_SECTIONS

CRITERIA = ("pcu", "vc")
METHODOLOGY_VERSION = "phase9-provisional-v1"


@dataclass(frozen=True)
class AlternativeResult:
    observation: SectionObservation
    normalized: dict[str, TriangularFuzzyNumber]
    weighted: dict[str, TriangularFuzzyNumber]
    distance_positive: Decimal
    distance_negative: Decimal
    closeness_coefficient: Decimal
    rank: int


@dataclass(frozen=True)
class DecisionResult:
    period: Period
    direction: Direction
    weights: dict[str, Decimal]
    alternatives: tuple[AlternativeResult, ...]


def _validate_slice(observations: Sequence[SectionObservation], period: Period, direction: Direction) -> list[SectionObservation]:
    if not observations:
        raise ValueError("at least one observation is required")
    if any(item.period != period or item.direction != direction for item in observations):
        raise ValueError("observations must contain exactly one requested period and direction")
    by_name: dict[str, SectionObservation] = {}
    for item in observations:
        if item.road_section in by_name:
            raise ValueError(f"duplicate alternative: {item.road_section}")
        by_name[item.road_section] = item
    if set(by_name) != set(EXPECTED_SECTIONS):
        missing = sorted(set(EXPECTED_SECTIONS) - set(by_name))
        extra = sorted(set(by_name) - set(EXPECTED_SECTIONS))
        raise ValueError(f"slice must contain exactly the six expected alternatives; missing={missing}, extra={extra}")
    ordered = [by_name[name] for name in EXPECTED_SECTIONS]
    if [item.section_no for item in ordered] != list(range(1, 7)):
        raise ValueError("section numbers must map to the expected alternatives in order")
    for item in ordered:
        if not item.volume_pcu.is_finite() or item.volume_pcu <= 0:
            raise ValueError(f"invalid PCU volume for {item.road_section}")
        if not item.vc_ratio.is_finite() or item.vc_ratio < 0:
            raise ValueError(f"invalid V/C ratio for {item.road_section}")
    return ordered


def run_fuzzy_topsis(
    observations: Sequence[SectionObservation],
    period: Period,
    direction: Direction,
    weights: dict[str, Decimal],
) -> DecisionResult:
    """Execute the documented provisional convention for one source slice."""
    validate_crisp_weights(set(CRITERIA), weights)
    ordered = _validate_slice(observations, period, direction)
    raw = {
        "pcu": [TriangularFuzzyNumber(item.volume_pcu, item.volume_pcu, item.volume_pcu) for item in ordered],
        "vc": [TriangularFuzzyNumber(item.vc_ratio, item.vc_ratio, item.vc_ratio) for item in ordered],
    }
    normalized = {
        name: normalize_fuzzy_criterion(values, "higher")
        for name, values in raw.items()
    }
    weighted = weighted_normalized_matrix(normalized, weights)
    positive, negative = fuzzy_ideal_solutions(weighted)
    coefficients = closeness_coefficients(weighted)
    ranking = rank_by_closeness(coefficients)
    ranks = {index: position + 1 for position, index in enumerate(ranking)}
    results: list[AlternativeResult] = []
    for index, item in enumerate(ordered):
        distance_positive = sum((vertex_distance(weighted[name][index], positive[name]) for name in CRITERIA), Decimal("0"))
        distance_negative = sum((vertex_distance(weighted[name][index], negative[name]) for name in CRITERIA), Decimal("0"))
        results.append(AlternativeResult(item, {name: normalized[name][index] for name in CRITERIA}, {name: weighted[name][index] for name in CRITERIA}, distance_positive, distance_negative, coefficients[index], ranks[index]))
    return DecisionResult(period, direction, dict(weights), tuple(results))

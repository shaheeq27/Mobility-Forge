"""Small, explicit Fuzzy TOPSIS primitives.

The implementation is deliberately independent of the research CSV. It uses
non-negative triangular fuzzy numbers (TFNs), Chen-style linear benefit/cost
normalisation, crisp caller-supplied criterion weights, weighted-matrix
FPIS/FNIS points, the vertex distance, and sum-of-criterion distances for the
closeness coefficient. These conventions are documented in Phase 7 and must
be approved before they are applied to the traffic observations.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from .scoring import DirectionOfPriority


ZERO = Decimal("0")
ONE = Decimal("1")


@dataclass(frozen=True, slots=True)
class TriangularFuzzyNumber:
    """A finite non-negative triangular fuzzy number ``(lower, modal, upper)``."""

    lower: Decimal
    modal: Decimal
    upper: Decimal

    def __post_init__(self) -> None:
        values = (self.lower, self.modal, self.upper)
        if any(not isinstance(value, Decimal) for value in values):
            raise ValueError("TFN components must be Decimal instances")
        if any(not value.is_finite() for value in values):
            raise ValueError("TFN components must be finite")
        if any(value < ZERO for value in values):
            raise ValueError("TFN components must be non-negative")
        if not self.lower <= self.modal <= self.upper:
            raise ValueError("TFN requires lower <= modal <= upper")

    def __mul__(self, scalar: Decimal) -> "TriangularFuzzyNumber":
        if not isinstance(scalar, Decimal) or not scalar.is_finite():
            raise ValueError("TFN scalar must be finite Decimal")
        if scalar < ZERO:
            raise ValueError("TFN scalar must be non-negative")
        return TriangularFuzzyNumber(
            self.lower * scalar,
            self.modal * scalar,
            self.upper * scalar,
        )

    __rmul__ = __mul__


def _validate_criterion_values(values: list[TriangularFuzzyNumber]) -> None:
    if not values:
        raise ValueError("criterion values cannot be empty")
    if not all(isinstance(value, TriangularFuzzyNumber) for value in values):
        raise ValueError("criterion values must be triangular fuzzy numbers")


def normalize_fuzzy_criterion(
    values: list[TriangularFuzzyNumber],
    priority: DirectionOfPriority,
) -> list[TriangularFuzzyNumber]:
    """Apply Chen-style linear normalization to one criterion.

    ``higher`` is the project's benefit-to-priority orientation. ``lower`` is
    the cost orientation. The formulas preserve TFN ordering and require a
    strictly positive denominator; zero-capacity/zero-cost cases are rejected
    rather than silently repaired.
    """

    _validate_criterion_values(values)
    if priority not in ("higher", "lower"):
        raise ValueError("priority must be 'higher' or 'lower'")

    if priority == "higher":
        denominator = max(value.upper for value in values)
        if denominator <= ZERO:
            raise ValueError("benefit normalization requires a positive upper maximum")
        return [
            TriangularFuzzyNumber(
                value.lower / denominator,
                value.modal / denominator,
                value.upper / denominator,
            )
            for value in values
        ]

    denominator = min(value.lower for value in values)
    if denominator <= ZERO:
        raise ValueError("cost normalization requires a positive lower minimum")
    return [
        TriangularFuzzyNumber(
            denominator / value.upper,
            denominator / value.modal,
            denominator / value.lower,
        )
        for value in values
    ]


def validate_crisp_weights(
    criterion_names: set[str],
    weights: dict[str, Decimal],
) -> None:
    """Validate explicit non-negative crisp weights summing exactly to one."""

    if not criterion_names:
        raise ValueError("at least one criterion is required")
    if set(weights) != criterion_names:
        raise ValueError("weights must be supplied for exactly the criteria")
    for name, weight in weights.items():
        if not isinstance(weight, Decimal) or not weight.is_finite():
            raise ValueError(f"weight {name!r} must be a finite Decimal")
        if weight < ZERO:
            raise ValueError(f"weight {name!r} cannot be negative")
    if sum(weights.values(), ZERO) != ONE:
        raise ValueError("weights must sum exactly to 1")


def weighted_normalized_matrix(
    normalized_criteria: dict[str, list[TriangularFuzzyNumber]],
    weights: dict[str, Decimal],
) -> dict[str, list[TriangularFuzzyNumber]]:
    """Apply explicit crisp weights to a normalized fuzzy decision matrix."""

    if not normalized_criteria:
        raise ValueError("at least one criterion is required")
    validate_crisp_weights(set(normalized_criteria), weights)
    for name, values in normalized_criteria.items():
        _validate_criterion_values(values)
        if any(value.upper > ONE for value in values):
            raise ValueError(f"normalized criterion {name!r} must be within [0, 1]")
    lengths = {len(values) for values in normalized_criteria.values()}
    if len(lengths) != 1:
        raise ValueError("all criteria must contain the same number of alternatives")
    return {
        name: [value * weights[name] for value in values]
        for name, values in normalized_criteria.items()
    }


def fuzzy_ideal_solutions(
    weighted_matrix: dict[str, list[TriangularFuzzyNumber]],
) -> tuple[dict[str, TriangularFuzzyNumber], dict[str, TriangularFuzzyNumber]]:
    """Return componentwise FPIS/FNIS from the weighted matrix.

    All criteria reaching this function have already been oriented as
    benefit-to-priority criteria. The positive ideal is therefore the
    componentwise maximum and the negative ideal the componentwise minimum
    across alternatives. This keeps ideals on the same weighted scale as the
    matrix; it is the selected project adaptation rather than a claim that the
    fixed Chen-style ``(1,1,1)/(0,0,0)`` convention is being used.
    """

    if not weighted_matrix:
        raise ValueError("weighted matrix cannot be empty")
    for values in weighted_matrix.values():
        _validate_criterion_values(values)
    lengths = {len(values) for values in weighted_matrix.values()}
    if len(lengths) != 1:
        raise ValueError("all criteria must contain the same number of alternatives")
    positive: dict[str, TriangularFuzzyNumber] = {}
    negative: dict[str, TriangularFuzzyNumber] = {}
    for name, values in weighted_matrix.items():
        positive[name] = TriangularFuzzyNumber(
            max(value.lower for value in values),
            max(value.modal for value in values),
            max(value.upper for value in values),
        )
        negative[name] = TriangularFuzzyNumber(
            min(value.lower for value in values),
            min(value.modal for value in values),
            min(value.upper for value in values),
        )
    return positive, negative


def vertex_distance(left: TriangularFuzzyNumber, right: TriangularFuzzyNumber) -> Decimal:
    """Return Chen's Euclidean vertex distance between two TFNs."""

    if not isinstance(left, TriangularFuzzyNumber) or not isinstance(right, TriangularFuzzyNumber):
        raise ValueError("distance arguments must be triangular fuzzy numbers")
    squared = (
        (left.lower - right.lower) ** 2
        + (left.modal - right.modal) ** 2
        + (left.upper - right.upper) ** 2
    )
    return (squared / Decimal("3")).sqrt()


def closeness_coefficients(
    weighted_matrix: dict[str, list[TriangularFuzzyNumber]],
) -> list[Decimal]:
    """Calculate coefficients using summed criterion distances.

    This uses the project-specific additive aggregation across criteria. A
    zero denominator is undefined and raises an error rather than fabricating a
    tie or a coefficient.
    """

    positive, negative = fuzzy_ideal_solutions(weighted_matrix)
    lengths = {len(values) for values in weighted_matrix.values()}
    if len(lengths) != 1:
        raise ValueError("all criteria must contain the same number of alternatives")
    count = next(iter(lengths))
    coefficients: list[Decimal] = []
    for index in range(count):
        distance_positive = sum(
            (vertex_distance(values[index], positive[name]) for name, values in weighted_matrix.items()),
            ZERO,
        )
        distance_negative = sum(
            (vertex_distance(values[index], negative[name]) for name, values in weighted_matrix.items()),
            ZERO,
        )
        denominator = distance_positive + distance_negative
        if denominator == ZERO:
            raise ValueError(f"closeness coefficient is undefined for alternative {index}")
        coefficients.append(distance_negative / denominator)
    return coefficients


def rank_by_closeness(coefficients: list[Decimal]) -> list[int]:
    """Return zero-based alternative indices in descending coefficient order."""

    if not coefficients:
        raise ValueError("coefficients cannot be empty")
    if any(
        not isinstance(value, Decimal)
        or not value.is_finite()
        or value < ZERO
        or value > ONE
        for value in coefficients
    ):
        raise ValueError("coefficients must be finite values in [0, 1]")
    return sorted(range(len(coefficients)), key=lambda index: (-coefficients[index], index))

"""Opt-in mathematical primitives; no research weights or aggregation defaults."""

from __future__ import annotations

from decimal import Decimal
from typing import Literal

DirectionOfPriority = Literal["higher", "lower"]


def min_max_normalize(values: list[Decimal], priority: DirectionOfPriority) -> list[Decimal]:
    """Normalize one criterion after the caller explicitly chooses its direction."""

    if not values:
        raise ValueError("cannot normalize an empty criterion")
    if priority not in ("higher", "lower"):
        raise ValueError("priority must be 'higher' or 'lower'")
    if any(not value.is_finite() for value in values):
        raise ValueError("criterion contains a non-finite value")
    low, high = min(values), max(values)
    if high == low:
        return [Decimal("0") for _ in values]
    span = high - low
    result = [(value - low) / span for value in values]
    if priority == "lower":
        result = [Decimal("1") - value for value in result]
    return result


def weighted_sum(
    normalized_criteria: dict[str, list[Decimal]],
    weights: dict[str, Decimal],
) -> list[Decimal]:
    """Combine already-normalized criteria using explicit caller-supplied weights.

    This function intentionally has no default weights, period aggregation, or
    direction aggregation. It is not called by the data-loading path.
    """

    if not normalized_criteria:
        raise ValueError("at least one criterion is required")
    if set(normalized_criteria) != set(weights):
        raise ValueError("weights must be supplied for exactly the normalized criteria")
    if any(not values for values in normalized_criteria.values()):
        raise ValueError("criterion lists cannot be empty")
    lengths = {len(values) for values in normalized_criteria.values()}
    if len(lengths) != 1:
        raise ValueError("all criteria must contain the same number of alternatives")
    for name, values in normalized_criteria.items():
        for value in values:
            if not value.is_finite():
                raise ValueError(f"normalized criterion {name!r} contains a non-finite value")
            if value < Decimal("0") or value > Decimal("1"):
                raise ValueError(f"normalized criterion {name!r} contains a value outside [0, 1]")
    for name, weight in weights.items():
        if not weight.is_finite():
            raise ValueError(f"weight {name!r} must be finite")
        if weight < Decimal("0"):
            raise ValueError(f"weight {name!r} cannot be negative")
    if sum(weights.values(), Decimal("0")) != Decimal("1"):
        raise ValueError("weights must sum exactly to 1")
    return [
        sum((normalized_criteria[name][index] * weights[name] for name in normalized_criteria), Decimal("0"))
        for index in range(next(iter(lengths)))
    ]

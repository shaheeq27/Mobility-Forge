"""Research-backed, dependency-free MobilityForge engine primitives."""

from .loader import DEFAULT_DATASET, load_observations
from .fuzzy_topsis import (
    TriangularFuzzyNumber,
    closeness_coefficients,
    fuzzy_ideal_solutions,
    normalize_fuzzy_criterion,
    rank_by_closeness,
    vertex_distance,
    weighted_normalized_matrix,
)
from .models import Direction, Period, SectionObservation
from .validation import ValidationIssue, validate_observations

__all__ = [
    "DEFAULT_DATASET",
    "Direction",
    "Period",
    "SectionObservation",
    "ValidationIssue",
    "load_observations",
    "validate_observations",
    "TriangularFuzzyNumber",
    "normalize_fuzzy_criterion",
    "weighted_normalized_matrix",
    "fuzzy_ideal_solutions",
    "vertex_distance",
    "closeness_coefficients",
    "rank_by_closeness",
]

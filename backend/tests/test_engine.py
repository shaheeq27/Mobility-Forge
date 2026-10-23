from decimal import Decimal
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest

from mobility_engine.loader import load_observations
from mobility_engine.models import Direction, Period
from mobility_engine.fuzzy_topsis import (
    TriangularFuzzyNumber,
    closeness_coefficients,
    fuzzy_ideal_solutions,
    normalize_fuzzy_criterion,
    rank_by_closeness,
    vertex_distance,
    weighted_normalized_matrix,
)
from mobility_engine.scoring import min_max_normalize, weighted_sum
from mobility_engine.validation import validate_observations
from mobility_engine.decision_service import run_fuzzy_topsis
from mobility_engine.models import SectionObservation


ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "data" / "extracted" / "bbmp_tumkur_midblock_vc_los_table8.csv"


class EngineTests(unittest.TestCase):
    def _synthetic_slice(self, period=Period.MORNING, direction=Direction.YESHWANTHPUR):
        return [
            SectionObservation(46, index, name, "synthetic", period, direction, Decimal(str(index)), Decimal(str(index) + ".1"), "C")
            for index, name in enumerate((
                "Yeshwanthpur TTMC", "Yeshwanthpur Skywalk",
                "Tumkur Road (Between Gorguntepalya-SRS)",
                "Tumkur Road (Between SRS-Jalahalli Junction)",
                "Tumkur Road (Between Jalahalli junction-Hesarghatta Junction)",
                "Tumkur Road (Between Hesarghatta Junction-Nagasandra)",
            ), start=1)
        ]

    def test_decision_service_runs_one_period_and_direction_without_aggregation(self):
        result = run_fuzzy_topsis(self._synthetic_slice(), Period.MORNING, Direction.YESHWANTHPUR, {"pcu": Decimal("0.5"), "vc": Decimal("0.5")})
        self.assertEqual(len(result.alternatives), 6)
        self.assertEqual({item.observation.period for item in result.alternatives}, {Period.MORNING})
        self.assertEqual({item.observation.direction for item in result.alternatives}, {Direction.YESHWANTHPUR})
        self.assertEqual([item.rank for item in result.alternatives], [6, 5, 4, 3, 2, 1])
        for item in result.alternatives:
            self.assertEqual(item.closeness_coefficient, item.distance_negative / (item.distance_positive + item.distance_negative))
            self.assertEqual(item.normalized["pcu"].upper, Decimal("1") if item.observation.section_no == 6 else Decimal(item.observation.section_no) / Decimal("6"))

    def test_decision_service_supports_each_separate_period_direction_run(self):
        for period in Period:
            for direction in Direction:
                with self.subTest(period=period, direction=direction):
                    result = run_fuzzy_topsis(self._synthetic_slice(period, direction), period, direction, {"pcu": Decimal("0.5"), "vc": Decimal("0.5")})
                    self.assertEqual(len(result.alternatives), 6)

    def test_decision_service_rejects_duplicate_or_mixed_slice(self):
        values = self._synthetic_slice()
        with self.assertRaisesRegex(ValueError, "duplicate alternative"):
            run_fuzzy_topsis(values + [values[0]], Period.MORNING, Direction.YESHWANTHPUR, {"pcu": Decimal("0.5"), "vc": Decimal("0.5")})
        mixed = list(values)
        mixed[0] = replace(mixed[0], direction=Direction.NAGASANDRA)
        with self.assertRaisesRegex(ValueError, "exactly one"):
            run_fuzzy_topsis(mixed, Period.MORNING, Direction.YESHWANTHPUR, {"pcu": Decimal("0.5"), "vc": Decimal("0.5")})

    def test_decision_service_rejects_invalid_observation_values(self):
        values = self._synthetic_slice()
        values[0] = replace(values[0], volume_pcu=Decimal("0"))
        with self.assertRaisesRegex(ValueError, "invalid PCU"):
            run_fuzzy_topsis(values, Period.MORNING, Direction.YESHWANTHPUR, {"pcu": Decimal("0.5"), "vc": Decimal("0.5")})
        values = self._synthetic_slice()
        values[0] = replace(values[0], vc_ratio=Decimal("-0.1"))
        with self.assertRaisesRegex(ValueError, "invalid V/C"):
            run_fuzzy_topsis(values, Period.MORNING, Direction.YESHWANTHPUR, {"pcu": Decimal("0.5"), "vc": Decimal("0.5")})
    def test_source_csv_loads_without_aggregation(self):
        observations = load_observations(CSV)
        self.assertEqual(len(observations), 24)
        self.assertEqual(len({item.road_section for item in observations}), 6)
        self.assertEqual({item.period for item in observations}, {Period.MORNING, Period.EVENING})
        self.assertEqual({item.direction for item in observations}, {Direction.YESHWANTHPUR, Direction.NAGASANDRA})
        self.assertEqual(observations[0].volume_pcu, Decimal("3407"))
        self.assertEqual(observations[0].vc_ratio, Decimal("1.26"))

    def test_source_csv_passes_integrity_validation(self):
        self.assertEqual(validate_observations(load_observations(CSV)), [])

    def test_missing_values_are_rejected(self):
        observations = load_observations(CSV)
        broken = observations[:-1]
        issues = validate_observations(broken)
        self.assertTrue(any(issue.code == "row_count" for issue in issues))
        self.assertTrue(any(issue.code == "missing_observations" for issue in issues))

    def test_incorrect_section_number_name_mapping_is_rejected(self):
        observations = load_observations(CSV)
        broken = list(observations)
        broken[0] = replace(broken[0], section_no=2)
        issues = validate_observations(broken)
        codes = {issue.code for issue in issues}
        self.assertIn("section_mapping", codes)
        self.assertIn("section_mapping_conflict", codes)
        self.assertIn("section_mapping_duplicate", codes)

    def test_invalid_ranges_and_los_are_rejected(self):
        observations = load_observations(CSV)
        broken = list(observations)
        broken[0] = broken[0].__class__(**{**broken[0].__dict__, "volume_pcu": Decimal("0"), "vc_ratio": Decimal("-0.1"), "los": "Z"})
        codes = {issue.code for issue in validate_observations(broken)}
        self.assertTrue({"volume_range", "vc_range", "los_value"}.issubset(codes))

    def test_normalization_requires_explicit_direction(self):
        values = [Decimal("2"), Decimal("4"), Decimal("6")]
        self.assertEqual(min_max_normalize(values, "higher"), [Decimal("0"), Decimal("0.5"), Decimal("1")])
        self.assertEqual(min_max_normalize(values, "lower"), [Decimal("1"), Decimal("0.5"), Decimal("0")])

    def test_weighted_sum_requires_explicit_valid_weights(self):
        criteria = {"volume": [Decimal("0"), Decimal("1")], "vc": [Decimal("1"), Decimal("0")]}
        self.assertEqual(weighted_sum(criteria, {"volume": Decimal("0.5"), "vc": Decimal("0.5")}), [Decimal("0.5"), Decimal("0.5")])
        with self.assertRaises(ValueError):
            weighted_sum(criteria, {"volume": Decimal("1")})

    def test_weighted_sum_rejects_empty_criteria(self):
        with self.assertRaisesRegex(ValueError, "criterion lists cannot be empty"):
            weighted_sum({"volume": [], "vc": []}, {"volume": Decimal("0.5"), "vc": Decimal("0.5")})

    def test_weighted_sum_rejects_mismatched_alternative_counts(self):
        with self.assertRaisesRegex(ValueError, "same number of alternatives"):
            weighted_sum(
                {"volume": [Decimal("0"), Decimal("1")], "vc": [Decimal("0")]},
                {"volume": Decimal("0.5"), "vc": Decimal("0.5")},
            )

    def test_weighted_sum_rejects_invalid_normalized_values(self):
        weights = {"volume": Decimal("0.5"), "vc": Decimal("0.5")}
        with self.assertRaisesRegex(ValueError, r"outside \[0, 1\]"):
            weighted_sum({"volume": [Decimal("-0.1")], "vc": [Decimal("0.5")]}, weights)
        with self.assertRaisesRegex(ValueError, r"outside \[0, 1\]"):
            weighted_sum({"volume": [Decimal("1.1")], "vc": [Decimal("0.5")]}, weights)
        with self.assertRaisesRegex(ValueError, "non-finite"):
            weighted_sum({"volume": [Decimal("NaN")], "vc": [Decimal("0.5")]}, weights)

    def test_weighted_sum_rejects_invalid_weights(self):
        criteria = {"volume": [Decimal("0.5")], "vc": [Decimal("0.5")]}
        with self.assertRaisesRegex(ValueError, "cannot be negative"):
            weighted_sum(criteria, {"volume": Decimal("-0.1"), "vc": Decimal("1.1")})
        with self.assertRaisesRegex(ValueError, "must be finite"):
            weighted_sum(criteria, {"volume": Decimal("NaN"), "vc": Decimal("1")})
        with self.assertRaisesRegex(ValueError, "sum exactly to 1"):
            weighted_sum(criteria, {"volume": Decimal("0.4"), "vc": Decimal("0.4")})

    def test_loader_rejects_missing_required_column(self):
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as handle:
            handle.write("source_page\n46\n")
            path = handle.name
        try:
            with self.assertRaises(ValueError):
                load_observations(path)
        finally:
            Path(path).unlink()

    def test_tfn_validation_and_scalar_arithmetic(self):
        value = TriangularFuzzyNumber(Decimal("1"), Decimal("2"), Decimal("4"))
        self.assertEqual(value * Decimal("0.5"), TriangularFuzzyNumber(Decimal("0.5"), Decimal("1"), Decimal("2")))
        with self.assertRaisesRegex(ValueError, "lower <= modal"):
            TriangularFuzzyNumber(Decimal("2"), Decimal("1"), Decimal("3"))
        with self.assertRaisesRegex(ValueError, "non-negative"):
            TriangularFuzzyNumber(Decimal("-1"), Decimal("0"), Decimal("1"))
        with self.assertRaisesRegex(ValueError, "finite"):
            TriangularFuzzyNumber(Decimal("NaN"), Decimal("1"), Decimal("2"))

    def test_vertex_distance_matches_hand_calculation(self):
        left = TriangularFuzzyNumber(Decimal("0"), Decimal("0"), Decimal("0"))
        right = TriangularFuzzyNumber(Decimal("1"), Decimal("1"), Decimal("1"))
        self.assertEqual(vertex_distance(left, right), Decimal("1"))

    def test_benefit_and_cost_normalization(self):
        values = [
            TriangularFuzzyNumber(Decimal("1"), Decimal("2"), Decimal("4")),
            TriangularFuzzyNumber(Decimal("2"), Decimal("4"), Decimal("8")),
        ]
        self.assertEqual(
            normalize_fuzzy_criterion(values, "higher"),
            [
                TriangularFuzzyNumber(Decimal("0.125"), Decimal("0.25"), Decimal("0.5")),
                TriangularFuzzyNumber(Decimal("0.25"), Decimal("0.5"), Decimal("1")),
            ],
        )
        costs = [
            TriangularFuzzyNumber(Decimal("2"), Decimal("4"), Decimal("6")),
            TriangularFuzzyNumber(Decimal("4"), Decimal("6"), Decimal("8")),
        ]
        self.assertEqual(
            normalize_fuzzy_criterion(costs, "lower"),
            [
                TriangularFuzzyNumber(Decimal(1) / Decimal(3), Decimal("0.5"), Decimal("1")),
                TriangularFuzzyNumber(Decimal("0.25"), Decimal(Decimal(1) / Decimal(3)), Decimal("0.5")),
            ],
        )

    def test_normalization_rejects_empty_and_zero_denominator(self):
        with self.assertRaisesRegex(ValueError, "cannot be empty"):
            normalize_fuzzy_criterion([], "higher")
        zero = [TriangularFuzzyNumber(Decimal("0"), Decimal("0"), Decimal("0"))]
        with self.assertRaisesRegex(ValueError, "positive upper maximum"):
            normalize_fuzzy_criterion(zero, "higher")
        with self.assertRaisesRegex(ValueError, "positive lower minimum"):
            normalize_fuzzy_criterion(zero, "lower")

    def test_weighted_matrix_and_ideal_solutions(self):
        matrix = {
            "volume": [
                TriangularFuzzyNumber(Decimal("0"), Decimal("0.5"), Decimal("1")),
                TriangularFuzzyNumber(Decimal("0.25"), Decimal("0.5"), Decimal("0.75")),
            ],
            "vc": [
                TriangularFuzzyNumber(Decimal("0"), Decimal("0.25"), Decimal("0.5")),
                TriangularFuzzyNumber(Decimal("0.5"), Decimal("0.75"), Decimal("1")),
            ],
        }
        weighted = weighted_normalized_matrix(matrix, {"volume": Decimal("0.5"), "vc": Decimal("0.5")})
        self.assertEqual(weighted["volume"][0].modal, Decimal("0.25"))
        positive, negative = fuzzy_ideal_solutions(weighted)
        self.assertEqual(positive["volume"], TriangularFuzzyNumber(Decimal("0.125"), Decimal("0.25"), Decimal("0.5")))
        self.assertEqual(negative["vc"], TriangularFuzzyNumber(Decimal("0"), Decimal("0.125"), Decimal("0.25")))

    def test_weighted_matrix_rejects_mismatches_and_invalid_weights(self):
        value = TriangularFuzzyNumber(Decimal("0"), Decimal("0"), Decimal("1"))
        with self.assertRaisesRegex(ValueError, "same number"):
            weighted_normalized_matrix({"volume": [value], "vc": [value, value]}, {"volume": Decimal("0.5"), "vc": Decimal("0.5")})
        with self.assertRaisesRegex(ValueError, "sum exactly"):
            weighted_normalized_matrix({"volume": [value], "vc": [value]}, {"volume": Decimal("0.4"), "vc": Decimal("0.4")})
        with self.assertRaisesRegex(ValueError, "cannot be negative"):
            weighted_normalized_matrix({"volume": [value], "vc": [value]}, {"volume": Decimal("-0.1"), "vc": Decimal("1.1")})
        out_of_range = TriangularFuzzyNumber(Decimal("0"), Decimal("1"), Decimal("2"))
        with self.assertRaisesRegex(ValueError, r"within \[0, 1\]"):
            weighted_normalized_matrix({"volume": [out_of_range], "vc": [value]}, {"volume": Decimal("0.5"), "vc": Decimal("0.5")})

    def test_zero_weight_criterion_contributes_zero(self):
        values = [
            TriangularFuzzyNumber(Decimal("0.2"), Decimal("0.4"), Decimal("0.8")),
            TriangularFuzzyNumber(Decimal("0.5"), Decimal("0.6"), Decimal("1")),
        ]
        weighted = weighted_normalized_matrix(
            {"pcu": values, "vc": values},
            {"pcu": Decimal("1"), "vc": Decimal("0")},
        )
        self.assertEqual(
            weighted["vc"],
            [
                TriangularFuzzyNumber(Decimal("0"), Decimal("0"), Decimal("0")),
                TriangularFuzzyNumber(Decimal("0"), Decimal("0"), Decimal("0")),
            ],
        )

    def test_singleton_tfn_pipeline(self):
        normalized = normalize_fuzzy_criterion(
            [
                TriangularFuzzyNumber(Decimal("2"), Decimal("2"), Decimal("2")),
                TriangularFuzzyNumber(Decimal("4"), Decimal("4"), Decimal("4")),
            ],
            "higher",
        )
        self.assertEqual(
            normalized,
            [
                TriangularFuzzyNumber(Decimal("0.5"), Decimal("0.5"), Decimal("0.5")),
                TriangularFuzzyNumber(Decimal("1"), Decimal("1"), Decimal("1")),
            ],
        )
        weighted = weighted_normalized_matrix({"pcu": normalized}, {"pcu": Decimal("1")})
        self.assertEqual(vertex_distance(weighted["pcu"][0], weighted["pcu"][1]), Decimal("0.5"))
        self.assertEqual(closeness_coefficients(weighted), [Decimal("0"), Decimal("1")])

    def test_single_criterion_weight_scenarios_are_evaluable_with_synthetic_data(self):
        synthetic = {
            "pcu": [
                TriangularFuzzyNumber(Decimal("0"), Decimal("0"), Decimal("0")),
                TriangularFuzzyNumber(Decimal("1"), Decimal("1"), Decimal("1")),
            ],
            "vc": [
                TriangularFuzzyNumber(Decimal("1"), Decimal("1"), Decimal("1")),
                TriangularFuzzyNumber(Decimal("0"), Decimal("0"), Decimal("0")),
            ],
        }
        pcu_only = weighted_normalized_matrix(
            synthetic,
            {"pcu": Decimal("1"), "vc": Decimal("0")},
        )
        vc_only = weighted_normalized_matrix(
            synthetic,
            {"pcu": Decimal("0"), "vc": Decimal("1")},
        )
        self.assertEqual(closeness_coefficients(pcu_only), [Decimal("0"), Decimal("1")])
        self.assertEqual(closeness_coefficients(vc_only), [Decimal("1"), Decimal("0")])

    def test_closeness_coefficients_and_tie_order(self):
        weighted = {
            "volume": [
                TriangularFuzzyNumber(Decimal("1"), Decimal("1"), Decimal("1")),
                TriangularFuzzyNumber(Decimal("0"), Decimal("0"), Decimal("0")),
            ],
            "vc": [
                TriangularFuzzyNumber(Decimal("0"), Decimal("0"), Decimal("0")),
                TriangularFuzzyNumber(Decimal("1"), Decimal("1"), Decimal("1")),
            ],
        }
        coefficients = closeness_coefficients(weighted)
        self.assertEqual(coefficients, [Decimal("0.5"), Decimal("0.5")])
        self.assertEqual(rank_by_closeness(coefficients), [0, 1])
        with self.assertRaisesRegex(ValueError, "undefined"):
            closeness_coefficients({"volume": [TriangularFuzzyNumber(Decimal("0"), Decimal("0"), Decimal("0"))]})

    def test_end_to_end_weighted_matrix_ideals_distances_and_closeness(self):
        """Synthetic three-alternative example; no research data are used."""
        normalized = {
            "volume": [
                TriangularFuzzyNumber(Decimal("0.2"), Decimal("0.2"), Decimal("0.2")),
                TriangularFuzzyNumber(Decimal("0.8"), Decimal("0.8"), Decimal("0.8")),
                TriangularFuzzyNumber(Decimal("1"), Decimal("1"), Decimal("1")),
            ],
            "vc": [
                TriangularFuzzyNumber(Decimal("0.8"), Decimal("0.8"), Decimal("0.8")),
                TriangularFuzzyNumber(Decimal("0.4"), Decimal("0.4"), Decimal("0.4")),
                TriangularFuzzyNumber(Decimal("0"), Decimal("0"), Decimal("0")),
            ],
        }
        weighted = weighted_normalized_matrix(
            normalized,
            {"volume": Decimal("0.6"), "vc": Decimal("0.4")},
        )
        positive, negative = fuzzy_ideal_solutions(weighted)
        self.assertEqual(positive["volume"], TriangularFuzzyNumber(Decimal("0.6"), Decimal("0.6"), Decimal("0.6")))
        self.assertEqual(positive["vc"], TriangularFuzzyNumber(Decimal("0.32"), Decimal("0.32"), Decimal("0.32")))
        self.assertEqual(negative["volume"], TriangularFuzzyNumber(Decimal("0.12"), Decimal("0.12"), Decimal("0.12")))
        self.assertEqual(negative["vc"], TriangularFuzzyNumber(Decimal("0"), Decimal("0"), Decimal("0")))
        coefficients = closeness_coefficients(weighted)
        self.assertEqual(coefficients, [Decimal("0.4"), Decimal("0.65"), Decimal("0.6")])
        self.assertEqual(rank_by_closeness(coefficients), [1, 2, 0])


if __name__ == "__main__":
    unittest.main()

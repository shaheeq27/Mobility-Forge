from decimal import Decimal
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest

from mobility_engine.loader import load_observations
from mobility_engine.models import Direction, Period
from mobility_engine.scoring import min_max_normalize, weighted_sum
from mobility_engine.validation import validate_observations


ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "data" / "extracted" / "bbmp_tumkur_midblock_vc_los_table8.csv"


class EngineTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()

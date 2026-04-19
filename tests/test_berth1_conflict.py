import csv
import tempfile
import unittest
from pathlib import Path

from os_cmasp.berth1_conflict import (
    ABLATION_CONDITIONS,
    LatentState,
    chi_b1,
    evaluate_bank,
    generate_episode_bank,
    load_replay_bank,
    paired_deltas,
    validate_bank,
    write_replay_template,
)


class Berth1ConflictContractTests(unittest.TestCase):
    def test_chi_excludes_hidden_precondition_truth(self):
        x_ready = LatentState(True, True, True, True)
        x_not_ready = LatentState(False, True, True, True)
        self.assertEqual(chi_b1(x_ready), chi_b1(x_not_ready))

    def test_preflight_bank_validates(self):
        bank = generate_episode_bank("mixed", horizon=8, seeds=3, p_all_clear=0.5)
        report = validate_bank(bank)
        self.assertEqual(report["steps"], 24)
        self.assertEqual(report["seeds"], 3)
        self.assertEqual(report["conditions"], ABLATION_CONDITIONS)
        self.assertTrue(report["leakage_guard"]["chi_equal_for_ready_pair"])

    def test_replay_template_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "template.csv"
            write_replay_template(str(path))
            bank = load_replay_bank(str(path))
            self.assertEqual(len(bank), 1)
            self.assertEqual(bank[0].seed, 0)
            self.assertEqual(bank[0].t, 0)
            self.assertGreaterEqual(len(bank[0].claims), 2)

    def test_replay_template_has_required_columns(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "template.csv"
            write_replay_template(str(path))
            with path.open(newline="") as f:
                reader = csv.DictReader(f)
                self.assertIsNotNone(reader.fieldnames)
                fields = set(reader.fieldnames or [])
            for required in ["seed", "t", "ready", "scenario", "prop", "value", "observer", "situation"]:
                self.assertIn(required, fields)

    def test_paired_ablation_row_shape(self):
        bank = generate_episode_bank("mixed", horizon=4, seeds=2, p_all_clear=0.5)
        rows = evaluate_bank(bank, ABLATION_CONDITIONS)
        self.assertEqual(len(rows), 4 * 2 * len(ABLATION_CONDITIONS))
        deltas = paired_deltas(rows)
        self.assertTrue(any(d["condition"] == "provenance_erased" for d in deltas))


if __name__ == "__main__":
    unittest.main()

import csv
import tempfile
import unittest
from pathlib import Path

from os_cmasp.berth1_conflict import load_replay_bank, validate_bank
from os_cmasp.berth1_replay_adapter import convert_wide, inspect_wide, normalize_long


class Berth1ReplayAdapterTests(unittest.TestCase):
    def test_from_wide_generates_valid_long_replay(self):
        with tempfile.TemporaryDirectory() as tmp:
            wide = Path(tmp) / "wide.csv"
            out = Path(tmp) / "replay.csv"
            wide.write_text(
                "seed,t,ready,scenario,crane_ok,eta_on_time,weather_safe,queue_state,weather_regime,disruption_family,vessel_class,operating_mode,time_bucket,berth_slot,eta_bin\n"
                "0,0,true,authority_conflict,true,true,true,normal,clear,none,feeder,nominal,day,slot-A,on-window\n"
                "0,1,false,human_override,true,true,false,normal,wind,weather,feeder,nominal,day,slot-A,on-window\n"
            )
            payload = convert_wide(str(wide), str(out))
            self.assertEqual(payload["mode"], "from-wide")
            bank = load_replay_bank(str(out))
            report = validate_bank(bank)
            self.assertEqual(report["steps"], 2)
            self.assertEqual(report["unknown_props"], [])
            self.assertEqual(report["unknown_observers"], [])


    def test_inspect_wide_accepts_common_aliases(self):
        with tempfile.TemporaryDirectory() as tmp:
            wide = Path(tmp) / "aliased_wide.csv"
            out = Path(tmp) / "replay.csv"
            wide.write_text(
                "episode_id,step,berth_ready,scenario_family,crane_available,arrival_on_time,weather_ok\n"
                "0,0,true,authority_conflict,true,true,true\n"
            )
            report = inspect_wide(str(wide))
            self.assertTrue(report["convertible_without_manual_rename"])
            self.assertEqual(report["recognized_required_columns"]["ready"], "berth_ready")
            payload = convert_wide(str(wide), str(out))
            self.assertEqual(payload["bank_report"]["steps"], 1)

    def test_normalize_long_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            wide = Path(tmp) / "wide.csv"
            replay = Path(tmp) / "replay.csv"
            normalized = Path(tmp) / "normalized.csv"
            wide.write_text("seed,t,ready,scenario\n0,0,true,authority_conflict\n")
            convert_wide(str(wide), str(replay))
            payload = normalize_long(str(replay), str(normalized))
            self.assertEqual(payload["mode"], "validate")
            with normalized.open(newline="") as f:
                reader = csv.DictReader(f)
                self.assertIn("observer", reader.fieldnames or [])


if __name__ == "__main__":
    unittest.main()

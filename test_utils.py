"""
File: test_utils.py
Author: Guy Matz
Email: gmatz@matz.org
Github: https://www.github.com/guymatz/
Description: Tests for utils.py
"""

import json
import unittest
import os

from utils import _calc_ibi


# pylint: disable=too-many-instance-attributes
class TestUtils(unittest.TestCase):
    """Tests for max_interval.py

    Spike Train compareed against output from
    using https://github.com/igm-team/meaRtools/blob/master/meaRtools/R/burst_stats.R
    as ref
    """

    def setUp(self) -> None:
        test_data_dir = "tests/data"
        test_data_file = os.path.join(test_data_dir, "cult.json")
        self.test_bursts = os.path.join(test_data_dir, "bursts_stage3.json")
        self.test_spikes = os.path.join(test_data_dir, "spikes_stage3.json")
        self.test_calc_ibis = os.path.join(test_data_dir, "ibi2_stage3.json")

        self.sampling_rate: int = 1000
        self.max_begin_isi: float = 0.17
        self.max_end_isi: float = 0.3
        self.min_burst_duration: float = 0.01
        self.min_ibi: float = 0.4
        self.min_spikes_in_burst: int = 3

        self.spike_train: list[float] = []
        with open(test_data_file, encoding="utf-8") as f:
            self.spike_train = json.load(f)

    def tearDown(self) -> None:
        pass

    def test_calc_ibi(self) -> None:
        """Test _calc_ibi method against output from reference"""
        with open(self.test_bursts, encoding="utf-8") as f:
            bursts_baseline = json.load(f)
        with open(self.test_spikes, encoding="utf-8") as f:
            spikes_baseline = json.load(f)
        with open(self.test_calc_ibis, encoding="utf-8") as f:
            test_calc_ibi_baseline = json.load(f)

        ibis: list[float | None] = _calc_ibi(spikes_baseline, bursts_baseline)
        self.assertEqual(len(ibis), len(test_calc_ibi_baseline))
        for n in range(1, len(ibis)):
            self.assertAlmostEqual(ibis[n], test_calc_ibi_baseline[n], 6)

    # Source - https://stackoverflow.com/a/8312110
    # pylint: disable=invalid-name
    def assertListAlmostEqual(self, list1, list2, places):
        """Check List of floats are equal within some tolerance"""

        self.assertEqual(len(list1), len(list2))
        for a, b in zip(list1, list2):
            self.assertAlmostEqual(a, b, places)


if __name__ == "__main__":
    unittest.main()

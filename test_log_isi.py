"""
File: test_log_isi.py
Author: Guy Matz
Email: gmatz@matz.org
Github: https://www.github.com/guymatz/
Description: tests for log_isi.py
"""

import json
import unittest
import os

from log_isi import _find_burst


# pylint: disable=too-many-instance-attributes
class TestLogISI(unittest.TestCase):
    """Tests for log_isi.py

    Spike Train compareed against output from
    using https://github.com/igm-team/meaRtools/blob/master/meaRtools/R/logisi_pasq_method.R
    as reference
    """

    def setUp(self) -> None:
        test_data_dir = "data"
        test_data_file = os.path.join(test_data_dir, "cult.json")
        self.test_burst_detection_baseline = os.path.join(test_data_dir, "bursts.json")
        self.test_merge_bursts_baseline = os.path.join(
            test_data_dir, "merged_bursts.json"
        )
        self.test_quality_control_baseline = os.path.join(
            test_data_dir, "quality_control.json"
        )

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

    def test_find_burst(self) -> None:
        """Test _find_burst method against output from reference"""
        with open(self.test_burst_detection_baseline, encoding="utf-8") as f:
            burst_detection_baseline = json.load(f)

        bursts: list[list[float]] = _burst_detection(
            self.spike_train, self.max_begin_isi, self.max_end_isi, self.sampling_rate
        )
        self.assertListEqual(burst_detection_baseline, bursts)

    # Source - https://stackoverflow.com/a/8312110
    # pylint: disable=invalid-name
    def assertListAlmostEqual(self, list1, list2, tol):
        """Check List of floats are equal within some tolerance"""

        self.assertEqual(len(list1), len(list2))
        for a, b in zip(list1, list2):
            self.assertAlmostEqual(a, b, tol)


if __name__ == "__main__":
    unittest.main()

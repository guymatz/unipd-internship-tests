"""
File: test_max_interval.py
Author: Guy Matz
Email: gmatz@matz.org
Github: https://www.github.com/guymatz/
Description: tests for max_interval.py
"""

import json
import unittest
import os

from max_interval import _burst_detection, _merge_bursts, _quality_control


# pylint: disable=too-many-instance-attributes
class TestMaxInterval(unittest.TestCase):
    """Tests for max_interval.py

    Spike Train compareed against output from
    using https://github.com/igm-team/meaRtools/blob/master/meaRtools/R/maxinterval.R
    as reference
    """

    def setUp(self) -> None:
        test_data_dir = "tests/data"
        # This datafile is in Experiments_neuronal_cultures/Data_AD/Alz_ab_m/Culture1REC1
        test_data_file = os.path.join(test_data_dir, "alz_ab_m_culture_c1r1.json")
        # mi == max_interval!
        self.test_burst_detection_baseline = os.path.join(
            test_data_dir, "mi_bursts.json"
        )
        self.test_merge_bursts_baseline = os.path.join(
            test_data_dir, "mi_merged_bursts.json"
        )
        self.test_quality_control_baseline = os.path.join(
            test_data_dir, "mi_quality_control.json"
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

    def test_burst_detection(self) -> None:
        """Test _burst_dection method against output from reference"""
        with open(self.test_burst_detection_baseline, encoding="utf-8") as f:
            burst_detection_baseline = json.load(f)

        bursts: list[list[float]] = _burst_detection(
            self.spike_train, self.max_begin_isi, self.max_end_isi, self.sampling_rate
        )
        self.assertListEqual(burst_detection_baseline, bursts)

    def test_merged_bursts(self) -> None:
        """Test _merged_bursts method against output from reference"""
        with open(self.test_merge_bursts_baseline, encoding="utf-8") as f:
            merged_bursts_baseline = json.load(f)

        bursts: list[list[float]] = _burst_detection(
            self.spike_train, self.max_begin_isi, self.max_end_isi, self.sampling_rate
        )
        merged_bursts: list[list[float]] = _merge_bursts(bursts, self.min_ibi)
        # Is there a better way to test list of list of floats?
        self.assertEqual(len(merged_bursts_baseline), len(merged_bursts))
        for n in range(1, len(merged_bursts_baseline)):
            self.assertListAlmostEqual(merged_bursts[n], merged_bursts_baseline[n], 3)

    def test_quality_control(self) -> None:
        """Test _quality_control method against output from reference"""
        with open(self.test_quality_control_baseline, encoding="utf-8") as f:
            quality_control_baseline = json.load(f)

        bursts: list[list[float]] = _burst_detection(
            self.spike_train, self.max_begin_isi, self.max_end_isi, self.sampling_rate
        )
        bursts = _merge_bursts(bursts, self.min_ibi)
        bursts = _quality_control(
            self.spike_train,
            self.sampling_rate,
            bursts,
            self.min_spikes_in_burst,
            self.min_burst_duration,
        )
        # breakpoint()
        for n in range(1, len(quality_control_baseline)):
            self.assertListAlmostEqual(bursts[n], quality_control_baseline[n], 3)

    # Source - https://stackoverflow.com/a/8312110
    # pylint: disable=invalid-name
    def assertListAlmostEqual(self, list1, list2, tol):
        """Check List of floats are equal within some tolerance"""

        self.assertEqual(len(list1), len(list2))
        for a, b in zip(list1, list2):
            self.assertAlmostEqual(a, b, tol)


if __name__ == "__main__":
    unittest.main()


if __name__ == "__main__":
    unittest.main()

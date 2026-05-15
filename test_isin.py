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

from isin import _get_lagged_diffs, _filter_within_isin


# pylint: disable=too-many-instance-attributes
class TestISIn(unittest.TestCase):
    """Tests for isin.py

    Spike Train compareed against output from
    using https://github.com/igm-team/meaRtools/blob/master/meaRtools/R/burst_stats.R
    as ref
    """

    def setUp(self) -> None:
        self.test_data_dir = "tests/data"
        # test_data_file = os.path.join(test_data_dir, "cult.json")
        self.test_spikes = os.path.join(self.test_data_dir, "short_spike_train.json")
        self.lagged_diffs = os.path.join(self.test_data_dir, "lagged_diffs_out.json")
        self.filtered_diffs = os.path.join(self.test_data_dir, "filtered_diffs_out.json")

        # self.max_begin_isi: float = 0.17
        # self.max_end_isi: float = 0.3
        # self.min_burst_duration: float = 0.01
        # self.min_ibi: float = 0.4
        # self.min_spikes_in_burst: int = 3

        self.spike_train: list[float] = []
        with open(self.test_spikes, encoding="utf-8") as f:
            self.spike_train = json.load(f)

    def tearDown(self) -> None:
        pass

    def test_get_lagged_diffs(self) -> None:
        """Testing portion of matlab code with the comment:
            % Look both directions from each spike
        """

        # test data was created with N=3
        test_diffs = _get_lagged_diffs(self.spike_train, 3)
        with open(self.lagged_diffs, encoding="utf-8") as f:
            good_diffs = json.load(f)
        for n in range(1, len(good_diffs)):
            self.assertListAlmostEqual(test_diffs[n], good_diffs[n], 3)

    def test_within_isin_filter(self) -> None:
        """Testing portion of matlab code with the comment:
            % Look both directions from each spike
        """

        # test data was created with N=3
        test_diffs = _get_lagged_diffs(self.spike_train, 3)
        # test data was created with ISIn = 8
        filtered_diffs = _filter_within_isin(test_diffs, 8)
        with open(self.filtered_diffs, encoding="utf-8") as f:
            test_filtered_diffs = json.load(f)
        for n in range(1, len(filtered_diffs)):
            self.assertListAlmostEqual(filtered_diffs[n], test_filtered_diffs[n], 3)

    # Source - https://stackoverflow.com/a/8312110
    # pylint: disable=invalid-name
    def assertListAlmostEqual(self, list1, list2, places):
        """Check List of floats are equal within some tolerance"""

        self.assertEqual(len(list1), len(list2))
        for a, b in zip(list1, list2):
            self.assertAlmostEqual(a, b, places)


if __name__ == "__main__":
    unittest.main()
